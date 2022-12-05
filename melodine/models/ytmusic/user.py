"""
only playlists and some videos have users.

videos might belong to either artists or users. so a try-catch here too.
albeit, the try-catch wrapped api call needs to be only for the data attr (only when it's needed).
"""

from typing import Dict, List

from melodine.utils import URIBase
from melodine.configs import YTMUSIC, YT
from melodine.models import ytmusic
from melodine.models.ytmusic import Video


class User(URIBase):

    __slots__ = (
        '_data',
        'id',
        '_name',
        'href',
        'uri',
        '_videos',
        '_playlists',

        '_total_playlists',
        '_total_uploads',
        '__next_page_token',
        '__prev_page_token'
    )

    def __init__(self, data: Dict, **kwargs) -> None:
        self._data = None

        self.id: str = data.get('id', kwargs.get('id', None))
        self.uploads_id: str = 'UU' + self.id[2:]
        self._name: str = data.get('name', None)
        self.href: str = "https://music.youtube.com/channel/" + \
            str(self.id or '')
        self.uri: str = "ytmusic:user:" + str(self.id or '')

        self._videos: List[Dict] = data.get('videos', {}).get('results')
        self._playlists: List[Dict] = data.get('playlists', {}).get('results')

        self._total_playlists = int()  # aka 0
        self._total_uploads = int()
        self.__next_page_token = None
        self.__prev_page_token = None

    def _get_data(self) -> None:
        self._data = YTMUSIC.get_user(self.id)

    @classmethod
    def from_id(cls, data: Dict) -> "User":
        return cls(data={'id': data})

    @property
    def total_uploads(self) -> int:
        '''total number of track uploaded by the user'''
        if self._total_uploads:
            return self._total_uploads

        self._total_uploads = YT.get_playlist_items(
            playlist_id=self.uploads_id,
            limit=1,
            return_json=True
        )['pageInfo']['totalResults']
        return self._total_uploads

    @property
    def total_playlists(self) -> int:
        '''total number of playlists from the user'''
        if self._total_playlists:
            return self._total_playlists

        self._total_playlists = YT.get_playlists(
            channel_id=self.id,
            limit=1,
            return_json=True
        )['pageInfo']['totalResults']
        return self._total_playlists

    @property
    def name(self) -> str:
        if self._name is None:
            if self._data is None:
                self._get_data()
            self._name = self._data['name']
        return self._name

    @property
    def videos(self) -> List[Video]:
        if len(self._videos) == 0:
            if self._data is None:
                self._get_data()
            self._videos = self._data['videos']['results']
        for idx, video in enumerate(self._videos.copy()):
            if not isinstance(video, Video):
                video = Video(video)
                self._videos.insert(idx, video)
                del self._videos[idx + 1]
        return self._videos

    def get_videos(
        self,
        limit: int = 10,
        reset=False
    ) -> List[Video]:
        '''Get a list of Videos from a User'''
        results = []
        data = {
            'nextPageToken': (
                '<placeholder>'
                if not self.__prev_page_token else self.__next_page_token
            )
        }

        if data.get('nextPageToken'):
            if data['nextPageToken'] == '<placeholder>' or reset:
                data = YT.get_playlist_items(
                    playlist_id=self.uploads_id,
                    limit=limit,
                    return_json=True
                )
            else:
                data = YT.get_playlist_items(
                    playlist_id=self.uploads_id,
                    page_token=data['nextPagetoken'],
                    limit=limit,
                    return_json=True
                )

            self.__next_page_token = data['nextPageToken']
            self.__prev_page_token = data['prevPageToken']

            _results = [Video(video['snippet']) for video in data['items']]
            results += _results
            return _results

    def get_all_videos(self) -> List[Video]:
        '''gets a list of all videos uploaded by a user.

        Might take extremely long time based on the number of videos an artist has.
        (some channels end up having over 100 uploads)

        Use :func:`get_videos` for paged results instead
        '''
        if len(self._videos) == self.total_uploads:
            return self.videos

        count = 0
        data = {}

        self._videos = []
        while count < self.total_uploads:
            if data:
                data = YT.get_playlist_items(
                    playlist_id=self.uploads_id, page_token=data['nextPageToken'], return_json=True)
            else:
                data = YT.get_playlist_items(
                    playlist_id=self.uploads_id, return_json=True)
            self._videos += [
                Video(video['snippet'])
                for video in data['items']
            ]
            count += len(data['items'])
        return self._videos

    @property
    def playlists(self) -> List["ytmusic.Playlist"]:
        from .playlist import Playlist

        if len(self._playlists) == 0:
            if self._data is None:
                self._get_data()
            self._playlists = self._data['playlists']['results']
        for idx, playlist in enumerate(self._playlists.copy()):
            if not isinstance(playlist, Playlist):
                playlist = Playlist(playlist)
                self._playlists.insert(idx, playlist)
                del self._playlists[idx + 1]
        return self._playlists

    def get_all_playlists(self) -> List["ytmusic.Playlist"]:
        '''Get a list of all Playlists from a User'''
        from .playlist import Playlist

        data = {'nextPageToken': '<placeholder>'}

        self._playlists = []
        while data.get('nextPageToken'):
            if not data:
                data = YT.get_playlists(
                    channel_id=self.id,
                    limit=5,
                    return_json=True
                )
            else:
                data = YT.get_playlists(
                    channel_id=self.id,
                    limit=5,
                    page_token=data['nextPageToken'],
                    return_json=True
                )

            self._playlists += [
                Playlist(playlist['id'])
                for playlist in data['items']
            ]
        return self._playlists
