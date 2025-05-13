import os
import yaml
from catalog.models import Collection, Skin
from django.conf import settings
from django.core.management.base import BaseCommand


COLLECTIONS_DIR = os.path.join(settings.BASE_DIR, 'catalog', 'collections')


class Command(BaseCommand):

    def handle(self, *args, **options):
        base_dir = COLLECTIONS_DIR

        for filename in os.listdir(base_dir):
            filepath = os.path.join(base_dir, filename)
            with open(filepath) as f:
                collections_data = yaml.safe_load(f)

            for data in collections_data:
                defaults = {
                    'note': data.get('note'),
                }

                collection, _ = Collection.objects.update_or_create(
                    name=data['name'],
                    defaults=defaults,
                )

                for skin_id in data['skin_ids']:
                    skin = Skin.objects.get(api_id=skin_id)
                    if skin.collection_id != collection.id:
                        skin.collection = collection
                        skin.save(update_fields=['collection'])
