from typing import Dict, List, Union
from typing_extensions import Self

from ...models import ytmusic  # pylint: disable=unused-import
from ...utils import YT, YTMUSIC, Image, URIBase


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
            return super().__new__(cls)  # pylint: disable=lost-exception

    def __init__(self, data: Union[Dict, str]) -> None:
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
        self._all_videos = []
        self._albums = self._data.get('albums', {}).get('results', [])
        self._all_albums = []  # fill this later in get_all_albums method to avoid api calls in init

        self._related_artists = data.get('related', {}).get('results', [])
        self.params = self._data.get('singles', {}).get('params', str())
        self.images = [
            Image(**image) for image in self._data.get('thumbnails', [])
        ]

    def __repr__(self) -> str:
        return f"<melo.Artist - {(self.name or self.id or self.uri)!r}>"

    @property
    def singles(self) -> List["ytmusic.Album"]:
        '''get list of artist singles'''
        from .album import Album
        for idx, single in enumerate(self._singles):
            if not isinstance(single, Album):
                single = Album(single)
                self._singles[idx] = single
        return self._singles
        # return [Album(data=single) for single in self._singles]

    @property
    def videos(self) -> List["ytmusic.Video"]:
        from .video import Video
        for idx, video in enumerate(self._videos):
            if not isinstance(video, Video):
                video = Video(video)
                self._videos[idx] = video
        return self._videos

    def get_all_videos(self) -> List["ytmusic.Video"]:
        '''Get all videos for an artist
        
        Might take extermely long in case an artist's channel has a lot of vidoes
        '''
        from .video import Video

        data = {'nextPageToken': '<placeholder>'}
        uploads_id = 'UU' + self.id[2:]

        while data.get('nextPageToken'):
            if data['nextPageToken'] == '<placeholder>':
                data = YT.get_playlist_items(
                    playlist_id=uploads_id, return_json=True)
            else:
                data = YT.get_playlist_items(
                    playlist_id=uploads_id, page_token=data['nextPageToken'], return_json=True)
            # print(data['items'][0]['snippet']['thumbnails'])
            for item in data['items']:
                item['snippet']['thumbnails'] = list(item['snippet']['thumbnails'].values())
            self._all_videos += [
                Video(video['snippet'])
                for video in data['items']
            ]
        return self._all_videos

    @property
    def albums(self) -> List["ytmusic.Album"]:
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

        for idx, album in enumerate(self._albums):
            if not isinstance(album, Album):
                album = Album(album)
                self._albums[idx] = album
        return self._albums
        # return [Album(data=album) for album in self._albums[offset: offset + limit]]

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

        if not self._all_albums:
            self._all_albums = YTMUSIC.get_artist_albums(
                channelId=self.id,
                params=self.params
            )

        for idx, album in enumerate(self._all_albums):
            if not isinstance(album, Album):
                album = Album(album)
                self._all_albums[idx] = album
        return self._all_albums
        # return [Album(album) for album in self._albums]

    @property
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

        for idx, song in enumerate(self._songs):
            if not isinstance(song, Track):
                song = Track(song)
                self._songs[idx] = song
        return self._songs
        # return [Track(track) for track in self._songs]

    @property
    def related_artists(self) -> List["Artist"]:
        '''Get a list of similar artist based on a given artist.

        Parameters
        ----------
        this method takes no parameters.

        Returns
        -------
        artists : List[Artist]
            A list of similar artists.
        '''

        for idx, artist in enumerate(self._related_artists):
            if not isinstance(artist, Artist):
                artist = Artist(artist)
                self._related_artists[idx] = artist
        return self._related_artists

        # return [
        #     Artist(artist['browseId'])
        #     for artist in self._data.get('related', {}).get('results', list())
        # ]
