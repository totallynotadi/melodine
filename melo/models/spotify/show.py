from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List, Optional, Union

from ...utils import SPOTIFY, Image, URIBase
from .episode import Episode


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

        self.images: List[Image] = [
            Image(**image) for image in data.get('images', [])
        ]

    @property
    def episodes(
        self,
        *,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0
    ) -> List[Episode]:
        '''Get paged results for episodes from a show based on the limit and offset'''

        data = SPOTIFY.show_episodes(
            self.id,
            limit=limit,
            offset=offset
        )

        return [Episode(episode) for episode in data['items']]

    @cached_property
    def get_all_episodes(self) -> List[Episode]:
        '''Get a list of all the episodes of a show'''
        result = []
        offset = 0

        while len(result) < self.total_episodes:
            data = SPOTIFY.show_episodes(
                self.id,
                limit=10,
                offset=offset
            )
            result += [Episode(episode) for episode in data['items']]
            offset += 10

        return result
