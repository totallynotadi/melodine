from typing import Dict, List, Optional, Union

from ...utils import YTMUSIC, Image, URIBase
from .artist import Artist
from .track import Track
from .user import User


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
            self.explicit = data.get('isExplicit', False)
            data = YTMUSIC.get_playlist(data.get('browseId', data.get('playlistId')))

        self._data = data
        self.id = data.get('browseId', str())  # pylint: disable=invalid-name
        self.name = data.get('title', str())
        self.href = f'https://music.youtube.com/playlist?list={self.id}'
        self.uri = f'ytmusic:playlist:{self.id}'
        self.description = data.get('description', str())
        # self._author = data.get('author', {}).get('id')
        self._owner = data.get('author', {}).get('id')
        self.track_count = data.get('trackCount', int())
        self._tracks = data.get('tracks', [])
        self.suggestions_token = data.get('suggestions_token', str())
        self.images = [
            Image(**image) for image in data.get('thumbnails', [])
        ]

    def __repr__(self) -> str:
        return f"<melo.Playlist - {(self.name or self.id or self.uri)!r}>"

    def __str__(self) -> str:
        return str(self.id)

    @property
    def owner(self) -> Union[Artist, User]:
        '''Property getter for the author of a playlist'''
        if isinstance(self._owner, (Artist, User)):
            return self._owner

        self._owner = Artist(self._owner)

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
        for idx, track in enumerate(self._tracks[offset : offset + limit]):
            if not isinstance(track, Track):
                track = Track(track)
                self._tracks[idx] = track
        return self._tracks           
        # return list(Track(track.get('videoId', str())) for track in self._tracks[offset: offset + limit])

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

        for idx, track in enumerate(self._tracks):
            if not isinstance(track, Track) and track.get('videoId') is not None:
                track = Track(track.get('videoId'))
                self._tracks[idx] = track
        return self._tracks 
        # return list(Track(track.get('videoId', str())) for track in self._tracks)
