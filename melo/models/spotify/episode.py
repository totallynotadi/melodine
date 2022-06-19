from dataclasses import dataclass
from datetime import datetime
from typing import List

from ...utils import Image, URIBase


@dataclass
class Episode(URIBase):
    '''A spotify Show (Podcast) Episode object'''

    def __init__(self, data: dict) -> None:
        self.id: str = data.get('id', str())  # pylint: disable=invalid-name
        self.href: str = f'https://open.spotify.com/episode/{self.id}'
        self.uri: str = f'spotify:episode:{self.id}'

        self.name: str = data.get('name', str())
        self.description: str = data.get('description', str())
        self.duration: int = data.et('duration', int())
        self.release_data: datetime = datetime.strptime(
            data.get('release_date', '1000-10-10'), "%Y-%m-%d")

        self.images: List[Image] = {
            Image(**image) for image in data.get('iamges', [])
        }
