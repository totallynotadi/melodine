from typing import Dict, List, Union

from melodine.configs import YTMUSIC
from melodine.models import ytmusic
from melodine.utils import Image, URIBase
from melodine.models.base.artist import ArtistBase


class Artist(URIBase):

    __slots__ = (
        '_data',
        'id',
        '_name',
        'href',
        'uri',
        '_shuffle_id',
        '_radio_id',
        '_singles',
        '_videos',
        '_albums',
        '_songs',
        '_params',
        '_images',
        '_related_artists',
        '_followers',
        '_description',
        '_views',
    )

    def __init__(self, data: dict, **kwargs) -> None:
        self._data = None

        self.id: str = data.get('channelId')
        self._name: Union[str, None] = data.get('name', None)
        self.href: str = 'https://music.youtube.com/channel/' + \
            str(self.id or '')
        self.uri: str = 'ytmusic:artist:' + str(self.id or '')

        self._shuffle_id: str = data.get('shuffleId', None)
        self._radio_id: str = data.get('radioId', None)

        self._singles: List[Dict] = data.get('singles', {}).get('results', [])
        self._videos: List[Dict] = data.get('videos', {}).get('results', [])
        self._albums: List[Dict] = data.get('albums', {}).get('results', [])
        self._songs: List[Dict] = data.get('songs', {}).get('results', [])

        self._params: str = data.get('singles', {}).get('params', None)

        self._images: List[Image] = [
            Image(**image)
            for image in data.get('images', [])
        ]

        self._related_artists: List[Dict] = data.get(
            'related', {}).get('results', [])
        self._followers: Union[str, None] = data.get('subscribers', None)
        self._description: Union[str, None] = data.get('description', None)
        self._views: Union[str, None] = data.get('views', None)

        self.total_albums = len(self._albums) + len(self._singles)

    def _get_data(self):
        self._data = YTMUSIC.get_artist(self.id)

    @classmethod
    def from_id(cls, id: str):
        return cls(data={'channelId': id})

    @classmethod
    def partial(cls, data: Dict) -> "Artist":
        '''
        for artist data obtained from a track or an album.
            `{'name': '', 'id': ''}`
        '''
        return cls(data={
            'name': data['name'],
            'channelId': data['id']
        })

    @classmethod
    def from_search(cls, data: Dict) -> "Artist":
        '''
        for artist data obtained from a search result 
            `{'artist': '', 'browseId': '', 'shuffleId': '', 'radioId': ''}`

        also accomodates for artist data from artist['related']
            `{'title': '', 'browseId': '', 'subscribers': '', 'thumbnails': ''}`
        '''
        data['name'] = data.pop('artist', data.pop('title', str()))
        data['channelId'] = data.pop('browseId')
        return cls(data=data)

    @property
    def name(self):
        if self._name is None:
            if self._data is None:
                self._get_data()
            self._name = self._data['name']
        return self._name

    @property
    def shuffle_id(self) -> str:
        if self._shuffle_id is None:
            if self._data is None:
                self._get_data()
            self._shuffle_id = self._data['shuffleId']
        return self._shuffle_id

    @property
    def radio_id(self) -> str:
        if self._radio_id is None:
            if self._data is None:
                self._get_data()
            self._radio_id = self._data['radioId']
        return self._radio_id

    @property
    def singles(self) -> List["ytmusic.Album"]:
        '''
        singles and albums are essentially the same thing, 
        hence comparing them against albums
        '''
        from .album import Album

        if len(self._singles) == 0:
            if self._data is None:
                self._get_data()
            self._singles = self._data['singles']['results']
        for idx, single in enumerate(self._singles.copy()):
            if not isinstance(single, Album):
                single = Album(single)
                self._singles.insert(idx, single)
                del self._singles[idx + 1]
        return self._singles

    @property
    def videos(self) -> List["ytmusic.Video"]:
        from .video import Video

        if len(self._videos) == 0:
            if self._data is None:
                self._get_data()
            self._videos = self._data['videos']['results']
        for idx, video in enumerate(self._videos.copy()):
            if not isinstance(video, Video):
                video = Video(video)
                self._videos.insert(idx, video)
                del self._videos[idx + 1]
        return self._videos

    @property
    def albums(self) -> List["ytmusic.Album"]:
        from .album import Album

        if len(self._albums) == 0:
            if self._data is None:
                self._get_data()
            self._albums = self._data['albums']['results']
        for idx, album in enumerate(self._albums.copy()):
            if not isinstance(album, Album):
                album = Album(album)
                self._albums.insert(idx, album)
                del self._albums[idx + 1]
        return self._albums

    @property
    def tracks(self) -> List["ytmusic.Track"]:
        from .track import Track

        if len(self._songs) == 0:
            if self._data is None:
                self._get_data()
            self._songs = self._data['songs']['results']
        for idx, track in enumerate(self._songs.copy()):
            if not isinstance(track, Track):
                track = Track(track)
                self._songs.insert(idx, track)
                del self._songs[idx + 1]
        return self._songs

    @property
    def params(self):
        if self._params is None:
            if self._data is None:
                self._get_data()
            self._params = self._data['singles']['params']
        return self._params

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
    def related_artists(self) -> List["ytmusic.Artist"]:
        if len(self._related_artists) == 0:
            if self._data is None:
                self._get_data()
            self._related_artists = self._data['related']['results']
        for idx, artist in enumerate(self._related_artists.copy()):
            if not isinstance(artist, Artist):
                artist = Artist.from_search(artist)
                self._related_artists.insert(idx, artist)
                del self._related_artists[idx + 1]
        return self._related_artists

    @property
    def followers(self) -> str:
        if self._followers is None:
            if self._data is None:
                self._get_data()
            self._followers = self._data['subscribers']
        return self._followers

    @property
    def description(self) -> str:
        if self._description is None:
            if self._data is None:
                self._get_data()
            self._desctiption = self._data.get('description')
        return self._desctiption

    @property
    def views(self) -> int:
        if self._views is None:
            if self._data is None:
                self._get_data()
            self._views = int(
                self._data['views']
                .split(' ')[0]
                .replace(',', '_')
            )
        return self._views
