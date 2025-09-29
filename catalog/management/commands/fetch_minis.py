from catalog.models import Mini
from catalog.services.gw2_api_client import GW2APIClient
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        def valid_mini(data):
            return bool(data.get('id')) and bool(data.get('name'))

        api_client = GW2APIClient()

        for data in filter(valid_mini, api_client.iter_minis()):
            defaults = {
                'name': data.get('name'),
            }

            mini, _ = Mini.objects.update_or_create(
                api_id=data['id'],
                defaults=defaults,
            )

            self.stdout.write(
                f"Mini {mini.api_id} : {mini.name}"
            )
