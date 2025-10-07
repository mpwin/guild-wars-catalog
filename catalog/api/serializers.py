from catalog.models import Achievement, Collection, Release, Skin, Zone
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
    id = serializers.IntegerField(source='api_id')

    class Meta:
        model = Achievement
        fields = ['id', 'name', 'requirement', 'description']


class AchievementCollectionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['name', 'type', 'items']

    def get_type(self, obj):
        return 'achievement'

    def get_items(self, obj):
        items = []
        for item in obj.items.all():
            items.append(AchievementSerializer(item.content_object).data)
        return items


class SkinSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='api_id')

    class Meta:
        model = Skin
        fields = ['id', 'name']


class SkinCollectionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['name', 'type', 'items']

    def get_type(self, obj):
        return 'skin'

    def get_items(self, obj):
        items = []
        for item in obj.items.all():
            items.append(SkinSerializer(item.content_object).data)
        return items


class ReleaseSerializer(serializers.ModelSerializer):
    zones = ZoneListItemSerializer(many=True)
    achievement_collections = serializers.SerializerMethodField()
    skin_collections = serializers.SerializerMethodField()

    class Meta:
        model = Release
        fields = [
            'name',
            'slug',
            'zones',
            'achievement_collections',
            'skin_collections',
        ]

    def get_achievement_collections(self, obj):
        collections = obj.collections.filter(
            category='achievement',
            zone=None,
        ).order_by('order')
        result = []
        for collection in collections:
            result.append(AchievementCollectionSerializer(collection).data)
        return result

    def get_skin_collections(self, obj):
        collections = obj.collections.filter(
            category='skin',
            zone=None,
        ).order_by('order')
        result = []
        for collection in collections:
            result.append(SkinCollectionSerializer(collection).data)
        return result


class ZoneSerializer(serializers.ModelSerializer):
    achievement_collections = serializers.SerializerMethodField()
    skin_collections = serializers.SerializerMethodField()

    class Meta:
        model = Zone
        fields = [
            'name',
            'slug',
            'achievement_collections',
            'skin_collections',
        ]

    def get_achievement_collections(self, obj):
        collections = obj.collections.filter(
            category='achievement',
        ).order_by('order')
        result = []
        for collection in collections:
            result.append(AchievementCollectionSerializer(collection).data)
        return result

    def get_skin_collections(self, obj):
        collections = obj.collections.filter(
            category='skin',
        ).order_by('order')
        result = []
        for collection in collections:
            result.append(SkinCollectionSerializer(collection).data)
        return result
