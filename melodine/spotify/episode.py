from dataclasses import dataclass
from datetime import datetime
from typing import List

from melodine.utils import Image
from melodine.base.misc import URIBase


from melodine.services import service


@dataclass
class Episode(URIBase):
    """A spotify Show (Podcast) Episode object"""

    def __init__(self, data: dict) -> None:
        from .show import Show

        self.id: str = data.get("id", str())  # pylint: disable=invalid-name
        self.href: str = f"https://open.spotify.com/episode/{self.id}"
        self.uri: str = f"spotify:episode:{self.id}"

        self.name: str = data.get("name", str())
        self.description: str = data.get("description", str())
        self.duration: int = data.get("duration", int())
        self.release_data: datetime = datetime.strptime(
            data.get("release_date", "1000-10-10"), "%Y-%m-%d"
        )

        self._show = None if data.get("show") is None else Show(data.get("show"))
        self.images: List[Image] = [Image(**image) for image in data.get("images", [])]

    def __repr__(self) -> str:
        return f"<spotify.Episode: {self.name!r}>"

    @classmethod
    def from_id(cls, id: str) -> "Episode":
        return cls(data=service.spotify.episode(id))

    @property
    def show(self):
        from .show import Show

        if self._show is not None:
            return self.show

        self._show = Show(service.spotify.episode(self.id)["show"])
        return self._show

    def add_to_playlist(self, playlist_id) -> None:
        service.spotify.playlist_add_items(playlist_id=playlist_id, items=[self.id])

    # def is_saved(self) -> bool:
    #     return service.spotify.current_user_saved_episodes_contains([self.id])[0]

    # def save_episode(self) -> None:
    #     return service.spotify.current_user_saved_episodes_add([self.id])

    # def unsave_episode(self) -> None:
    #     return service.spotify.current_user_saved_episodes_delete([self.id])
