from melodine.models.spotify.album import Album
from melodine.models.spotify.artist import Artist
from melodine.models.spotify.track import Track
from melodine.models.spotify.playlist import Playlist
from melodine.models.spotify.show import Show
from melodine.models.spotify.episode import Episode
from melodine.models.spotify.device import Device
from melodine.models.spotify.user import User
from melodine.models.spotify.player import Player
from melodine.models.spotify._search import search
from melodine.models.spotify.client import client

# client = Client()

__all__ = [
    'Track',
    'Artist',
    'Album',
    'Playlist',
    'User',
    'Player',
    'Show',
    'Episode',
    'Device',
    'search',
    'client'
]
