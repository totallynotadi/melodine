from itertools import groupby
from typing import Any, Callable, Iterable, Literal, Dict, List

from dacite import from_dict
from melodine.services import service
from melodine.utils import singleton
from melodine.ytmusic.models.search import YTMusicSearchResults
from melodine.ytmusic.models.artist import SearchArtist, TopResultArtist
from melodine.ytmusic.models.album import SearchAlbum, TopResultAlbum
from melodine.ytmusic.models.track import SearchTrack, TopResultTrack
from melodine.ytmusic.models.video import SearchVideo, TopResultVideo
from melodine.ytmusic.models.playlist import SearchPlaylist


_SEARCH_TYPES = {"artists", "albums", "tracks", "videos", "playlists"}

_TYPES = {
    "artist": SearchArtist,
    "album": SearchAlbum,
    "song": SearchTrack,
    "video": SearchVideo,
    "playlist": SearchPlaylist,
}
_TOP_RES_TYPES = {
    "artist": TopResultArtist,
    "album": TopResultAlbum,
    "song": TopResultTrack,
    "video": TopResultVideo,
    "playlist": SearchPlaylist,
}


to_snake_case = lambda x: "_".join(x.lower().split(" "))

sub_res_types = lambda x: (
    "More from YouTube"
    if x is None
    else "Playlists"
    if x == "Community playlists"
    else "Tracks"
    if x == "Songs"
    else x
)


def group_models(search_json: List[Dict]) -> Dict[str, Any]:
    grouped_results = {}

    grouped_data = groupby(search_json, lambda x: x.category)  # type:ignore

    for key, val in grouped_data:
        grouped_results[to_snake_case(sub_res_types(key))] = list(val)

    return grouped_results


@singleton
class YTMusicSearch:
    @staticmethod
    def search(
        q: str,
        *,
        types: Iterable[
            Literal["tracks", "songs", "videos", "albums", "artists", "playlists"]
        ] = [],
        limit: int = 20,
    ) -> YTMusicSearchResults:
        search_json = []

        if types:
            if not hasattr(types, "__iter__"):
                raise TypeError("types must be an iterable.")

            types = set(types)

            if not types.issubset(_SEARCH_TYPES):
                raise ValueError(
                    'Bad queary type! got "%s" expected one or more of: tracks, playlists, artists, albums, videos'
                    % types.difference(_SEARCH_TYPES).pop()
                )

            if "tracks" in types:
                types.remove("tracks")
                types.add("songs")

            for type in types:
                results = service.ytmusic.search(q, filter=type, limit=limit)
                search_json.extend(results)
        else:
            results = service.ytmusic.search(q, limit=limit)
            search_json.extend(results)

        model_callback: Callable[[Dict[str, Any]], Any] = lambda x: from_dict(
            data_class=_TOP_RES_TYPES[x["resultType"]]
            if x["category"] == "Top result"
            else _TYPES[x["resultType"]],
            data=x,
        )

        modeled_srch: List[Any] = list(
            map(
                model_callback,
                search_json,
            )
        )

        grouped_models = group_models(modeled_srch)

        return from_dict(data_class=YTMusicSearchResults, data=grouped_models)  # type: ignore


# using __func__ to bind the search attribute's underlying function to wherever it's being used.
# https://stackoverflow.com/questions/41921255/staticmethod-object-is-not-callable
search: YTMusicSearch.search = YTMusicSearch.search.__func__  # type: ignore
