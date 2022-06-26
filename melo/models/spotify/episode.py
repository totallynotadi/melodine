from dataclasses import dataclass
from datetime import datetime
from typing import List

from ...utils import SPOTIFY, Image, URIBase


@dataclass
class Episode(URIBase):
    '''A spotify Show (Podcast) Episode object'''

    def __init__(self, data: dict) -> None:
        from .show import Show

        self.id: str = data.get('id', str())  # pylint: disable=invalid-name
        self.href: str = f'https://open.spotify.com/episode/{self.id}'
        self.uri: str = f'spotify:episode:{self.id}'

        self.name: str = data.get('name', str())
        self.description: str = data.get('description', str())
        self.duration: int = data.get('duration', int())
        self.release_data: datetime = datetime.strptime(
            data.get('release_date', '1000-10-10'), "%Y-%m-%d")

        self.show = Show(data.get('show'))
        self.images: List[Image] = [
            Image(**image) for image in data.get('images', [])
        ]

    def __repr__(self) -> str:
        return f'<spotify.Episode: {self.name!r}>'

    def add_to_playlist(self, playlist_id) -> None:
        SPOTIFY.playlist_add_items(
            playlist_id=playlist_id,
            items=[self.id]
        )

    def is_saved(self) -> bool:
        return SPOTIFY.current_user_saved_episodes_contains([self.id])[0]

    def save_episode(self) -> None:
        return SPOTIFY.current_user_saved_episodes_add([self.id])

    def unsave_episode(self) -> None:
        return SPOTIFY.current_user_saved_episodes_delete([self.id])
