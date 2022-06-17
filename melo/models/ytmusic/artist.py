from typing import List, Optional

from ...models import ytmusic  # pylint: disable=unused-import
from ...utils import YTMUSIC, Image


class Artist:
    """A YTMusic Artist object

    Attributes
    ----------
    id : `str`
        The YTMusic artist ID. Equivalent to the YouTube channelID
    name : `str`
        The name of the artist
    albums : `List[Albums]`
        A list of top albums from and artist
    tracks : `List[Track]`
        A list of top tarcks form the artist
    images : `List[Image]`
        A list of images for the album cover art
    """

    __slots__ = [
        "_data",
        "id",
        "name",
        "_singles",
        "_albums",
        "_songs",
        "_videos",
        "images"
    ]

    def __init__(self, *args, **kwargs) -> None:
        self._data = ''
        if (len(args) > 0 and isinstance(args[0], dict)) or 'data' in kwargs:
            self._data = kwargs['data'] if 'data' in kwargs else args[0]
        elif (len(args) > 0 and isinstance(args[0], str)) or 'artist_id' in kwargs:
            _id = kwargs['artist_id'] if 'artist_id' in kwargs else args[0]
            self._data = YTMUSIC.get_artist(_id)

        self.id = self._data.get('channelId', str())  # pylint: disable=invalid-name
        self.name = self._data.get('name', str())
        self._singles = self._data.get('singles', {}).get('results', [])
        # doesn't have the 'type' property in the album abjects
        self._albums = self._data.get('albums', {}).get('results', [])
        # self._albums = YTMUSIC.get_artist_albums(                          # has the 'type' property in the album abjects
        #     channelId=self._data.get('albums', {}).get('channelId', None), # also try 'browseId instead of channelId
        #     params=self._data.get('albums', {}).get('params', None)
        # )
        self._albums.extend(self._singles)
        self._songs = self._data.get('songs', {}).get('results', {})
        self._videos = self._data.get('videos', {}).get('results', {})
        self.images = [
            Image(**image) for image in self._data.get('thumbnails', [])
        ]

    def get_singles(self):
        '''get list of artist singles'''
        from ..ytmusic.album import Album
        return [Album(data=single) for single in self._singles]

    def get_albums(
        self,
        limit: Optional[int] = 5,
        offset: Optional[int] = 0
    ) -> List["ytmusic.Album"]:
        '''Get albums of an artist based on given limit and offset

        Parameters
        ----------
        limit : :class:`int`
            Maximum number of items to return. Default is 5. Minimum is 1. Maximum is 50.
        offset : int
            The offset to start returning tracks from. Default is 0.

        Returns
        -------
        albums : List[Album]
            The albums of the artist
        '''
        from .album import Album

        return [Album(data=album) for album in self._albums[offset: offset + limit]]

    def get_all_albums(self) -> List["ytmusic.Album"]:
        '''Fetches all the artists's albums.

        This operation might take long based on how many albums the artist has.

        Parameters
        ----------
        this method takes no parameters.

        Returns
        -------
        albums : List[Albums]
            All the albums of the artist.
        '''
        from .album import Album

        # return [Album(data=album) for album in self._albums]  # construct from data
        # construct from id
        return [Album(album_id=album['browseId']) for album in self._albums]

    def top_tracks(self) -> List["ytmusic.Track"]:
        """Gets an artist's top tracks.

        Parameters
        ----------
        this method takes no parameters.

        Returns
        -------
        tracks : List[Tracks]
            the aritst top tracks.
        """
        from .track import Track

        return [Track(track) for track in self._songs]

    def get_related_artists(self) -> List["Artist"]:
        '''Get a list of similar artist based on a given artist.

        Parameters
        ----------
        this method takes no parameters.

        Returns
        -------
        artists : List[Artist]
            A list of similar artists.
        '''
        return [
            Artist(artist_id=artist['browseId'])
            for artist in self._data.get('related', {}).get('results', list())
        ]
