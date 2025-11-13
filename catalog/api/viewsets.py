from catalog.models import Release, Zone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from . import serializers


class ReleaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Release.objects.prefetch_related('zones')
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ReleaseListSerializer
        return serializers.ReleaseSerializer


class ZoneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Zone.objects.all()
    lookup_field = 'slug'
    serializer_class = serializers.ZoneSerializer
