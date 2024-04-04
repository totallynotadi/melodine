from melodine.ytmusic.client import YTMusic
from melodine.ytmusic.views._artist import YTMusicArtist
from melodine.ytmusic.views._playlist import Playlist
from melodine.ytmusic.views._track import Track
from melodine.ytmusic.views._video import Video
from melodine.ytmusic.views.album import YTMusicAlbum
from melodine.ytmusic.views.search import search
from melodine.ytmusic.views.user import User

__all__ = [
    "YTMusic",
    "Track",
    "YTMusicArtist",
    "YTMusicAlbum",
    "Video",
    "User",
    "Playlist",
    "search",
]
