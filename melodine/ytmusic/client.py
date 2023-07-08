from typing import Dict, Iterable, List, Literal, TYPE_CHECKING, Optional
from melodine.utils import CacheStrategy

from melodine.ytmusic.search import YTMusicSearch

if TYPE_CHECKING:
    import requests
    import ytmusicapi

from melodine.services import service
from melodine.ytmusic.search import search, YTMusicSearchResults


class YTMusic:
    def __init__(
        self,
        cookie: str = "",
        cache_strategy: Optional[CacheStrategy] = None,
        session: Optional["requests.Session"] = None,
    ) -> None:
        self._ytmusic: "ytmusicapi.YTMusic" = service._ytmusic(cookie)
        self._search: YTMusicSearch = YTMusicSearch()

    def home(self, limit=4):
        raise NotImplementedError()

    def search(
        self,
        query: str,
        *,
        types: Iterable[
            Literal["tracks", "videos", "albums", "artists", "playlists"]
        ] = [],
        limit: int = 20,
    ) -> YTMusicSearchResults:
        return self._search.search(query, types, limit)

    def get_search_suggestions(self, query: str, *, detailed: bool = False):
        raise NotImplementedError()

    def library_albums(
        self,
        limit: int = 25,
        order: Literal["a_to_z", "z_to_a", "recently_added"] = None,
    ):
        raise NotImplementedError()

    def library_artists(
        self,
        limit: int = 25,
        order: Literal["a_to_z", "z_to_a", "recently_added"] = None,
    ):
        raise NotImplementedError()

    def library_playlists(
        self,
        limit: int = 25,
    ):
        raise NotImplementedError()

    def library_songs(
        self,
        limit: int = 25,
        order: Literal["a_to_z", "z_to_a", "recently_added"] = None,
    ):
        raise NotImplementedError()

    def liked_songs(limit: int = 100):
        raise NotImplementedError()

    def get_tasteprofile(self):
        raise NotImplementedError()

    def set_tasteprofile(self, artists: List[str], taste_profile: Dict = None):
        raise NotImplementedError()

    def get_categories(self):
        raise NotImplementedError()