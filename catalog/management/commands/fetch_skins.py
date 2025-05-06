from catalog.models import Skin
from catalog.services.gw2_api_client import GW2APIClient
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        def valid_skin(data):
            return bool(data.get('id')) and bool(data.get('name'))

        api_client = GW2APIClient()

        for data in filter(valid_skin, api_client.iter_skins()):
            defaults = {
                'name': data.get('name'),
                'category': data.get('type'),
                'details': data.get('details', {}),
            }

            skin, _ = Skin.objects.update_or_create(
                api_id=data['id'],
                defaults=defaults,
            )

            self.stdout.write(
                f"Skin {skin.api_id} : {skin.name}"
            )
