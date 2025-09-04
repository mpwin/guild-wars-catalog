from catalog.models import Achievement
from catalog.services.gw2_api_client import GW2APIClient
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        def valid_achievement(data):
            return bool(data.get('id')) and bool(data.get('name'))

        api_client = GW2APIClient()

        for data in filter(valid_achievement, api_client.iter_achievements()):
            defaults = {
                'name': data.get('name'),
                'description': data.get('description'),
                'requirement': data.get('requirement'),
            }

            achievement, _ = Achievement.objects.update_or_create(
                api_id=data['id'],
                defaults=defaults,
            )

            self.stdout.write(
                f"Achievement {achievement.api_id}"
            )
