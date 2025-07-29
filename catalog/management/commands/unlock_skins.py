from catalog.models import Skin
from catalog.services.gw2_api_client import GW2APIClient
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        api_client = GW2APIClient()

        for skin_id in api_client.iter_unlocked_skin_ids():
            skin = Skin.objects.get(pk=skin_id)
            skin.is_unlocked = True
            skin.save()
            self.stdout.write(f"Unlocked Skin {skin.pk} : {skin.name}")
