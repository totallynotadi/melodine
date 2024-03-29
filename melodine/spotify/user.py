from typing import Dict, List

from melodine.services import service
from melodine.spotify.playlist import Playlist
from melodine.utils import Image
from melodine.base.misc import URIBase


class User(URIBase):
    def __init__(self, data: Dict) -> None:
        self.id = data.get("id")  # pylint: disable=invalid-name
        self.name = data.get("display_name")
        self.href = "open.spotify.com/user/" + self.id
        self.uri = data.get("uri")
        self.followers = data.get("followers")
        self.type = data.get("type")
        self._images = [Image(**image_) for image_ in data.get("images", [])]

    def __repr__(self):
        return f"<spotify.User: {(self.name or self.id)!r}>"

    @classmethod
    def from_id(cls, id: str) -> "User":
        return cls(data=service.spotify.user(id))

    @property
    def images(self):
        """thumbnails for a user's profile"""
        if self._images:
            return self._images

        data = service.spotify.user(self.id)
        self._images = [Image(**image) for image in data.get("images", [])]
        return self._images

    def user_playlists(self, limit: int = 30, offset: int = 0) -> List[Playlist]:
        """Get a user's playlists"""
        data = service.spotify.current_user_playlists(limit=limit, offset=offset)

        return [Playlist(playlist) for playlist in data.get("items", [])]

    # @cached_property
    # def all_user_playlists(self) -> List[Playlist]:
    #     """Get all playlists from a user"""
    #     data = {"next": "<placeholder>"}
    #     results = []

    #     while data.get("next"):
    #         if data["next"] == "<placeholder>":
    #             data = service.spotify.user_playlists(self.id)
    #         else:
    #             data = service.spotify.next(data)
    #         results += data["items"]
    #     return [Playlist(playlist) for playlist in data]

    def is_followed(self) -> bool:
        return service.spotify.current_user_following_users([self.id])[0]

    def follow_user(self) -> None:
        return service.spotify.user_follow_users([self.id])

    def unfollow_user(self) -> None:
        return service.spotify.user_unfollow_users([self.id])
