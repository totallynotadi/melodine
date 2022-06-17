from typing import Any, Dict, List, Optional

from ...innertube import InnerTube
from ...utils import YTMUSIC, Image
from .artist import Artist


class Video:
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
        'duration',
        'images',
        'url_',
        'recs_'
    ]

    def __init__(self, data: Dict) -> None:
        self.id: str = data.get('videoId')  # pylint: disable=invalid-name
        self.href: str = f'https://music.youtube.com/watch?v={self.id}'
        self.uri: str = f'ytmusic:video:{self.id}'
        self.name: str = data.get('title')

        self.artists_: List[Dict[str, str]] = data.get('artists')

        self.duration: int = data.get('duration_seconds')
        self.images: List[Dict[str, str]] = [
            Image(**image) for image in data.get('thumbnails')
        ] if data.get('thumbnails') is not None else []

        self.url_: str = str()
        self.recs_: List[Dict[str, Any]] = []

    @property
    def artists(self) -> List[Artist]:
        '''Get a list of artist for the track or video'''
        for idx, artist in enumerate(self.artists_):
            if not isinstance(artist, Artist):
                self.artists_[idx] = Artist(data=artist)
        return self.artists_

    @property
    def url(self) -> str:
        '''Get the playback URL for a track or video'''
        if self.url_:
            return self.url_

        innertube = InnerTube()
        video_info = innertube.player(self.id)
        self.url_ = video_info['streamingData']['adaptiveFormats'][-1]['url']
        return self.url_

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
