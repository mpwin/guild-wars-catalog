import os
import yaml
from catalog.models import Release, Zone
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
