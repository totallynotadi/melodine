from typing import Any, Dict, List, Optional, Union

from ...innertube import InnerTube
from ...utils import YTMUSIC, Image, URIBase
from .artist import Artist


class Video(URIBase):
    """A YTMusic Video object

    Basically the same as a YTMusic Track
    but represents a tiny distinction between a track and video
    that a Video does not have a album while a track does.

    Attributes
    ----------
    id : str
        The YouTube video ID for the track
    name : str
        The name of the track
    href : str
        The music.youtbe URL which is the link to the ytmusic page
        for the track
    uri : str
        The YTMusic uri for the track
    artists : List[Artist]
        A list of Artist objects representing the artists for a track
    url: str
        The audio playback url for the track
    images List[Image]
        A list of images for the cover art of the track
    """

    __slots__ = [
        'id',
        'href',
        'uri',
        'name',
        'artists_',
        'images',
        'duration_',
        'url_',
        'recs_'
    ]

    def __init__(self, data: Union[Dict, str]) -> None:

        if isinstance(data, str):
            data = YTMUSIC.get_song(data)

        # print(data.keys())
        # print(data)

        self.id: str = data.get('videoId', data.get('resourceId', {}).get(  # pylint: disable=invalid-name
            'videoId', str()))
        self.href: str = f'https://music.youtube.com/watch?v={self.id}'
        self.uri: str = f'ytmusic:video:{self.id}'
        self.name: str = data.get('title')

        self.artists_: Union[List[Dict[str, str]], str] = data.get(
            'artists', data.get('channelId'))

        self.images: List[Dict[str, str]] = [
            Image(**image)
            for image in data.get(
                'thumbnails',
                data.get('thumbnail') if not 'thumbnails' in data.get('thumbnail', {})
                else data.get('thumbnail', {}).get('thumbnails', [])
            )
        ]

        self.duration_: Union[int, None] = data.get('duration_seconds')

        self.url_: str = str()
        self.recs_: List[Dict[str, Any]] = []

    def __repr__(self) -> str:
        return f"<melo.Video - {(self.name or self.id or self.uri)!r}>"

    def __str__(self) -> str:
        return str(self.id)

    @property
    def artists(self) -> List[Artist]:
        '''Get a list of artist for the track or video'''
        from .user import User

        if isinstance(self.artists_, str):
            self.artists_ = [YTMUSIC.get_artist(self.artists_)]

        for idx, artist in enumerate(self.artists_):
            if not (isinstance(artist, (Artist, User))):
                # print(artist)
                self.artists_[idx] = Artist(artist.get(
                    'id', artist.get('browseId', artist.get('channelId'))))
        return self.artists_

    @property
    def url(self) -> str:
        '''Get the playback URL for a track or video

        retrieves the higest quality adaptive track by default
        '''
        print(self.url_)
        if self.url_:
            return self.url_
        print(':::fetching new url')
        
        innertube = InnerTube()
        video_info = innertube.player(self.id)
        self.url_ = video_info['streamingData']['adaptiveFormats'][-1]['url']

        return self.url_

    @property
    def duration(self):
        if self.duration_:
            return self.duration_

        video_info = YTMUSIC.get_song(self.id)['videoDetails']
        duration = video_info.get('lengthSeconds')
        self.duration_ = duration
        return self.duration_

    def get_recommendations(
        self,
        limit: Optional[int] = 10
    ) -> List["Video"]:
        '''Get recommendations for a track or video'''
        if not self.recs_ or len(self.recs_) > limit:
            self.recs_.extend(YTMUSIC.get_watch_playlist(
                self.id, f'RDAMVM{self.id}')['tracks'])

        recs: List[Dict[str, Any]] = self.recs_[: limit]
        del self.recs_[: limit]
        return [Video(data=video) for video in recs]
