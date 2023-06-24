from melodine.spotify.album import Album
from melodine.spotify.artist import Artist
from melodine.spotify.track import Track
from melodine.spotify.playlist import Playlist
from melodine.spotify.show import Show
from melodine.spotify.episode import Episode
from melodine.spotify.device import Device
from melodine.spotify.user import User
from melodine.spotify.player import Player
from melodine.spotify.category import Category
from melodine.spotify._search import search
from melodine.spotify.client import client

# client = Client()

__all__ = [
    "Track",
    "Artist",
    "Album",
    "Playlist",
    "User",
    "Player",
    "Show",
    "Episode",
    "Device",
    "Category",
    "search",
    "client",
]
