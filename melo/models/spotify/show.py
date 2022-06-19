from dataclasses import dataclass
from typing import Dict, List, Union

from melo.models.spotify.episode import Episode

from ...utils import SPOTIFY, Image, URIBase


@dataclass
class Show(URIBase):
    '''A spotify Show (Podcast) object'''
    def __init__(self, data: Union[Dict, str]) -> None:
        self.id: str = data.get('id', str())  #pylint: disable=invalid-name
        self.href: str = f'https://open.spotify.com/show/{self.id}'
        self.uri: str = f'spotify:show:{self.id}'

        self.name: str = data.get('name', str())
        self.description: str = data.get('description', str())
        self.total_episodes: int = data.get('total_episodes', int())
        self.publisher: str = data.get('published', str())
        self._episodes: Union[List[Episode], None] = data.get('episodes')

        self.images: List[Image] = [
            Image(**image) for image in data.get('images', [])
        ]

    @property
    def episodes(self):
        if self._episodes:
            return self._episodes

        self._episodes = SPOTIFY.show_episodes(self.id)
        self._episodes = [Episode(episode) for episode in self._episodes]

        return self._episodes
