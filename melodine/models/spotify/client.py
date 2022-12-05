import os
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List, Literal, Optional

import appdirs
import spotipy
from typing_extensions import Self

from melodine.configs import CACHE_PATH, SCOPES, SPOTIFY
from melodine.models.spotify.album import Album
from melodine.models.spotify.artist import Artist
from melodine.models.spotify.episode import Episode
from melodine.models.spotify.player import Player
from melodine.models.spotify.playlist import Playlist
from melodine.models.spotify.show import Show
from melodine.models.spotify.track import PlaylistTrack, Track
from melodine.utils import Image, URIBase, singleton


@singleton
@dataclass
class Category:
    def __init__(self, data: Dict) -> None:
        self.id = data.get('id')  # pylint: disable=invalid-name
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
        if not os.path.exists(CACHE_PATH):
            self.__is_authorized = False

            self.id = None  # pylint: disable=invalid-name
            self.name = None
            self.href = None
            self.uri = None
            self.followers = None
            self.type = None
            self.images = None
        else:
            self.authorize()

    def __repr__(self):
        return f"<spotify.Client: {(self.name or 'Unauthorized')!r}>"

    @property
    def is_authorized(self) -> bool:
        return self.__is_authorized

    def authorize(self) -> None:
        '''carry out authorization to access a user's data'''

        SPOTIFY = spotipy.Spotify(
            auth_manager=spotipy.SpotifyOAuth(
                scope=SCOPES,
                client_id="22e27810dff0451bb93a71beb5e4b70d",
                client_secret="6254b7703d8540a48b4795d82eae9300",
                redirect_uri="http://localhost:8080/",
                cache_handler=spotipy.CacheFileHandler(
                    cache_path=os.path.join(
                        appdirs.user_data_dir(), '.melo', 'spotify_cache'
                    )
                )
            )
        )

        data = SPOTIFY.current_user()

        self.id = data.get('id')
        self.name = data.get('display_name')
        self.href = 'open.spotify.com/user/' + self.id
        self.uri = data.get('uri')
        self.followers = data.get('followers')
        self.type = data.get('type')
        self.images = [Image(**image_) for image_ in data.get('images', [])]
        self.__is_authorized = True

    def currently_playing(self) -> Track:
        data = SPOTIFY.current_user_playing_track()
        return Track(data['item'])

    def current_playback(self) -> Player:
        return Player(SPOTIFY.current_playback(), self)

    def recently_played(self, limit: int = 20) -> List[Track]:
        data = SPOTIFY.current_user_recently_played(limit=limit)
        return [Track(track_['track']) for track_ in data.get('items')]

    def featured_playlist(self) -> List[Playlist]:
        data = SPOTIFY.featured_playlists()
        return [Playlist(playlist) for playlist in data['playlists']['items']]

    def new_releases(self) -> List[Album]:
        data = SPOTIFY.new_releases()
        return [Album(album) for album in data['albums']['items']]

    @cached_property
    def categories(self):
        data = SPOTIFY.categories()
        return [Category(category) for category in data['categories']['items']]
    
    def is_artist_followed(self, artist_id: str) -> bool:
        return SPOTIFY.current_user_following_artists([artist_id])

    def follow_artist(self, artist_id: str) -> None:
        return SPOTIFY.user_follow_artists([artist_id])

    def unfollow_artist(self, artist_id: str) -> None:
        return SPOTIFY.user_unfollow_artists([artist_id])

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
    
    def is_playlist_followed(self, playlist_id: str) -> bool:
        return SPOTIFY.playlist_is_following(playlist_id, [self.id])

    def save_playlist(self, playlist_id: str) -> None:
        '''Add the current user as the follower of this playlist'''
        SPOTIFY.current_user_follow_playlist(playlist_id)

    def unsave_playlist(playlist_id: str) -> None:
        return SPOTIFY.current_user_unfollow_playlist(playlist_id)

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


    def is_album_saved(self, album_id: str) -> bool:
        ''' Check if an album is already saved in
            the current Spotify user’s “Your Music” library.
        '''
        return SPOTIFY.current_user_saved_albums_contains([album_id])[0]

    def save_album(self, album_id: str) -> None:
        '''Add one or more albums to the current user's
            "Your Music" library.
        '''
        return SPOTIFY.current_user_saved_albums_add([album_id])

    def unsave_album(self, album_id: str):
        return SPOTIFY.current_user_saved_albums_delete([album_id])
    
    def saved_albums(
        self,
        *,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0
    ) -> List[Album]:
        data = SPOTIFY.current_user_saved_albums(limit=limit, offset=offset)
        return [Album(album['album']) for album in data['items']]

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
    
    def is_track_saved(self, track_id: str) -> bool:
        return SPOTIFY.current_user_saved_tracks_contains([track_id])[0]

    def save_track(self, track_id: str) -> None:
        return SPOTIFY.current_user_saved_tracks_add([track_id])

    def unsave_track(self, track_id: str) -> None:
        return SPOTIFY.current_user_saved_tracks_delete([track_id])

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
    
    def is_episode_saved(self, episode_id: str) -> bool:
        return SPOTIFY.current_user_saved_episodes_contains([episode_id])[0]

    def save_episode(self, episode_id: str) -> None:
        return SPOTIFY.current_user_saved_episodes_add([episode_id])

    def unsave_episode(self, episode_id: str) -> None:
        return SPOTIFY.current_user_saved_episodes_delete([episode_id])

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

    def is_show_saved(self, show_id: str) -> bool:
        return SPOTIFY.current_user_saved_shows_contains([show_id])[0]

    def save_show(self, show_id: str) -> None:
        return SPOTIFY.current_user_saved_shows_add([show_id])

    def unsave_show(self, show_id: str) -> None:
        return SPOTIFY.current_user_saved_shows_delete([show_id])

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
        time_range: Literal['long_term', 'short_term',
                            'medium_term'] = 'medium_term'
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
        time_range: Literal[
            'long_term','short_term', 'medium_term'
        ] = 'medium_term'
    ) -> List[Track]:

        data = SPOTIFY.current_user_top_tracks(
            limit=limit,
            offset=offset,
            time_range=time_range
        )

        return [Track(track_) for track_ in data['items']]


client = Client()
