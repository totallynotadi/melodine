from typing import Dict, List

from melodine.configs import YTMUSIC
from melodine.models import ytmusic
from melodine.models.ytmusic.artist import Artist
from melodine.models.ytmusic.track import Track
from melodine.utils import Image, URIBase
from melodine.models.base.album import AlbumBase


class Album(URIBase):

    __slots__ = (
        '_data',
        '_id',
        '_name',
        '_href',
        'uri',
        '_audio_playlist_id',
        '_type',
        '_description',
        '_year',
        '_total_tracks',
        '_duration',
        '_images',
        '_artists',
        '_tracks',
    )

    def __init__(self, data: Dict) -> None:
        self._data = None

        self._id: str = data.get(
            'browseId',
            str()
        )
        self._name: str = data.get('title')
        self._href: str
        self.uri: str = f"ytmusic:album:{self.id}"

        self._audio_playlist_id: str = data.get('audioPlaylistId', None)

        self._type: str = data.get('type', None)
        self._description: str = data.get('description', None)
        self._year: str = data.get('year', None)
        self._total_tracks: int = data.get('trackCount', None)
        self._duration: int = data.get('duration_seconds', None)

        self._images: List[Image] = [
            Image(**image)
            for image in data.get('thumbnails', [])
        ]

        self._artists: List[Dict] = data.get('artists', [])
        self._tracks: List[Dict] = data.get('tracks', [])

    def _get_data(self) -> None:
        self._data = YTMUSIC.get_album(self.id)

    @property
    def id(self) -> str:
        if not self._id:
            self._id = YTMUSIC.get_album_browse_id(
                self._data.get('audioPlaylistId')
            )
        return self._id

    @classmethod
    def from_id(cls, id: str) -> "Album":
        # the given id could be a playlistsId or a browseId.
        # a browseId starts with 'MPREb' and a audioPlaylistId starts with 'OLAK5uy'
        return cls(data={'browseId' if id.startswith("MPREb") else 'audioPlaylistId': id})

    @classmethod
    def partial(cls, data: Dict) -> "Album":
        """
        for data obtained from tracks and other shorter sources.
            `{'name': '<album-name>', 'id': '<album-id>'}`
        """
        return cls(data={
            'title': data['name'],
            'browseId': data['id']
        })

    @property
    def name(self) -> str:
        if self._name is None:
            if self._data is None:
                self._get_data()
            self._name = self._data['title']
        return self._name

    @property
    def href(self) -> str:
        return "https://music.youtube.com/playlist?list=" + self.audio_playlist_id

    @property
    def audio_playlist_id(self) -> str:
        if self._audio_playlist_id is None:
            if self._data is None:
                self._get_data()
            self._audio_playlist_id = self._data.get('audioPlaylistId')
        return self._audio_playlist_id

    @property
    def type(self) -> str:
        if self._type is None:
            if self._data is None:
                self._get_data()
            self._type = self._data.get('type')
        return self._type

    @property
    def description(self) -> str:
        if self._description is None:
            if self._data is None:
                self._get_data()
            self._description = self._data.get('description')
        return self._description

    @property
    def year(self) -> str:
        if self._year is None:
            if self._data is None:
                self._get_data()
            self._year = self._data.get('year')
        return self._year

    @property
    def total_tracks(self) -> int:
        if self._total_tracks is None:
            if self._data is None:
                self._get_data()
            self._total_tracks = self._data.get('trackCount')
        return self._total_tracks

    @property
    def duration(self) -> int:
        if self._duration is None:
            if self._data is None:
                self._get_data()
            self._duration = self._data.get('duration_seconds')
        return self._duration

    @property
    def images(self) -> List[Image]:
        if len(self._images) == 0:
            if self._data is None:
                self._get_data()
            self._images = [
                Image(**image)
                for image in self._data['thumbnails']
            ]
        return self._images

    @property
    def artists(self) -> List["ytmusic.Artist"]:
        if len(self._artists) == 0:
            if self._data is None:
                self._get_data()
            self._artists = self._data.get('artists')
        for idx, artist in enumerate(self._artists.copy()):
            if not isinstance(artist, Artist):
                artist = Artist.partial(artist)
                self._artists.insert(idx, artist)
                del self._artists[idx + 1]
        return self._artists

    @property
    def tracks(self) -> List["ytmusic.Track"]:
        if len(self._tracks) == 0:
            if self._data is None:
                self._get_data()
            self._tracks = self._data.get('tracks')
        for idx, track in enumerate(self._tracks.copy()):
            if not isinstance(track, Track):
                track = Track(track, album=self)
                self._tracks.insert(idx, track)
                del self._tracks[idx + 1]
        return self._tracks
