from catalog.models import Release, Zone
from rest_framework import viewsets
from . import serializers


class ReleaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Release.objects.prefetch_related('zones')
    serializer_class = serializers.ReleaseListSerializer
