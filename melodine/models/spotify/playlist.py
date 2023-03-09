from typing import Dict, List, Optional, Union

from melodine.models import spotify

from melodine.utils import Image, URIBase
from melodine.configs import SPOTIFY
from melodine.models.spotify.track import PlaylistTrack, Track
from melodine.models.base.playlist import PlaylistBase


class Playlist(URIBase):  # pylint: disable=too-many-instance-attributes
    '''A Spotify playlist object'''
    __slots__ = (
        "tracks",
        "total_tracks",
        "images",
        "href",
        "name",
        "owner",
        "snapshot_id",
        "public",
        "collaborative",
        "description",
        "fllowers",
        "uri",
        "id",
    )

    def __init__(self, data: Dict) -> None:
        from .user import User

        self.id: str = data.get('id')  # pylint: disable=invalid-name

        self.name: str = data.get('name')
        self.owner: User = User(data.get('owner'))
        self.snapshot_id: str = data.get('snapshot_id')
        self.href: str = 'https://open.spotify.com/playlist/' + self.id
        self.uri: str = data.get('uri')

        self.public: bool = data.get('public')
        self.collaborative: bool = data.get('collaborative')
        self.description: str = data.get('description')
        self.followers: int = data.get('followers', {}).get('total', 0)

        self.tracks: List[PlaylistTrack] = [
            PlaylistTrack(track) for track in data['tracks']['items']
        ] if 'items' in data['tracks'] else []

        self.images: List[Image] = [
            Image(**image_) for image_ in data.get('images', [])
        ]

        self.total_tracks: int = data.get('tracks')['total']

    def __repr__(self) -> str:
        return f"melo.Playlist - {(self.name or self.id or self.uri)!r}"

    def get_tracks(
        self,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0
    ) -> List[PlaylistTrack]:
        '''Get  a list of tracks based on the given limit and offset

        Parameters
        ----------
        limit: `int`
            The maximum number of tracks to return.
        offset: `int`
            Specifies where the API should begin fetching tracks from.

        Returns
        -------
        result: `List[PlaylistTrack]`
            A list of tracks from the playlist.
        '''

        if (offset + limit) < self.total_tracks:
            return [PlaylistTrack(track_) for track_ in self.tracks[offset: offset + limit]]

        # TODO - Use multi-type results with playlist items (it returns episodes as well)
        data = SPOTIFY.playlist_tracks(
            self.id,
            limit=limit,
            offset=offset
        )

        return [PlaylistTrack(track_) for track_ in data['items']]

    def get_all_tracks(self) -> List[PlaylistTrack]:
        '''Get a list of all the tracks in aplaylist

        This operation might take long depending on the size of the playlist.
        '''

        if len(self.tracks) >= self.total_tracks:
            return self.tracks

        self.tracks = []
        offset = 0

        while len(self.tracks) < self.total_tracks:
            data = SPOTIFY.playlist_tracks(
                self.id,
                limit=50,
                offset=offset
            )

            self.tracks.extend([PlaylistTrack(track_) for track_ in data])
            offset += 50

        self.total_tracks = len(self.tracks)
        return self.tracks

    def add_items(self, items: List[Union[Track, "spotify.Episode", str]]) -> None:
        from .episode import Episode

        items = list(
            map(
                lambda item: item.id if isinstance(item, (Track, Episode))
                else item,
                items
            )
        )
        SPOTIFY.playlist_add_items(self.id, items=items)
        if len(self.tracks) == self.total_tracks:
            self.tracks.extend(items)
        self.total_tracks += len(items)

    # def saved(self) -> bool:
    #     from .client import client

    #     return SPOTIFY.playlist_is_following(self.id, client.id)

    # def save_playlist(self) -> None:
    #     '''Add the current user as the follower of this playlist'''
    #     SPOTIFY.current_user_follow_playlist(self.id)

    # def unsave_playlist(self) -> None:
    #     return SPOTIFY.current_user_unfollow_playlist(self.id)

    # TODO - implement scopes and playlist modifications
