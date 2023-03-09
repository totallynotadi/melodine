from typing import Any, Dict, List

from melodine.configs import YTMUSIC
from melodine.innertube import InnerTube
from melodine.models import ytmusic
from melodine.models.base.track import TrackBase
from melodine.utils import Image, URIBase


class Track(URIBase):
    '''A YTMusic Track Object

    Attributes
    ---------
    id: str
        The Spotify ID for the Track
    '''

    __slots__ = [
        'id',
        'name',
        'href',
        'uri',
        'explicit',
        'duration',
        'images',
        '_artists',
        '_album',

        '_url'
        '_recs',
        '_recs_offset'
    ]

    def __init__(self, data: Dict, **kwargs) -> None:
        self.id: str = data.get('videoId')
        self.name: str = data.get('title')
        self.href: str = "https://music.youtube.com/watch?v=" + self.id
        self.uri: str = f"ytmusic:track:{self.id}"

        self.explicit: bool = data.get('isExplicit', False)
        self.duration: int = data.get(
            'duration_seconds', data.get('lengthSeconds', 0))

        images: List[Dict]
        if 'thumbnail' in data:
            images = data.get('thumbnail')
            # sometimes, the images are in yet another nested dict
            if 'thumbnails' in images:
                # because it's a dict
                images = images.get('thumbnails')
        else:
            images = data.get('thumbnails')
        self.images: List[Image] = [
            Image(**image) for image in (images or [])
        ]

        artists: Any
        if 'artists' in data:
            artists = data.get('artists')
        else:
            artists = [{
                'name': data.get('author'),
                'id': data.get('channelId')
            }]
        self._artists: List[Dict] = artists

        album: Any
        if 'album' in data and not isinstance(data['album'], str):
            album = data.get('album')
        elif 'album' in kwargs:
            album = kwargs.get('album')
        else:
            album = None
        self._album: Dict = album

        self._url = str()
        self._recs = list()
        self._recs_offset = int()  # aka 0

    @classmethod
    def from_id(cls, id: str) -> "Track":
        '''tracks obtained directly from an ID have the album attribute as None'''
        return cls(data=YTMUSIC.get_song(id)['videoDetails'])

    @property
    def artists(self) -> List["ytmusic.Artist"]:
        """Get a list of all Artists from the track"""
        from .artist import Artist

        for idx, artist in enumerate(self._artists.copy()):
            if not isinstance(artist, Artist):
                artist = Artist.partial(artist)
                self._artists.insert(idx, artist)
                del self._artists[idx + 1]
        return self._artists

    @property
    def album(self) -> "ytmusic.Album":
        '''Get the Album which the track belongs to'''
        from .album import Album

        if self._album is not None and not isinstance(self._album, Album):
            self._album = Album.partial(self._album)
        return self._album

    @property
    def url(self) -> str:
        '''fetch the playback url for the track.'''
        if not self._url:
            video_id = YTMUSIC.search(
                f"{self.artists[0].name} - {self.name}", filter='songs'
            )[0]['videoId'] if not self.id else self.id

            video_info = InnerTube().player(video_id)

            # print(video_info['streamingData']['expiresInSeconds'])
            # print(video_info['streamingData']['formats'][0].keys())
            self._url = video_info['streamingData']['formats'][-2]['url']

            return self._url
        return self._url

    def cache_url(self) -> None:
        '''just a dummy call to trigger the url fetching.'''
        if not self.url:
            self._url = self.url

    @property
    def recommendations(self) -> List["Track"]:
        '''A list of recommended tracks for this track already fetched upto this point.

        it is initially empty and gets populated as more calls are made to `get_recommendations` are made.

        use `get_recommendations` to fetch new recommendations. instead'''
        return self._recs

    def get_recommendations(self, limit: int = 10) -> List["Track"]:
        '''
        used to get new recommendations for the track.

        earlier fetched recommended tracks can be accessed whith `.recommendations
        '''

        data = YTMUSIC.get_watch_playlist(
            self.id,
            f"RDAMVM{self.id}",
            limit=self._recs_offset + limit
        )

        tracks = data['tracks'][self._recs_offset: (self._recs_offset + limit)]
        tracks = [Track(track) for track in tracks]
        self._recs.extend(tracks)
        self._recs_offset += limit

        return tracks
