from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List, Literal, Optional
from typing_extensions import Self

from ...utils import SPOTIFY, Image, URIBase
from .album import Album
from .artist import Artist
from .episode import Episode
from .player import Player
from .playlist import Playlist
from .show import Show
from .track import PlaylistTrack, Track


@dataclass
class Category:
    def __init__(self, data: Dict) -> None:
        self.id = data.get('id')  #pylint: disable=invalid-name
        self.name = data.get('name')
        self.images = [Image(**image) for image in data.get('icons')]

    @classmethod
    def from_id(cls, category_id: str) -> Self:
        category_data = SPOTIFY.category(category_id)
        return cls(category_data)

    def get_playlist(self) -> List[Playlist]:
        data = SPOTIFY.category_playlists(self.id)
        return [Playlist(playlist) for playlist in data['playlists']['items']]


class Client(URIBase):
    def __init__(self) -> None:

        data = SPOTIFY.current_user()

        self.id = data.get('id')  # pylint: disable=invalid-name
        self.name = data.get('display_name')
        self.href = 'open.spotify.com/user/' + self.id
        self.uri = data.get('uri')
        self.followers = data.get('followers')
        self.type = data.get('type')
        self.images = [Image(**image_) for image_ in data.get('images', [])]

    def __repr__(self):
        return f"<spotify.User: {(self.name or self.id)!r}>"

    def currently_playing(self) -> Track:
        data = SPOTIFY.current_user_playing_track()
        return Track(data['item'])

    def current_playback(self) -> Player:
        return Player(SPOTIFY.current_playback(), self)

    def recently_played(self, limit: int = 20) -> List[Track]:
        data = SPOTIFY.current_user_recently_played(limit=limit)
        return [Track(track_) for track_ in data.get('track', {})]

    def featured_playlist(self) -> List[Playlist]:
        data = SPOTIFY.featured_playlists()
        return [Playlist(playlist) for playlist in data['playlists']['items']]

    def new_releases(self):
        data = SPOTIFY.new_releases()
        return [Album(album) for album in data['albums']['items']]

    @cached_property
    def categories(self):
        data = SPOTIFY.categories()
        return [Category(category) for category in data['categories']['items']]

    def followed_artists(
        self,
        *,
        limit: Optional[int] = 20,
    ) -> List[Artist]:
        data = SPOTIFY.current_user_followed_artists(limit=limit)
        return [Artist(artist) for artist in data['artists']['items']]

    @cached_property
    def all_followed_artists(self) -> List[Artist]:
        data = {'next': '<placeholder>'}
        results = []

        while data.get('next'):
            if data['next'] == '<placeholder>':
                data = SPOTIFY.current_user_followed_artists()['artists']
            else:
                data = SPOTIFY.next(data)['artists']
            results += data['items']
        return [Artist(artist) for artist in results]

    def saved_playlists(
        self,
        *,
        limit: Optional[int] = 50,
        offset: Optional[int] = 0
    ) -> List[Playlist]:
        data = SPOTIFY.current_user_playlists(limit=limit, offset=offset)
        return [Playlist(playlist) for playlist in data['items']]

    @cached_property
    def all_saved_playlists(self) -> List[Playlist]:
        data = {'next': '<placeholder>'}
        results = []

        while data.get('next'):
            if data['next'] == '<placeholder>':
                data = SPOTIFY.current_user_playlists()
            else:
                data = SPOTIFY.next(data)
            results += data['items']
        return [Playlist(playlist) for playlist in results]

    def saved_albums(
        self,
        *,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0
    ) -> List[Album]:
        data = SPOTIFY.current_user_saved_albums(limit=limit, offset=offset)
        return [Album(album) for album in data['items']]

    @cached_property
    def all_saved_albums(self) -> List[Album]:
        data = {'next': '<placeholder>'}
        results = []

        while data.get('next'):
            if data['next'] == '<placeholder>':
                print('lmao')
                data = SPOTIFY.current_user_saved_albums()
                print(data.keys())
            else:
                data = SPOTIFY.next(data)
            results += data['items']
        return [Album(album['album']) for album in results]

    def saved_tracks(
        self,
        *,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0
    ) -> List[PlaylistTrack]:
        data = SPOTIFY.current_user_saved_tracks(limit=limit, offset=offset)
        results = []
        for track in data['items']:
            track['added_by'] = self
            track = PlaylistTrack(track)
            results.append(track)
        return results

    @cached_property
    def all_saved_tracks(self) -> List[PlaylistTrack]:
        data = {'next': '<placeholder>'}
        results = []

        while data.get('next'):
            if data['next'] == '<placeholder>':
                data = SPOTIFY.current_user_saved_tracks()
            else:
                data = SPOTIFY.next(data)
            results += data['items']
        for idx, track in enumerate(results.copy()):
            track['added_by'] = self
            track = PlaylistTrack(track)
            results[idx] = track
        return results

    def saved_episodes(
        self,
        *,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0
    ) -> List[Episode]:
        data = SPOTIFY.current_user_saved_episodes(limit=limit, offset=offset)
        return [Episode(episode['episode']) for episode in data['items']]

    def all_saved_episodes(self) -> List[Episode]:
        data = {'next': '<placeholder>'}
        results = []

        while data.get('next'):
            if data['next'] == '<placeholder>':
                data = SPOTIFY.current_user_saved_episodes()
            else:
                data = SPOTIFY.next(data)
            results += data['items']
        return [Episode(episode['episode']) for episode in results]

    def saved_shows(
        self,
        *,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0
    ) -> List[Show]:
        data = SPOTIFY.current_user_saved_shows(limit=limit, offset=offset)
        return [Show(show['show']) for show in data['items']]

    def all_saved_shows(self) -> List[Show]:
        data = {'next': '<placeholder>'}
        results = []

        while data.get('next'):
            if data['next'] == '<placeholder>':
                data = SPOTIFY.current_user_saved_shows()
            else:
                data = SPOTIFY.next(data)
            results += data['items']
        return [Show(show['show']) for show in results]

    def top_artists(
        self,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        time_range: Literal['long_term', 'short_term', 'medium_term'] = 'medium_term'
    ) -> List[Artist]:

        data = SPOTIFY.current_user_top_artists(
            limit=limit,
            offset=offset,
            time_range=time_range
        )

        return [Artist(artist_) for artist_ in data['items']]

    def top_tracks(
        self,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        time_range: Literal['long_term', 'short_term', 'medium_term'] = 'medium_term'
    ) -> List[Track]:

        data = SPOTIFY.current_user_top_tracks(
            limit=limit,
            offset=offset,
            time_range=time_range
        )

        return [Track(track_) for track_ in data['items']]

client = Client()
