import os
import yaml

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import (
    Achievement,
    Collection,
    CollectionItem,
    Release,
    Skin,
    Zone
)


RELEASES_DIR = os.path.join(settings.BASE_DIR, 'catalog', 'data', 'releases')


class Command(BaseCommand):

    def handle(self, *args, **options):
        base_dir = RELEASES_DIR

        for filename in os.listdir(base_dir):
            filepath = os.path.join(base_dir, filename)
            with open(filepath) as f:
                data = yaml.safe_load(f)

            release, _ = Release.objects.get_or_create(
                slug=data['release']['slug'],
                defaults={
                    'name': data['release']['name'],
                    'order': data['release']['order'],
                }
            )
            self.stdout.write(f"Release : {release.name}")

            if 'achievement_collections' in data['release']:
                self.load_skins(release, data['release']['achievement_collections'])
            if 'skin_collections' in data['release']:
                self.load_skins(release, data['release']['skin_collections'])

            for zone_data in data['zones']:
                zone, _ = Zone.objects.get_or_create(
                    slug=zone_data['slug'],
                    defaults={
                        'name': zone_data['name'],
                        'release': release,
                        'order': zone_data['order'],
                    }
                )
                self.stdout.write(f"Zone : {zone.name}")

                self.load_achs(zone, zone_data['achievement_collections'])
                if 'skin_collections' in zone_data:
                    self.load_skins(zone, zone_data['skin_collections'])

    def load_achs(self, obj: Release | Zone, colls: list) -> None:
        if isinstance(obj, Release):
            release = obj
            zone = None
        if isinstance(obj, Zone):
            release = obj.release
            zone = obj

        for coll_order, coll_data in enumerate(colls, 1):
            collection, _ = Collection.objects.get_or_create(
                name=coll_data['name'],
                category='achievement',
                release=release,
                zone=zone,
                defaults={
                    'order': coll_order,
                }
            )

            content_type = ContentType.objects.get_for_model(Achievement)
            for ach_order, ach_id in enumerate(coll_data['achievement_ids'], 1):
                CollectionItem.objects.get_or_create(
                    collection=collection,
                    content_type=content_type,
                    object_id=ach_id,
                    defaults={
                        'order': ach_order,
                    }
                )

    def load_skins(self, obj: Release | Zone, colls: list) -> None:
        if isinstance(obj, Release):
            release = obj
            zone = None
        if isinstance(obj, Zone):
            release = obj.release
            zone = obj

        for coll_order, coll_data in enumerate(colls, 1):
            collection, _ = Collection.objects.get_or_create(
                name=coll_data['name'],
                category='skin',
                release=release,
                zone=zone,
                defaults={
                    'order': coll_order,
                }
            )

            content_type = ContentType.objects.get_for_model(Skin)
            for skin_order, skin_id in enumerate(coll_data['skin_ids'], 1):
                CollectionItem.objects.get_or_create(
                    collection=collection,
                    content_type=content_type,
                    object_id=skin_id,
                    defaults={
                        'order': skin_order,
                    }
                )
