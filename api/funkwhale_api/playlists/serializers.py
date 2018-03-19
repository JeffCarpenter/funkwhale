from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from taggit.models import Tag

from funkwhale_api.music.serializers import TrackSerializerNested

from . import models


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializerNested()

    class Meta:
        model = models.PlaylistTrack
        fields = ('id', 'track', 'playlist', 'index', 'creation_date')


class PlaylistTrackWriteSerializer(serializers.ModelSerializer):
    index = serializers.IntegerField(
        required=False, min_value=0, allow_null=True)

    class Meta:
        model = models.PlaylistTrack
        fields = ('id', 'track', 'playlist', 'index')

    def validate_playlist(self, value):
        if self.context.get('request'):
            # validate proper ownership on the playlist
            if self.context['request'].user != value.user:
                raise serializers.ValidationError(
                    'You do not have the permission to edit this playlist')
        existing = value.playlist_tracks.count()
        if existing >= settings.PLAYLISTS_MAX_TRACKS:
            raise serializers.ValidationError(
                'Playlist has reached the maximum of {} tracks'.format(
                    settings.PLAYLISTS_MAX_TRACKS))
        return value

    @transaction.atomic
    def create(self, validated_data):
        index = validated_data.pop('index', None)
        instance = super().create(validated_data)
        instance.playlist.insert(instance, index)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        update_index = 'index' in validated_data
        index = validated_data.pop('index', None)
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

    class Meta:
        model = models.Playlist
        fields = ('id', 'name', 'privacy_level', 'creation_date')
        read_only_fields = ['id', 'creation_date']
