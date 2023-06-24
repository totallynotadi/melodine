from typing import List

from melodine.utils import Image
from melodine.base.misc import URIBase

from melodine.services import service
from melodine.spotify.artist import Artist
from melodine.spotify.track import Track
from melodine.base.album import AlbumBase


class Album(URIBase):
    """
    Model for Spotify Album response

    Attributes
    ----------
    `:attr:id` - spotify id for the album

    `:attr:name` - the name of the album

    `:attr:artists` - a list containing a `Artist` objects of all the artists from this album

    `:attr:tracks` - a list containing `Track` objects for all the tracks in a album

    `:attr:type` - the type of album, either one of `album,  single or collection`
    """

    __slots__ = (
        "_data",
        "_tracks",
        "artists",
        "images",
        "href",
        "name",
        "type",
        "data",
        "year",
        "uri",
        "id",
    )

    def __init__(self, data):
        self._data = data
        self.id = data.get("id", None)  # pylint: disable=invalid-name
        self.name = data.get("name")
        self.href = data.get("external_urls").get("spotify", None)
        self.uri = data.get("uri", None)

        self.year = data.get("release_date").split("-")[0]
        self.type = data.get("album_type", None)
        self.images = [Image(**image) for image in data.get("images", [])]

        self.artists = [Artist(artist) for artist in data.get("artists")]
        self._total_tracks = data.get("total_tracks", 0)
        self._tracks = []

    def __repr__(self) -> str:
        return f"melo.Album - {(self.name or self.id or self.uri)!r}"

    @classmethod
    def from_id(cls, id: str) -> "Album":
        return cls(data=service.spotify.album(id))

    @property
    def total_tracks(self) -> int:
        """get all the tracks from an album"""

        if not self._total_tracks:
            self._total_tracks = service.spotify.album_tracks(self.id, limit=1)["total"]
        return self._total_tracks

    @property
    def tracks(self):
        """get all the tracks from the album"""
        offset = 0

        while len(self._tracks) < self.total_tracks:
            data = service.spotify.album_tracks(self.id, limit=50, offset=offset)
            offset += 50
            self._tracks += list(
                Track(track, album=self._data) for track in data["items"]
            )
        return self._tracks

    def get_tracks(self, limit: int = 20, offset: int = 0) -> List[Track]:
        """get specific tracks from an album based on the limit and offsets"""
        if len(self._tracks) == 0:
            data = service.spotify.album_tracks(self.id, limit=limit, offset=offset)
            for track in data["items"]:
                track["album"] = self._data
            self._tracks = list(Track(_track) for _track in data["items"])
        return self._tracks

    # @cached_property
    # def get_all_tracks(self) -> List[Track]:
    #     '''get all tracks of an album'''
    #     offset = 0

    #     while len(self.tracks) < self.total_tracks:
    #         data = service.spotify.album_tracks(self.id, limit=50, offset=offset)
    #         offset += 50
    #         self.tracks += list(Track(track, album=self._data) for track in data['items'])
    #     return self.tracks

    # def saved(self) -> bool:
    #     ''' Check if one or more albums is already saved in
    #         the current Spotify user’s “Your Music” library.
    #     '''
    #     return service.spotify.current_user_saved_albums_contains([self.id])[0]

    # def save_album(self) -> None:
    #     '''Add one or more albums to the current user's
    #         "Your Music" library.
    #     '''
    #     return service.spotify.current_user_saved_albums_add([self.id])

    # def unsave_album(self):
    #     return service.spotify.current_user_saved_albums_delete([self.id])
