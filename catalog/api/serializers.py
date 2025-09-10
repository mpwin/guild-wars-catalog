from catalog.models import Achievement, Release, Zone
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


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['name', 'requirement', 'description']


class ZoneSerializer(serializers.ModelSerializer):
    # achievements = AchievementSerializer(many=True)

    class Meta:
        model = Zone
        # fields = ['name', 'slug', 'achievements']
        fields = ['name', 'slug']
