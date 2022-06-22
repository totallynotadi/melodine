from typing import List, Optional

from ...utils import YTMUSIC, Image, URIBase
from .artist import Artist
from .track import Track


class Album(URIBase):
    """A YTMusic Album object

    Attributes
    ----------
    id: str
        the YTMusic id for the album
    name: str
        the name of the album
    type: str
        Type of the album. one of "single" or "album"
    artist: List[str]
        A list of Artist objects representing the artists for an album
    tracks: List[str]
        A list of first 5 tracks of an album
    total_tracks: int
        the number of tacks in an album
    duration: int
        the total duration of the album in seconds
    images: List[Image]
        A list of images for the album cover art

    Methods
    -------
    get_tracks(limit=5, offset=0) -> List[Tracks]
        returns a list of Tracks from the album based on the limit and offset

    get_all_tracks() -> List[Tracks]
        returns a list of all the tracks form the album at once
    """

    __slots__ = [
        "_data",
        "_artists",
        "_tracks",
        "id",
        "href",
        "uri",
        "name",
        "type",
        "total_tracks",
        "duration",
        "images"
    ]

    def __init__(self, *args, **kwargs) -> None:
        if (len(args) > 0 and isinstance(args[0], dict)) or 'data' in kwargs:
            data = kwargs['data'] if 'data' in kwargs else args[0]
            if 'tracks' not in data:
                data = YTMUSIC.get_album(
                    data['browseId']
                ) if 'browseId' in data else YTMUSIC.get_album(
                    data['audioPlaylistId']
                )
        elif (len(args) > 0 and isinstance(args[0], str)) or 'album_id' in kwargs:
            _id = kwargs['album_id'] if 'album_id' in kwargs else args[0]
            data = YTMUSIC.get_album(_id)

        self._data = data

        self._artists = []
        # list of unconstructed track object dictionaries, will construct in another method
        self._tracks = data.get('tracks')

        if 'browseId' not in data:
            self.id = YTMUSIC.get_album_browse_id(  # pylint: disable=invalid-name
                data['audioPlaylistId'])
        else:
            self.id = data['browseId']  # pylint: disable=invalid-name
        self.name = data.get('title', str())
        self.href = f'https://music.youtube.com/playlist?list={self.id}'
        self.uri = f'ytmusic:album:{self.id}'
        self.type = data.get('type', str())
        self.total_tracks = data.get('trackCount', 0)
        self.duration = (data.get("duration"), data.get("duration_seconds"))

        self.images = list(
            Image(**image) for image in data.get('thumbnails', [])
        )

    def __repr__(self) -> str:
        return f"melo.Album - {(self.name or self.id or self.uri)!r}"

    def __str__(self) -> str:
        return str(self.id)

    @property
    def tracks(self) -> List[Track]:
        '''A property getter to get first few tracks of an album'''
        return self.get_tracks()

    @property
    def artists(self) -> List["Album"]:
        '''A list of all the artists from an album'''
        if not self._artists:
            self._artists = [Artist(artist['id'])
                             for artist in self._data.get('artists', [])]
        return self._artists

    def get_tracks(
        self,
        *,
        limit: Optional[int] = 5,
        offset: Optional[int] = 0
    ) -> List[Track]:
        """gets specific tracks based on limit and offset

        Parameters
        ----------
        limit: Optional[int]
            the limit for how many tracks to retrieve for the album (default is 5).
        offset: Optional[int]
            the offset the api should start from in the tracks

        Returns
        -------
        tracks: List[Track]
            A list of tracks retrieved from the album
        """
        return list(map(
            lambda track: Track(track.get(
                'videoId', str()), album=self._data)
            if not isinstance(track, Track) else track, self._tracks[offset: offset + limit]
        ))

    def get_all_tracks(self):
        '''get all tracks for the album

        Parameters
        ----------
        this methods takes no parameters

        Returns
        -------
        tracks: List[Track]
            A list of all the tracks from the album
        '''
        return list(map(
            lambda track: Track(track.get(
                'videoId', str()), album=self._data)
            if not isinstance(track, Track) else track, self._tracks
        ))
