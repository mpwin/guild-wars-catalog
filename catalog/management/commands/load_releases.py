import os
import yaml
from catalog.models import Achievement, Collection, Release, Skin, Zone
from django.conf import settings
from django.core.management.base import BaseCommand


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

            zones: dict = {}
            for zone_data in data['zones']:
                zone, _ = Zone.objects.get_or_create(
                    slug=zone_data['slug'],
                    defaults={
                        'name': zone_data['name'],
                        'release': release,
                        'order': zone_data['order'],
                    }
                )
                zones[zone.slug] = zone
                self.stdout.write(f"Zone : {zone.name}")
                self.load_achievements(zone, zone_data['achievement_ids'])

            for collection_data in data['collections']:
                collection, _ = Collection.objects.update_or_create(
                    name=collection_data['name'],
                    defaults={
                      'category': collection_data['category'],
                      'note': collection_data['note'],
                      'release': release,
                      'zone': zones.get(collection_data.get('zone')),
                    },
                )
                self.stdout.write(f"Collection : {collection.name}")

                for skin_id in collection_data['skin_ids']:
                    skin = Skin.objects.get(api_id=skin_id)
                    if skin.collection_id != collection.id:
                        skin.collection = collection
                        skin.save(update_fields=['collection'])

    def load_achievements(self, zone: Zone, ach_ids: list[int]) -> None:
        for ach_id in ach_ids:
            ach = Achievement.objects.get(api_id=ach_id)
            ach.release = zone.release
            ach.zone = zone
            ach.save()
            print(f"Achievement : {zone} ~ {ach.name}")
