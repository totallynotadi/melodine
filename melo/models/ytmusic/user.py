from functools import cached_property
from typing import Dict, List, Union

from ...models import ytmusic  # pylint: disable=unused-import
from ...utils import YT, YTMUSIC, URIBase
from .video import Video


class User(URIBase):
    def __init__(self, data: Union[Dict, str]) -> None:
        if isinstance(data, str):
            data = YTMUSIC.get_user(data)

        print('got user')

        self.id: str = data.get('videos', {}).get(  # pylint: disable=invalid-name
            'browseId', str())
        self.uploads_id: str = 'UU' + self.id[2:]
        self.href: str = f'https://music.youtube.com/channel/{self.id}'
        self.uri: str = f'ytmusic:user:{self.id}'
        self.name: str = data.get('name', str())

        self._total_playlists: int = 0
        self._total_uploads: int = 0

        self._videos: List[Union[Dict, Video]] = data.get(
            'videos', {}).get('results', [])
        self._playlists: List[Union[Dict, "ytmusic.Playlist"]] = data.get(
            'playlists', {}).get('results', [])

    @property
    def total_uploads(self) -> int:
        '''total number of track uploaded by the user'''
        if self._total_uploads:
            return self._total_uploads

        self.total_uploads = YT.get_playlist_items(playlist_id=self.uploads_id, limit=1)[
            'pageInfo']['totalResults']
        return self._total_uploads

    @property
    def total_playlists(self) -> int:
        '''total number of playlists from the user'''
        if self._total_playlists:
            return self._total_playlists

        self._total_playlists = YT.get_playlists(
            channel_id=self.id, limit=1, return_json=True)['pageInfo']['totalResults']
        return self._total_playlists

    @property
    def videos(self) -> List[Video]:
        '''Property getter for a user's video uploads'''
        for idx, video in enumerate(self._videos):
            if not isinstance(video, Video):
                video = Video(video)
                self._videos[idx] = video
        return self._videos

    def get_videos(
        self,
        limit: int = 10,
        reset: bool = False
    ) -> List[Video]:
        '''Get a list of Videos from a User'''
        results = []
        data = {'nextPageToken': '<placeholder>'}

        while  data.get('nextPageToken'):
            if data['nextPageToken'] == '<placeholder>' or reset:
                data = YT.get_playlist_items(
                    playlist_id=self.uploads_id, limit=limit, return_json=True)
            else:
                data = YT.get_playlist_items(
                    playlist_id=self.uploads_id,
                    page_token=data['nextPagetoken'],
                    limit=limit,
                    return_json=True
                )

            _results = [Video(video['snippet']) for video in data['items']]
            results += _results
            yield _results

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
        '''Property getter for a user's playlist'''
        from .playlist import Playlist

        for idx, playlist in enumerate(self._playlists):
            if not isinstance(playlist, Playlist):
                playlist = Playlist(playlist)
                self._playlists[idx] = playlist
        return self._playlists

    def get_all_playlists(self) -> List["ytmusic.Playlist"]:
        '''Get a list of all Playlists from a User'''
        from .playlist import Playlist

        if not self._needs_playlists_fetch:
            return self.playlists

        data = {'nextPageToken': '<placeholder>'}

        self._playlists = []
        while data.get('nextPageToken'):
            if not data:
                data = YT.get_playlists(
                    channel_id=self.id, limit=5, return_json=True)
            else:
                data = YT.get_playlists(
                    channel_id=self.id, limit=5, page_token=data['nextPageToken'], return_json=True)

            self._playlists += [Playlist(playlist['id'])
                                for playlist in data['items']]
        return self._playlists

    @cached_property
    def _needs_playlists_fetch(self):
        data = YT.get_playlists(channel_id=self.id, limit=5, return_json=True)
        self._total_playlists = data['pageInfo']['totalResults']
        if data['nextPageToken']:
            return True
        return False
