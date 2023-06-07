from typing import Dict, List
from melodine.services import service
from melodine.models.spotify.playlist import Playlist
from melodine.utils import Image


class Category:
    def __init__(self, data: Dict) -> None:
        self.id = data.get("id")  # pylint: disable=invalid-name
        self.name = data.get("name")
        self.images = [Image(**image) for image in data.get("icons")]

    @classmethod
    def from_id(cls, category_id: str):
        category_data = service.spotify.category(category_id)
        return cls(category_data)

    @staticmethod
    def get_categories(limit: int = 20, offset: int = 0) -> "Category":
        data = service.spotify.categories(limit=limit, offset=offset)
        return [Category(category) for category in data["categories"]["items"]]

    def get_playlist(self) -> List[Playlist]:
        data = service.spotify.category_playlists(self.id)
        return [Playlist(playlist) for playlist in data["playlists"]["items"]]
