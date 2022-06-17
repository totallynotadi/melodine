from typing import List, Optional

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
        "author",
        "track_count",
        "_tracks",
        "suggestions_token",
        "images"
    ]

    def __init__(self, *args, **kwargs) -> None:
        if (len(args) > 0 and isinstance(args[0], dict)) or 'data' in kwargs:
            data = kwargs['data'] if 'data' in kwargs else args[0]
            if 'tracks' not in data:
                data = YTMUSIC.get_playlist(data.get('browseId'))
        elif (len(args) > 0 and isinstance(args[0], str)) or 'playlist_id' in kwargs:
            _id = kwargs['playlist_id'] if 'playlist_id' in kwargs else args[0]
            data = YTMUSIC.get_playlist(_id)

        self._data = data
        self.id = data.get('browseId', str())  # pylint: disable=invalid-name
        self.name = data.get('title', str())
        self.href = f'https://music.youtube.com/playlist?list={self.id}'
        self.uri = f'ytmusic:playlist:{self.id}'
        self.description = data.get('description', str())
        self.author = data.get('author', str())
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
