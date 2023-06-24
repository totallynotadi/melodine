from typing import List, Literal

from melodine.spotify.category import Category

from melodine.services import service

from melodine.spotify.album import Album
from melodine.spotify.artist import Artist
from melodine.spotify.episode import Episode
from melodine.spotify.player import Player
from melodine.spotify.playlist import Playlist
from melodine.spotify.show import Show
from melodine.spotify.track import PlaylistTrack, Track
from melodine.utils import Image, singleton
from melodine.base.misc import URIBase


@singleton
class Client(URIBase):
    def __init__(self) -> None:
        data = service.spotify.current_user()

        self.id = data.get("id")
        self.name = data.get("display_name")
        self.href = "open.spotify.com/user/" + self.id
        self.uri = data.get("uri")
        self.followers = data.get("followers")
        self.type = data.get("type")
        self.images = [Image(**image_) for image_ in data.get("images", [])]

    def __repr__(self):
        return f"<spotify.Client: {(self.name or 'Unauthorized')!r}>"

    def currently_playing(self) -> Track:
        data = service.spotify.current_user_playing_track()
        return Track(data["item"])

    def current_playback(self) -> Player:
        return Player(service.spotify.current_playback(), self)

    def recently_played(self, limit: int = 20) -> List[Track]:
        data = service.spotify.current_user_recently_played(limit=limit)
        return [Track(track_["track"]) for track_ in data.get("items")]

    def featured_playlist(self) -> List[Playlist]:
        data = service.spotify.featured_playlists()
        return [Playlist(playlist) for playlist in data["playlists"]["items"]]

    def new_releases(self) -> List[Album]:
        data = service.spotify.new_releases()
        return [Album(album) for album in data["albums"]["items"]]

    def get_categories(self, limit: int = 20, offset: int = 0) -> List[Category]:
        return Category.get_categories(limit=limit, offset=offset)

    def is_artist_followed(self, artist_id: str) -> bool:
        return service.spotify.current_user_following_artists([artist_id])

    def follow_artist(self, artist_id: str) -> None:
        return service.spotify.user_follow_artists([artist_id])

    def unfollow_artist(self, artist_id: str) -> None:
        return service.spotify.user_unfollow_artists([artist_id])

    def followed_artists(
        self,
        *,
        limit: int = 20,
    ) -> List[Artist]:
        data = service.spotify.current_user_followed_artists(limit=limit)
        return [Artist(artist) for artist in data["artists"]["items"]]

    # @cached_property
    # def all_followed_artists(self) -> List[Artist]:
    #     data = {"next": "<placeholder>"}
    #     results = []

    #     while data.get("next"):
    #         if data["next"] == "<placeholder>":
    #             data = service.spotify.current_user_followed_artists()["artists"]
    #         else:
    #             data = service.spotify.next(data)["artists"]
    #         results += data["items"]
    #     return [Artist(artist) for artist in results]

    def is_playlist_followed(self, playlist_id: str) -> bool:
        return service.spotify.playlist_is_following(playlist_id, [self.id])

    def save_playlist(self, playlist_id: str) -> None:
        """Add the current user as the follower of this playlist"""
        service.spotify.current_user_follow_playlist(playlist_id)

    def unsave_playlist(playlist_id: str) -> None:
        return service.spotify.current_user_unfollow_playlist(playlist_id)

    def saved_playlists(self, *, limit: int = 50, offset: int = 0) -> List[Playlist]:
        data = service.spotify.current_user_playlists(limit=limit, offset=offset)
        return [Playlist(playlist) for playlist in data["items"]]

    # @cached_property
    # def all_saved_playlists(self) -> List[Playlist]:
    #     data = {"next": "<placeholder>"}
    #     results = []

    #     while data.get("next"):
    #         if data["next"] == "<placeholder>":
    #             data = service.spotify.current_user_playlists()
    #         else:
    #             data = service.spotify.next(data)
    #         results += data["items"]
    #     return [Playlist(playlist) for playlist in results]

    def is_album_saved(self, album_id: str) -> bool:
        """Check if an album is already saved in
        the current Spotify user’s “Your Music” library.
        """
        return service.spotify.current_user_saved_albums_contains([album_id])[0]

    def save_album(self, album_id: str) -> None:
        """Add one or more albums to the current user's
        "Your Music" library.
        """
        return service.spotify.current_user_saved_albums_add([album_id])

    def unsave_album(self, album_id: str):
        return service.spotify.current_user_saved_albums_delete([album_id])

    def saved_albums(self, *, limit: int = 20, offset: int = 0) -> List[Album]:
        data = service.spotify.current_user_saved_albums(limit=limit, offset=offset)
        return [Album(album["album"]) for album in data["items"]]

    # @cached_property
    # def all_saved_albums(self) -> List[Album]:
    #     data = {"next": "<placeholder>"}
    #     results = []

    #     while data.get("next"):
    #         if data["next"] == "<placeholder>":
    #             # print("lmao")
    #             data = service.spotify.current_user_saved_albums()
    #             # print(data.keys())
    #         else:
    #             data = service.spotify.next(data)
    #         results += data["items"]
    #     return [Album(album["album"]) for album in results]

    def is_track_saved(self, track_id: str) -> bool:
        return service.spotify.current_user_saved_tracks_contains([track_id])[0]

    def save_track(self, track_id: str) -> None:
        return service.spotify.current_user_saved_tracks_add([track_id])

    def unsave_track(self, track_id: str) -> None:
        return service.spotify.current_user_saved_tracks_delete([track_id])

    def saved_tracks(self, *, limit: int = 20, offset: int = 0) -> List[PlaylistTrack]:
        data = service.spotify.current_user_saved_tracks(limit=limit, offset=offset)
        results = []
        for track in data["items"]:
            track["added_by"] = self
            track = PlaylistTrack(track)
            results.append(track)
        return results

    # @cached_property
    # def all_saved_tracks(self) -> List[PlaylistTrack]:
    #     data = {"next": "<placeholder>"}
    #     results = []

    #     while data.get("next"):
    #         if data["next"] == "<placeholder>":
    #             data = service.spotify.current_user_saved_tracks()
    #         else:
    #             data = service.spotify.next(data)
    #         results += data["items"]
    #     for idx, track in enumerate(results.copy()):
    #         track["added_by"] = self
    #         track = PlaylistTrack(track)
    #         results[idx] = track
    #     return results

    def is_episode_saved(self, episode_id: str) -> bool:
        return service.spotify.current_user_saved_episodes_contains([episode_id])[0]

    def save_episode(self, episode_id: str) -> None:
        return service.spotify.current_user_saved_episodes_add([episode_id])

    def unsave_episode(self, episode_id: str) -> None:
        return service.spotify.current_user_saved_episodes_delete([episode_id])

    def saved_episodes(self, *, limit: int = 20, offset: int = 0) -> List[Episode]:
        data = service.spotify.current_user_saved_episodes(limit=limit, offset=offset)
        return [Episode(episode["episode"]) for episode in data["items"]]

    # def all_saved_episodes(self) -> List[Episode]:
    #     data = {"next": "<placeholder>"}
    #     results = []

    #     while data.get("next"):
    #         if data["next"] == "<placeholder>":
    #             data = service.spotify.current_user_saved_episodes()
    #         else:
    #             data = service.spotify.next(data)
    #         results += data["items"]
    #     return [Episode(episode["episode"]) for episode in results]

    def is_show_saved(self, show_id: str) -> bool:
        return service.spotify.current_user_saved_shows_contains([show_id])[0]

    def save_show(self, show_id: str) -> None:
        return service.spotify.current_user_saved_shows_add([show_id])

    def unsave_show(self, show_id: str) -> None:
        return service.spotify.current_user_saved_shows_delete([show_id])

    def saved_shows(self, *, limit: int = 20, offset: int = 0) -> List[Show]:
        data = service.spotify.current_user_saved_shows(limit=limit, offset=offset)
        return [Show(show["show"]) for show in data["items"]]

    def all_saved_shows(self) -> List[Show]:
        data = {"next": "<placeholder>"}
        results = []

        while data.get("next"):
            if data["next"] == "<placeholder>":
                data = service.spotify.current_user_saved_shows()
            else:
                data = service.spotify.next(data)
            results += data["items"]
        return [Show(show["show"]) for show in results]

    def top_artists(
        self,
        limit: int = 20,
        offset: int = 0,
        time_range: Literal["long_term", "short_term", "medium_term"] = "medium_term",
    ) -> List[Artist]:
        data = service.spotify.current_user_top_artists(
            limit=limit, offset=offset, time_range=time_range
        )
        return [Artist(artist_) for artist_ in data["items"]]

    def top_tracks(
        self,
        limit: int = 20,
        offset: int = 0,
        time_range: Literal["long_term", "short_term", "medium_term"] = "medium_term",
    ) -> List[Track]:
        data = service.spotify.current_user_top_tracks(
            limit=limit, offset=offset, time_range=time_range
        )
        return [Track(track_) for track_ in data["items"]]


client = Client()
