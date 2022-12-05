from functools import cached_property
from typing import Dict, List, Optional

from melodine.configs import SPOTIFY
from melodine.models.spotify.playlist import Playlist
from melodine.utils import Image, URIBase


class User(URIBase):
    def __init__(self, data: Dict) -> None:
        self.id = data.get('id')  #pylint: disable=invalid-name
        self.name = data.get('display_name')
        self.href = 'open.spotify.com/user/' + self.id
        self.uri = data.get('uri')
        self.followers = data.get('followers')
        self.type = data.get('type')
        self._images = [Image(**image_) for image_ in data.get('images', [])]

    def __repr__(self):
        return f"<spotify.User: {(self.name or self.id)!r}>"

    @property
    def images(self):
        '''thumbnails for a user's profile'''
        if self._images:
            return self._images

        data = SPOTIFY.user(self.id)
        self._images = [Image(**image) for image in data.get('images', [])]
        return self._images

    def user_playlists(
        self,
        limit: Optional[int] = 30,
        offset: Optional[int] = 0
    ) -> List[Playlist]:
        '''Get a user's playlists'''
        data = SPOTIFY.user_playlists(
            self.id,
            limit=limit,
            offset=offset
        )

        return [Playlist(playlist) for playlist in data.get('items', [])]

    @cached_property
    def all_user_playlists(self) -> List[Playlist]:
        '''Get all playlists from a user'''
        data = {'next': '<placeholder>'}
        results = []

        while data.get('next'):
            if data['next'] == '<placeholder>':
                data = SPOTIFY.user_playlists(self.id)
            else:
                data = SPOTIFY.next(data)
            results += data['items']
        return [Playlist(playlist) for playlist in data]

    def is_followed(self) -> bool:
        return SPOTIFY.current_user_following_users([self.id])[0]

    def follow_user(self) -> None:
        return SPOTIFY.user_follow_users([self.id])

    def unfollow_user(self) -> None:
        return SPOTIFY.user_unfollow_users([self.id])
