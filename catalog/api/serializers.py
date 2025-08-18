from catalog.models import Release, Zone
from rest_framework import serializers


class ZoneListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['name', 'slug', 'order']


class ReleaseListSerializer(serializers.ModelSerializer):
    zones = ZoneListItemSerializer(many=True)

    class Meta:
        model = Release
        fields = ['name', 'slug', 'order', 'zones']
