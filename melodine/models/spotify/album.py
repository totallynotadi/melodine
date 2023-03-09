from typing import List, Optional

from melodine.utils import Image, URIBase
from melodine.configs import SPOTIFY
from melodine.models.spotify.artist import Artist
from melodine.models.spotify.track import Track
from melodine.models.base.album import AlbumBase


class Album(URIBase):
    '''
    id - spotify id for the album
    name - the name of the album
    artists - a list containing a artist object of all the artists from a album
    tracks - a list containing track objects for all the tracks in a album
    type - the type of album (a full album, or a single or smthng)
    '''

    __slots__ = (
        "_data",
        "_tracks",
        "artists",
        "images",
        "href",
        "name",
        "type",
        "data",
        'year',
        "uri",
        "id",
    )

    def __init__(self, data):

        self._data = data
        self.id = data.get('id', None)  # pylint: disable=invalid-name
        self.name = data.get('name')
        self.href = data.get('external_urls').get('spotify', None)
        self.uri = data.get('uri', None)

        self.year = data.get('release_date').split('-')[0]
        self.type = data.get('album_type', None)
        self.images = [Image(**image) for image in data.get('images', [])]

        self.artists = [Artist(artist) for artist in data.get('artists')]
        self._track_count = data.get('total_tracks', 0)
        self._tracks = []

    def __repr__(self) -> str:
        return f"melo.Album - {(self.name or self.id or self.uri)!r}"

    @property
    def total_tracks(self) -> int:
        '''get all the tracks from an album'''

        if not self._total_tracks:
            self._total_tracks = SPOTIFY.album_tracks(self.id, limit=1)[
                'total']
        return self._total_tracks

    @property
    def tracks(self):
        '''get all the tracks from the album'''
        offset = 0

        while len(self._tracks) < self.total_tracks:
            data = SPOTIFY.album_tracks(self.id, limit=50, offset=offset)
            offset += 50
            self._tracks += list(Track(track, album=self._data)
                                 for track in data['items'])
        return self._tracks

    def get_tracks(self, limit: Optional[int] = 20, offset: Optional[int] = 0) -> List[Track]:
        '''get specific tracks from an album based on the limit and offsets'''
        if len(self._tracks) == 0:
            data = SPOTIFY.album_tracks(self.id, limit=limit, offset=offset)
            for track in data['items']:
                track['album'] = self._data
            self._tracks = list(Track(_track) for _track in data['items'])
        return self._tracks

    # @cached_property
    # def get_all_tracks(self) -> List[Track]:
    #     '''get all tracks of an album'''
    #     offset = 0

    #     while len(self.tracks) < self.total_tracks:
    #         data = SPOTIFY.album_tracks(self.id, limit=50, offset=offset)
    #         offset += 50
    #         self.tracks += list(Track(track, album=self._data) for track in data['items'])
    #     return self.tracks

    # def saved(self) -> bool:
    #     ''' Check if one or more albums is already saved in
    #         the current Spotify user’s “Your Music” library.
    #     '''
    #     return SPOTIFY.current_user_saved_albums_contains([self.id])[0]

    # def save_album(self) -> None:
    #     '''Add one or more albums to the current user's
    #         "Your Music" library.
    #     '''
    #     return SPOTIFY.current_user_saved_albums_add([self.id])

    # def unsave_album(self):
    #     return SPOTIFY.current_user_saved_albums_delete([self.id])
