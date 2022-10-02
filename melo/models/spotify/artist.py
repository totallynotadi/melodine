from typing import Dict, List, Literal, Optional

from melo.utils import Image, URIBase
from melo.configs import SPOTIFY


class Artist(URIBase):
    '''
    Attributes
    ----------
        id: `str`
            spotify id for the album

        name: `str`
            name of the artist

        genres: `List[str]`
            a list of all the genres from an artist

        albums: `List[Album]`
            a list of all the albums from an artist

    methods
    -------
        artist_top_tracks: `List[Track]`
            a list of top tracks (a list containing track objects for the top tracks)
    '''

    __slots__ = (
        "followers",
        "genres",
        "images",
        "name",
        "href",
        "id",
        "uri",
        "_albums",
    )

    def __init__(self, data: Dict):
        self.id = data.get('id')  # pylint: disable=invalid-name
        self.uri = data.get('uri', None)
        self.href = data.get('external_urls').get('spotify', None)
        self.name = data.get('name', None)
        self.genres = data.get('genres', None)
        self.followers = data.get('followers', {}).get('total', None)
        self.images = [
            Image(**image)
            for image in data.get('images', [])
        ]

        self._albums = list()

    def __repr__(self) -> str:
        return f"melo.Artist - {(self.name or self.id or self.uri)!r}"

    @property
    def albums(self):
        if not self._albums:
            self.get_albums()
        return self._albums

    @property
    def total_albums(self):
        return SPOTIFY.artist_albums(self.id, limit=1)['total']

    def get_albums(
        self,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        album_type: Literal['album', 'single',
                            'appears_on', 'compilation'] = 'album'
    ) -> List:
        from .album import Album
        
        if len(self._albums) == 0:
            data = SPOTIFY.artist_albums(
                self.id, limit=limit, offset=offset, album_type=album_type)
            self._albums = list(Album(album) for album in data['items'])
        return self._albums

    def get_all_albums(self):
        from .album import Album

        offset = 0

        while len(self._albums) < self.total_albums:
            data = SPOTIFY.artist_albums(self.id, limit=50)

            offset += 50
            self._albums.extend(list(Album(album) for album in data['items']))
        return list(set(self._albums))

    def artist_top_tracks(self):
        from .track import Track

        top = SPOTIFY.artist_top_tracks(self.id)
        return list(Track(track) for track in top['tracks'])

    def get_related_artists(self):
        related = SPOTIFY.artist_related_artists(self.id)
        return list(Artist(artist) for artist in related['artists'])

    def is_followed(self) -> bool:
        return SPOTIFY.current_user_following_artists([self.id])

    def follow_artist(self) -> None:
        return SPOTIFY.user_follow_artists([self.id])

    def unfollow_artist(self) -> None:
        return SPOTIFY.user_unfollow_artists([self.id])
