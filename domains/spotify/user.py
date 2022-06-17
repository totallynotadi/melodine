from typing import Dict, List, Literal, Optional

from ...utils import SPOTIFY, Image
from . import Artist, Track
from .player import Player


class User:
    def __init__(self, data: Dict) -> None:
        self.id = data.get('id')
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

    def top_artist(
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

    def top_track(
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
