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


class ZoneViewSet(viewsets.ViewSet):
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        queryset = Zone.objects.all()
        zone = get_object_or_404(queryset, slug=slug)
        serializer = serializers.ZoneSerializer(zone)
        return Response(serializer.data)
