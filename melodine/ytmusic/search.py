from itertools import groupby
from typing import Any, Dict, Iterable, List, Literal

import dacite
from dacite import Config, from_dict

from melodine.services import service
from melodine.utils import camel_to_snake_case, singleton, to_snake_case
from melodine.ytmusic.models.search import YTMusicSearchResults
from melodine.ytmusic.models.search_models import (
    SearchAlbum,
    SearchArtist,
    SearchPlaylist,
    SearchTrack,
    SearchVideo,
)
from melodine.ytmusic.models.top_result_models import (
    TopResultAlbum,
    TopResultArtist,
    TopResultTrack,
    TopResultVideo,
)

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

sub_res_types = lambda x: (
    "More from YouTube"
    if x is None
    else "Playlists" if x == "Community playlists" else "Tracks" if x == "Songs" else x
)


def transform_field_names(search_item: Dict[str, Any]):
    for key in list(search_item.keys()).copy():
        search_item[camel_to_snake_case(key)] = search_item.pop(key)
    return search_item


def model_callback(search_item: Dict[str, Any]) -> Any:
    if (
        search_item["category"] == "Profiles"
        or search_item["category"] == "Episodes"
        or search_item["category"] == "Podcasts"
    ):
        return

    dataclass = (
        _TOP_RES_TYPES[search_item["resultType"]]
        if search_item["category"] == "Top result"
        else _TYPES[search_item["resultType"]]
    )

    # [print(f"{key}: {val}") for key, val in transform_field_names(search_item).items()]
    # print(dataclass, end="\n\n")
    try:
        return from_dict(
            data_class=dataclass,
            data=transform_field_names(search_item),
            config=Config(strict=True, strict_unions_match=True),
        )
    except dacite.MissingValueError as e:
        print("errored on search item:: ", search_item)
        print(e)


def group_models(model_items: List[Any]) -> Dict[str, Any]:
    grouped_results = {}

    grouped_data = groupby(model_items, lambda x: x.category)  # type:ignore

    for key, val in grouped_data:
        grouped_results[to_snake_case(sub_res_types(key))] = list(val)

    return grouped_results


def parse_results(search_results: List[Dict[str, Any]]):
    modeled_search: List[Any] = list(
        map(
            model_callback,
            search_results,
        )
    )
    modeled_search = [_ for _ in modeled_search if _ is not None]

    return group_models(modeled_search)


def search(
    q: str,
    types: Iterable[
        Literal["tracks", "songs", "videos", "albums", "artists", "playlists"]
    ] = [],
    limit: int = 20,
) -> YTMusicSearchResults:
    search_results = []

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
            search_results.extend(results)
    else:
        results = service.ytmusic.search(q, limit=limit)
        search_results.extend(results)

    # print(search_results)

    search_results = parse_results(search_results)

    return from_dict(data_class=YTMusicSearchResults, data=search_results)  # type: ignore
