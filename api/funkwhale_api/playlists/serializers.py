from django.db import transaction
from rest_framework import serializers

from funkwhale_api.common import preferences
from funkwhale_api.music.models import Track
from funkwhale_api.music.serializers import TrackSerializer
from funkwhale_api.users.serializers import UserBasicSerializer

from . import models


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer()

    class Meta:
        model = models.PlaylistTrack
        fields = ("id", "track", "playlist", "index", "creation_date")


class PlaylistTrackWriteSerializer(serializers.ModelSerializer):
    index = serializers.IntegerField(required=False, min_value=0, allow_null=True)

    class Meta:
        model = models.PlaylistTrack
        fields = ("id", "track", "playlist", "index")

    def validate_playlist(self, value):
        if self.context.get("request"):
            # validate proper ownership on the playlist
            if self.context["request"].user != value.user:
                raise serializers.ValidationError(
                    "You do not have the permission to edit this playlist"
                )
        existing = value.playlist_tracks.count()
        max_tracks = preferences.get("playlists__max_tracks")
        if existing >= max_tracks:
            raise serializers.ValidationError(
                "Playlist has reached the maximum of {} tracks".format(max_tracks)
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        index = validated_data.pop("index", None)
        instance = super().create(validated_data)
        instance.playlist.insert(instance, index)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        update_index = "index" in validated_data
        index = validated_data.pop("index", None)
        super().update(instance, validated_data)
        if update_index:
            instance.playlist.insert(instance, index)
        return instance

    def get_unique_together_validators(self):
        """
        We explicitely disable unique together validation here
        because it collides with our internal logic
        """
        return []


class PlaylistSerializer(serializers.ModelSerializer):
    tracks_count = serializers.SerializerMethodField(read_only=True)
    user = UserBasicSerializer(read_only=True)

    class Meta:
        model = models.Playlist
        fields = (
            "id",
            "name",
            "tracks_count",
            "user",
            "modification_date",
            "creation_date",
            "privacy_level",
        )
        read_only_fields = ["id", "modification_date", "creation_date"]

    def get_tracks_count(self, obj):
        try:
            return obj.tracks_count
        except AttributeError:
            # no annotation?
            return obj.playlist_tracks.count()


class PlaylistAddManySerializer(serializers.Serializer):
    tracks = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Track.objects.for_nested_serialization()
    )
