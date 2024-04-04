from typing import TYPE_CHECKING, Dict, Iterable, List, Literal, Optional

from melodine.utils import CacheStrategy

if TYPE_CHECKING:
    import requests
    import ytmusicapi

from melodine.services import service
from melodine.ytmusic.views.search import YTMusicSearchResults, search


class YTMusic:
    def __init__(
        self,
        cookie: str = "",
        cache_strategy: Optional[CacheStrategy] = None,
        session: Optional["requests.Session"] = None,
    ) -> None:
        self._ytmusic: "ytmusicapi.YTMusic" = service._ytmusic(cookie)

    def home(self, limit=4):
        raise NotImplementedError()

    def search(
        self,
        query: str,
        types: Iterable[
            Literal["tracks", "videos", "albums", "artists", "playlists"]
        ] = [],
        limit: int = 20,
    ) -> YTMusicSearchResults:
        return search(query, types, limit)

    def get_search_suggestions(self, query: str, *, detailed: bool = False):
        raise NotImplementedError()

    def library_albums(
        self,
        limit: Optional[int] = 25,
        order: Optional[Literal["a_to_z", "z_to_a", "recently_added"]] = None,
    ):
        raise NotImplementedError()

    def library_artists(
        self,
        limit: Optional[int] = 25,
        order: Optional[Literal["a_to_z", "z_to_a", "recently_added"]] = None,
    ):
        raise NotImplementedError()

    def library_playlists(
        self,
        limit: int = 25,
    ):
        raise NotImplementedError()

    def library_songs(
        self,
        limit: Optional[int] = 25,
        order: Optional[Literal["a_to_z", "z_to_a", "recently_added"]] = None,
    ):
        raise NotImplementedError()

    def liked_songs(self, limit: Optional[int] = 100):
        raise NotImplementedError()

    def get_tasteprofile(self):
        raise NotImplementedError()

    def set_tasteprofile(
        self, artists: Optional[List[str]], taste_profile: Optional[Dict] = None
    ):
        raise NotImplementedError()

    def get_categories(self):
        raise NotImplementedError()
