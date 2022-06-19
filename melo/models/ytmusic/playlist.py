from ast import Dict
from typing import List, Optional, Union

from .artist import Artist
from .user import User

from ...utils import YTMUSIC, Image, URIBase
from .track import Track


class Playlist(URIBase):
    '''A YTMusic Playlist object'''

    __slots__ = [
        "_data",
        "id",
        "name",
        "href",
        "uri",
        "description",
        "_author",
        "track_count",
        "_tracks",
        "suggestions_token",
        "images"
    ]

    def __init__(self, data: Union[Dict, str], **kwargs) -> None:

        if isinstance(data, str):
            data = YTMUSIC.get_playlist(data)
        if 'tracks' not in data:
            data = YTMUSIC.get_playlist(data.get('browseId', data.get('playlistId')))

        self._data = data
        self.id = data.get('browseId', str())  # pylint: disable=invalid-name
        self.name = data.get('title', str())
        self.href = f'https://music.youtube.com/playlist?list={self.id}'
        self.uri = f'ytmusic:playlist:{self.id}'
        self.description = data.get('description', str())
        self._author = data.get('author', {}).get('id')
        self.track_count = data.get('trackCount', int())
        self._tracks = data.get('tracks', [])
        self.suggestions_token = data.get('suggestions_token', str())
        self.images = [
            Image(**image) for image in data.get('thumbnails', [])
        ]

    def __repr__(self) -> str:
        return f"melo.Playlist - {(self.name or self.id or self.uri)!r}"

    def __str__(self) -> str:
        return str(self.id)

    @property
    def author(self) -> Artist:
        '''Property getter for the author of a playlist'''
        if isinstance(self._author, Artist) or isinstance(self._author, User):
            return self._author

        self._author = Artist(self._author)

    def get_tracks(
        self,
        limit: Optional[int] = 8,
        offset: Optional[int] = 0
    ) -> List[Track]:
        '''Get specific tracks from a playlist based on limit and offset

        Parameters
        ----------
        limit : int
            The maximum number of tracks to return. Default is 8. Minimum is 1. Maximum is 50.
        offset : int
            The offset to start returning tracks from

        Returns
        -------
        tracks : List[Tracks]
            The tracks from the playlist
        '''

        return list(map(lambda track: track if isinstance(track, Track) else Track(track_id=track.get('videoId', str())), self._tracks[offset: offset + limit]))

    def get_all_tracks(self) -> List[Track]:
        '''Get all the tracks from a playlist

        Parameters
        ----------
        this methods takes no parameters

        Returns
        -------
        tracks : List[Tracks]
            A list of all the tracks from the given playlist
        '''

        return list(map(lambda track: track if isinstance(track, Track) else Track(track_id=track.get('videoId', str())), self._tracks))
