import os
import requests
import time
from collections.abc import Iterator


class GW2APIClient:

    def __init__(self):
        self.api_key = os.getenv('GW2_API_KEY')
        self.base_url = "https://api.guildwars2.com/v2/"
        self.session = requests.Session()

    def iter_achievements(self) -> Iterator[dict]:
        response = self.session.get(
            self.base_url + "achievements",
            params={'page': 0, 'page_size': 200},
        )
        page_total = int(response.headers.get('X-Page-Total', 1))

        for page in range(page_total):
            response = self.session.get(
                self.base_url + "achievements",
                params={'page': page, 'page_size': 200},
            )
            achievements = response.json()

            for achievement in achievements:
                yield achievement

            time.sleep(2)

    def iter_skins(self) -> Iterator[dict]:
        response = self.session.get(
            self.base_url + "skins",
            params={'page': 0, 'page_size': 200},
        )
        page_total = int(response.headers.get('X-Page-Total', 1))

        for page in range(page_total):
            response = self.session.get(
                self.base_url + "skins",
                params={'page': page, 'page_size': 200},
            )
            skins = response.json()

            for skin in skins:
                yield skin

            time.sleep(2)

    def iter_unlocked_skin_ids(self) -> Iterator[int]:
        response = self.session.get(
            self.base_url + "account/skins",
            headers={'Authorization': f'Bearer {self.api_key}'},
        )
        response.raise_for_status()
        return iter(response.json())
