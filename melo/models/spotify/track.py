import datetime
from typing import List, Optional

from ...innertube import InnerTube
from ...utils import SPOTIFY, YTMUSIC, Image, URIBase
from .artist import Artist


class Track(URIBase):
    '''A Spotify Track Object

    Attributes
    ---------
    id: str
        The Spotify ID for the Track
    '''

    __slots__ = [
        "artists",
        "album",
        "id",
        "name",
        "uri",
        "href",
        "duration",
        "url_",
        "images"
    ]

    def __init__(self, data, **kwargs) -> None:
        from .album import Album

        self.artists = list(
            Artist(_artist) for _artist in data.get('artists', [])
        )

        self.album = Album(data.get('album', {})) if 'album' in data else kwargs.get('album', {})

        self.id = data.get('id', None) #pylint: disable=invalid-name
        self.name = data.get('name', None)
        self.uri = data.get('uri', None)
        self.href = 'https://open.spotify.com/track/' + self.id
        self.duration = data.get('duration_ms') * 1000
        self.url_ = []
        
        if 'images' in data:
            self.images = [
                Image(**_image) for _image in data.get('images', [])
            ]
        else:
            self.images = self.album.images.copy()

    def __repr__(self) -> str:
        return f"melo.Trackt - {(self.name or self.id or self.uri)!r}"

    def __str__(self) -> str:
        return str(self.id)

    def test_run(): #pylint: disable=no-method-argument
        return Track(SPOTIFY.search('ritchrd - paris', type='track')['tracks']['items'][0])

    @property
    def url(self):
        '''porperty getter for the Track URL'''

        if self.url_:
            return self.url_

        video_id = YTMUSIC.search(f"{self.artists[0].name} - {self.name}", filter='songs')[0]['videoId']

        # for ID of the top search results which could be a video (that's not implemented yet)
        # video_id = YTMUSIC.search(f"{self.artists[0].name} - {self.name}")[0]['videoId']

        innertube = InnerTube()
        video_info = innertube.player(video_id)
        self.url_ = video_info['streamingData']['adaptiveFormats'][-1]['url']

        return self.url_

    def cache_url(self) -> None:
        '''just a dummy call to trigger the url fetching'''
        if not self.url:
            self.url = self.url

    def get_recommendations(
        self,
        limit: Optional[int] = 1
    ) -> List["Track"]:

        ''' get recommendation for a particular track
        
        Returns one Track per call, use the limit parameter to change number of returned tracks.

        Parameters
        ----------
        limit: int
            The number of suggestions to returns

        Returns
        -------
        results: List[Tracks]
            A list of suggested tracks
        '''
        recs = SPOTIFY.recommendations(seed_tracks=[self.id], limit=limit)

        return [Track(rec) for rec in recs['tracks']]


class PlaylistTrack(Track):
    '''A playlist track.
    
    same as a normal track, but with some extra attributes
    '''
    __slots__ = ['added_by', 'added_at']

    def __init__(self, data, **kwargs) -> None:
        
        super().__init__(data['tracks'])

        #TODO - get adding user as an User object
        self.added_by = data.get('added_by')
        self.added_at = datetime.datetime.strptime(
            data["added_at"], "%Y-%m-%dT%H:%M:%SZ"
        )

    def __repr__(self):
        return f"<spotify.PlaylistTrack: {self.name!r}>"
