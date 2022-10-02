from functools import cached_property
from typing import List, Optional

from melo.utils import Image, URIBase
from melo.configs import SPOTIFY
from melo.models.spotify.artist import Artist
from melo.models.spotify.track import Track


class Album(URIBase):
    '''
    id - spotify id for the album
    name - the name of the album
    artists - a list containing a artist object of all the artists from a album
    tracks - a list containing track objects for all the tracks in a album
    type - the type of album (a full album, or a single or smthng)
    '''

    __slots__ = (
        "_tracks",
        "artists",
        "images",
        "_data",
        "href",
        "name",
        "type",
        "data",
        "uri",
        "id",
    )

    def __init__(self, data):

        self._data = data
        self.artists = [Artist(artist) for artist in data.get('artists')]
        self.id = data.get('id', None) # pylint: disable=invalid-name
        self.uri = data.get('uri', None)
        self.href = data.get('external_urls').get('spotify', None)
        self.images = [Image(**image) for image in data.get('images', [])]
        self.name = data.get('name')
        self._tracks = []
        self.type = data.get('album_type', None)

    def __repr__(self) -> str:
        return f"melo.Album - {(self.name or self.id or self.uri)!r}"

    @property
    def tracks(self):
        '''a property getter to get top tracks from an album'''
        if len(self._tracks) == 0:
            self.get_tracks()
        return self._tracks

    @property
    def total_tracks(self) -> int:
        '''get all the tracks from an album'''
        return SPOTIFY.album_tracks(self.id, limit=1)['total']

    def get_tracks(self, limit: Optional[int] = 20, offset: Optional[int] = 0) -> List[Track]:
        '''get specific tracks from an album based on the limit and offsets'''
        if len(self._tracks) == 0:
            data = SPOTIFY.album_tracks(self.id, limit=limit, offset=offset)
            for track in data['items']:
                track['album'] = self._data
            self._tracks = list(Track(_track) for _track in data['items'])
        return self._tracks

    @cached_property
    def get_all_tracks(self) -> List[Track]:
        '''get all tracks of an album'''
        offset = 0

        while len(self.tracks) < self.total_tracks:
            data = SPOTIFY.album_tracks(self.id, limit=50, offset=offset)
            offset += 50
            self.tracks += list(Track(track, album=self._data) for track in data['items'])
        return self.tracks

    def saved(self) -> bool:
        ''' Check if one or more albums is already saved in
            the current Spotify user’s “Your Music” library.
        '''
        return SPOTIFY.current_user_saved_albums_contains([self.id])[0]

    def save_album(self) -> None:
        '''Add one or more albums to the current user's
            "Your Music" library.
        '''
        return SPOTIFY.current_user_saved_albums_add([self.id])

    def unsave_album(self):
        return SPOTIFY.current_user_saved_albums_delete([self.id])
