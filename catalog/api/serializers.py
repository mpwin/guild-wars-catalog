from catalog.models import Achievement, Collection, Release, Zone
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


class AchievementCollectionSerializer(serializers.ModelSerializer):
    achievements = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['name', 'achievements']

    def get_achievements(self, obj):
        result = []
        for item in obj.items.all():
            result.append(AchievementSerializer(item.content_object).data)
        return result


class ZoneSerializer(serializers.ModelSerializer):
    achievement_collections = serializers.SerializerMethodField()

    class Meta:
        model = Zone
        fields = [
            'name',
            'slug',
            'achievement_collections',
        ]

    def get_achievement_collections(self, obj):
        collections = obj.collections.filter(
            category='achievement',
        ).order_by('order')
        result = []
        for collection in collections:
            result.append(AchievementCollectionSerializer(collection).data)
        return result
