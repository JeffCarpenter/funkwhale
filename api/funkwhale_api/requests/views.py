from rest_framework import generics, mixins, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from funkwhale_api.music.views import SearchMixin

from . import filters
from . import models
from . import serializers


class ImportRequestViewSet(
        SearchMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    serializer_class = serializers.ImportRequestSerializer
    queryset = (
        models.ImportRequest.objects.all()
              .select_related()
              .order_by('-creation_date'))
    search_fields = ['artist_name', 'album_name', 'comment']
    filter_class = filters.ImportRequestFilter
    ordering_fields = ('id', 'artist_name', 'creation_date', 'status')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        return context