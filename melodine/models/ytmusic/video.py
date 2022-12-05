from typing import Dict, List, Union

from melodine.utils import URIBase, Image
from melodine.configs import YTMUSIC
from melodine.innertube import InnerTube
from melodine.models import ytmusic
from melodine.models.ytmusic.artist import Artist
from melodine.models.ytmusic.track import Track


class Video(URIBase):

    __slots__ = (
        '_data',
        'id',
        '_name',
        'href',
        'uri',
        '_artists',
        '_explicit',
        '_views',
        '_duration',
        '_images',

        '_url',
        '_recs',
        '_recs_offset'
    )

    def __init__(self, data: Dict) -> None:
        self._data = None

        self.id: str = data.get('videoId', data.get('resourceId'))
        self._name: str = data.get('title', None)
        self.href: str = "https://music.youtube.com/watch?v=" + self.id
        self.uri: str = "ytmusic:video:" + self.id

        self._artists: List[Dict] = data.get('artists', [])

        self.explicit: bool = data.get('isExplicit', False)
        self._views: str = data.get('views', data.get('viewCount', None))

        self._duration: Union[int, None] = data.get(
            'lengthSeconds', data.get('duration_seconds', data.get('length', None)))

        self._images: List[Image] = [
            Image(**image)
            for image in data.get('thumbnails', [])
        ]

        self.playlist_id = data.get('playlist_id', None)

        self._url = str()
        self._recs = list()
        self._recs_offset = int()  # aka 0

    def _get_data(self) -> None:
        self._data = YTMUSIC.get_song(self.id)['videoDetails']

    @classmethod
    def from_id(cls, id) -> "Video":
        return cls(data={'videoId': id})

    @classmethod
    def from_raw(cls, data: Dict) -> "Video":
        data['artists'] = [
            {
                'name': data.pop('author'),
                'id': data.pop('channelId')
            }
        ]
        data['thumbnails'] = data.pop('thumbnail').get('thumbnails')
        return cls(data=data)

    @property
    def name(self) -> str:
        if self._name is None:
            if self._data is None:
                self._get_data()
            self._name = self._data['title']
        return self._name

    @property
    def artists(self) -> Union[Artist, "ytmusic.User"]:
        from .user import User

        if len(self._artists) == 0:
            if self._data is None:
                self._get_data()
            self._artists = [{'name': self._data.pop(
                'author'), 'id': self._data.pop('channelId')}]
        for idx, artist in enumerate(self._artists.copy()):
            if not isinstance(artist, (Artist, User, )):
                # since a video is'nt neccessarily owned by an artist each time,
                # so it's from a user in case it's not from an artist.
                try:
                    user = YTMUSIC.get_user(artist['id'])
                    artist = User(user, id=artist['id'])
                except (KeyError, ValueError):
                    artist = Artist.partial(artist)
                self._artists.insert(idx, artist)
                del self._artists[idx + 1]
        return self._artists

    @property
    def views(self) -> int:
        if self._views is None or not self._views.isdigit():
            if self._data is None:
                self._get_data()
            self._views = self._data['viewCount']
        return int(self._views)

    @property
    def duration(self) -> int:
        if self._duration is None:
            if self._data is None:
                self._get_data()
            self._duration = self._data['lengthSeconds']
        if isinstance(self._duration, str):
            if ':' in self._duration:
                self._duration = self._duration.split(':')
                self._duration = int(
                    self._duration[0]) * 60 + int(self._duration[1])
            else:
                self._duration = int(self._duration)
        return self._duration

    @property
    def images(self) -> List[Image]:
        if len(self._images) == 0:
            if self._data is None:
                self._get_data()
            self._images = self._data.get('thumbnail')['thumbnails']
        for idx, image in enumerate(self._images.copy()):
            if not isinstance(image, Image):
                image = Image(**image)
                self._images.insert(idx, image)
                del self._images[idx + 1]
        return self._images

    @property
    def url(self) -> str:
        '''Get the playback URL for a track or video

        retrieves the higest quality adaptive track by default
        '''
        if self._url:
            return self._url

        innertube = InnerTube()
        video_info = innertube.player(self.id)
        self._url = video_info['streamingData']['adaptiveFormats'][-1]['url']

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
        '''used to get new recommendations for the track.

        earlier fetched recommended tracks can be accessed whith `.recommendations'''

        data = YTMUSIC.get_watch_playlist(
            self.id,
            f"RDAMVM{self.id}",
            limit=self._recs_offset + limit
        )

        tracks = data['tracks'][self._recs_offset: (self._recs_offset + limit)]
        tracks = [Track(track) for track in tracks]
        self._recs.append(tracks)
        self._recs_offset += limit

        return tracks
