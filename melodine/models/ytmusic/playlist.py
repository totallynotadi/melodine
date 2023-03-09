"""
a playlist is owned only by users.

some artists may own playlists but they dont show up the artists's profile.
so a simple try catch for when  a artist owns a playlist shoudl suffice.
"""

from typing import Dict, List, Union

from melodine.configs import YTMUSIC
from melodine.models import ytmusic
from melodine.models.ytmusic.artist import Artist
from melodine.models.ytmusic.track import Track
from melodine.models.ytmusic.video import Video
from melodine.utils import Image, URIBase
from melodine.models.base.playlist import PlaylistBase


class Playlist(URIBase):

    __slots__ = (
        '_data',
        'id',
        '_name',
        'href',
        'uri',
        '_tracks',
        '_owner',
        '_duration',
        '_total_tracks',
        '_images',
        '_description',
        '_year',
    )

    def __init__(self, data: Dict):
        self._data = None

        self.id: str = data.get('id', data.get(
            'playlistId', data.get('browseId')))  # pylint: disable=invalid-name
        if self.id.startswith('VL'):
            self.id = self.id[2:]
        self._name: str = data.get('title', None)
        self.href: str = "https://music.youtube.com/playlist?list=" + self.id
        self.uri: str = "ytmusic:user:" + self.id

        self._tracks: List[Dict] = data.get('tracks', [])
        self._owner: Union[Dict, str] = data.get('author', [])
        self._duration: Union[int, None] = data.get('duration_seconds', None)
        self._total_tracks: Union[int, None] = data.get(
            'trackCount', data.get('itemCount'))

        self.images: List[Image] = [
            Image(**image)
            for image in data.get('thumbnails', [])
        ]

        self._description = data.get('description', None)
        self._year = data.get('year', None)

    def _get_data(self) -> None:
        self._data = YTMUSIC.get_playlist(self.id)

    @classmethod
    def from_id(cls, id: str) -> "Playlist":
        return cls(data={'id': id})

    @property
    def name(self) -> str:
        if self._name is None:
            if self._data is None:
                self._get_data()
            self._name = self._data['title']
        return self._name

    @property
    def tracks(self) -> List[Union[Video, Track]]:
        if len(self._tracks) == 0:
            if self._data is None:
                self._get_data()
            self._tracks = self._data['tracks']
        for idx, video in enumerate(self._tracks.copy()):
            if not isinstance(video, (Video, Track)):
                if video['videoId'] is not None:
                    if video.get('album') is not None:
                        video = Track(video)
                    else:
                        video = Video(video)
                    self._tracks.insert(idx, video)
                    del self._tracks[idx + 1]
                else:
                    self._tracks[idx] = None
        self._tracks = list(
            filter(lambda track: track is not None, self._tracks)
        )
        return self._tracks

    @property
    def owner(self) -> Union["ytmusic.User", Artist]:
        from .user import User

        if isinstance(self._owner, str) or not self._owner:
            if self._data is None:
                self._get_data()
            self._owner = self._data['author']

        if not isinstance(self._owner, (Artist, User)):
            try:
                user = YTMUSIC.get_user(self._owner if isinstance(
                    self._owner, str) else self._owner['id'])
                self._owner = User.from_id(self._owner) if isinstance(
                    self._owner, str) else User(user, id=self._owner['id'])
            except (KeyError, ValueError, Exception):
                self._owner = Artist.from_id(self._owner) if isinstance(
                    self._owner, str) else Artist(self._owner)
        return self._owner

    @property
    def duration(self) -> int:
        if self._duration is None:
            if self._data is None:
                self._get_data()
            self._duration = self._data['duration_seconds']
        return self._duration

    @property
    def total_tracks(self) -> int:
        if self._total_tracks is None:
            if self._data is None:
                self._get_data()
            self._total_tracks = self._data['trackCount']
        return self._total_tracks

    @property
    def description(self) -> str:
        if self._description is None:
            if self._data is None:
                self._get_data()
            self._description = self._data['description']
        return str(self._description or '')

    @property
    def year(self) -> int:
        if self._year is None:
            if self._data is None:
                self._get_data()
            self._year = int(self._data['year'])
        return self._year
