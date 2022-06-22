from typing import Dict, List, Optional, Union
from typing_extensions import Self

from ...models import ytmusic  # pylint: disable=unused-import
from ...utils import YTMUSIC, Image, URIBase


class Artist(URIBase):
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
        "href",
        "uri",
        "_singles",
        "_albums",
        "_songs",
        "_videos",
        "images"
    ]

    data: Union[Dict, str] = str()

    def __new__(cls: Self, data: Union[Dict, str]) -> Union[Self, "ytmusic.User"]:
        from .user import User
        try:
            if 'songs' not in data:
                # TODO - can handle browseId data for simple constructor, implement properties
                artist_id = data.get('channelId', data.get(
                    'id', data.get('browseId')))
            else:
                artist_id = data
            cls.data = YTMUSIC.get_artist(artist_id)
            return super().__new__(cls)
        except (KeyError, ValueError):
            return User(data)
        finally:
            return super().__new__(cls)  #pylint: disable=lost-exception

    def __init__(self, data: Union[Dict, str]) -> None:
        # self._data: Union[str, dict] = str()
        # if (len(args) > 0 and isinstance(args[0], dict)) or 'data' in kwargs:
        #     self._data = kwargs['data'] if 'data' in kwargs else args[0]
        #     if 'songs' not in self._data:
        #         if 'browseId' in self._data:
        #             self._data = YTMUSIC.get_artist(self._data.get('browseId'))
        #         else:
        #             self._data = YTMUSIC.get_user(self._data.get('id'))
        # elif (len(args) > 0 and isinstance(args[0], str)) or 'artist_id' in kwargs:
        #     _id = kwargs['artist_id'] if 'artist_id' in kwargs else args[0]
        #     self._data = YTMUSIC.get_artist(_id)

        if self.data:
            self._data = self.data
        else:
            self._data = data

        # super().__init__(data=self._data)

        self.id = self._data.get(  # pylint: disable=invalid-name
            'channelId', str())
        self.name = self._data.get('name', str())
        self.href = f'https://music.youtube.com/channel/{self.id}'
        self.uri = f'ytmusic:artist:{self.id}'

        self._singles = self._data.get('singles', {}).get('results', [])
        self._songs = self._data.get('songs', {}).get('results', {})
        self._videos = self._data.get('videos', {}).get('results', {})

        self._albums = self._data.get('albums', {}).get('results', [])
        # self._all_albums = YTMUSIC.get_artist_albums(
        #     channelId=self._data.get('albums', {}).get('channelId', None),
        #     params=self._data.get('albums', {}).get('params', None)
        # )
        self._albums.extend(self._singles)

        self.params = self._data.get('singles', {}).get('params', str())
        self.images = [
            Image(**image) for image in self._data.get('thumbnails', [])
        ]

    def __repr__(self) -> str:
        return f"<melo.Artist - {(self.name or self.id or self.uri)!r}>"

    def get_singles(self):
        '''get list of artist singles'''
        from .album import Album
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
            Artist(artist['browseId'])
            for artist in self._data.get('related', {}).get('results', list())
        ]
