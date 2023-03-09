import datetime
from typing import List, Optional

from melodine.configs import SPOTIFY, YTMUSIC
from melodine.innertube import InnerTube
from melodine.models.spotify.artist import Artist
from melodine.models.spotify.episode import Episode
from melodine.utils import Image, URIBase
from melodine.models.base.track import TrackBase


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
        "images",
        "explicit"
    ]

    def __new__(cls, data, **kwargs):
        # for some cases when a result contains an episode
        if data.get('episode'):
            return Episode(data)
        return super().__new__(cls)

    def __init__(self, data, **kwargs) -> None:
        from melodine.models.spotify.album import Album

        self.artists = list(
            Artist(_artist) for _artist in data.get('artists', [])
        )

        self.album = Album(
            data.get('album', {})
        ) if 'album' in data else kwargs.get('album', {})

        self.id = data.get('id', None)  # pylint: disable=invalid-name
        self.name = data.get('name', None)
        self.uri = data.get('uri', None)
        self.href = 'https://open.spotify.com/track/' + self.id
        self.duration = int(data.get('duration_ms') / 1000)
        self.explicit = data.get('explicit', False)
        self.url_ = []

        if 'images' in data:
            self.images = [
                Image(**image) for image in data.get('images', [])
            ]
        else:
            self.images = self.album.images.copy()

        self._audio_analysis = {}
        self._audio_features = {}

    def __repr__(self) -> str:
        return f"<melo.Track - {(self.name or self.id or self.uri)!r}>"

    def test_run():  # pylint: disable=no-method-argument
        return Track(SPOTIFY.search('ritchrd - paris', type='track')['tracks']['items'][0])

    @property
    def url(self):
        '''porperty getter for the Track URL'''

        if self.url_:
            return self.url_

        video_id = YTMUSIC.search(
            f"{self.artists[0].name} - {self.name}", filter='songs')[0]['videoId']

        # for ID of the top search results which could be a video (that's not implemented yet)
        # video_id = YTMUSIC.search(f"{self.artists[0].name} - {self.name}")[0]['videoId']

        video_info = InnerTube().player(video_id)

        # self.url_ = video_info['streamingData']['adaptiveFormats'][-1]['url']
        self.url_ = video_info['streamingData']['formats'][-1]['url']

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

    def audio_analysis(self):
        '''get audio analysis for a track based on spotify community's listening patterns'''
        if self._audio_analysis:
            return self._audio_analysis

        self._audio_analysis = SPOTIFY.audio_analysis(self.id)
        return self._audio_analysis

    def audio_features(self):
        '''get audio features for a track based on spotify community's listening patterns'''
        if self._audio_features:
            return self._audio_features

        self._audio_analysis = SPOTIFY.audio_features(self.id)
        return self.audio_features

    def add_to_playlist(self, playlist_id) -> None:
        '''Add the track to a spotify playlist'''
        SPOTIFY.playlist_add_items(
            playlist_id=playlist_id,
            items=[self.id]
        )

        # def is_saved(self) -> bool:
        #     return SPOTIFY.current_user_saved_tracks_contains([self.id])[0]

        # def save_track(self) -> None:
        #     return SPOTIFY.current_user_saved_tracks_add([self.id])

        # def unsave_track(self) -> None:
        #     return SPOTIFY.current_user_saved_tracks_delete([self.id])


class PlaylistTrack(Track):
    '''A playlist track.

    same as a normal track, but with some extra attributes
    '''
    __slots__ = ['added_by', 'added_at']

    def __init__(self, data, **kwargs) -> None:
        from melodine.models.spotify.client import Client
        from melodine.models.spotify.user import User

        super().__init__(data['track'])

        self.added_by = User(data.get('added_by')) if not isinstance(
            data.get('added_by'), (Client, User)) else data.get('added_by')
        self.added_at = datetime.datetime.strptime(
            data["added_at"], "%Y-%m-%dT%H:%M:%SZ"
        )

    def __repr__(self):
        return f"<spotify.PlaylistTrack: {self.name!r}>"
