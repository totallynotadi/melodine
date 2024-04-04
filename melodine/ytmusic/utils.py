from itertools import groupby
from typing import Any, Callable, Dict, List, Optional

import dacite

from melodine.utils import to_snake_case, transform_field_names
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


def ensure_data(func: Callable):
    def inner(self):
        try:
            return func(self)
        except AttributeError:
            self._get_data()
            return func(self)

    return inner


def sub_res_types(res_type):
    return (
        "More from YouTube"
        if res_type is None
        else (
            "Playlists"
            if res_type == "Community playlists"
            else "Tracks"
            if res_type == "Songs"
            else res_type
        )
    )


def model_item(search_item: Dict[str, Any], model: Optional[Any] = None) -> Any:
    """
    Model a result item based on its `result_type` or a given dataclass model.
    Dataclass model, if provided will be prioritized over item's result type.
    """
    if "category" in search_item:
        # TODO: we're not supporting Podcasts and User Profiles on YTMusic yet.
        if (
            search_item["category"] == "Profiles"
            or search_item["category"] == "Episodes"
            or search_item["category"] == "Podcasts"
        ):
            return

    if "resultType" in search_item:
        # hacky fix
        if search_item["resultType"] == "album":
            search_item["artists"] = list(
                filter(lambda x: x["id"] is not None, search_item.pop("artists"))
            )

    dataclass = (
        (
            _TOP_RES_TYPES[search_item["resultType"]]
            if search_item["category"] == "Top result" or "category" not in search_item
            else _TYPES[search_item["resultType"]]
        )
        if model is None
        else model
    )

    # [print(f"{key}: {val}") for key, val in transform_field_names(search_item).items()]
    # print(dataclass, end="\n\n")
    try:
        return dacite.from_dict(
            data_class=dataclass,
            data=transform_field_names(search_item),
            config=dacite.Config(strict=True, strict_unions_match=True),
        )
    except dacite.MissingValueError as e:
        print("errored on search item:: ", search_item)
        print(e)


def group_models(model_items: List[Any]) -> Dict[str, Any]:
    grouped_results = {}

    grouped_data = groupby(model_items, lambda x: x.category)

    for key, val in grouped_data:
        grouped_results[to_snake_case(sub_res_types(key))] = list(val)

    return grouped_results


def model_search_results(search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    # model search results
    modeled_search: List[Any] = list(
        map(
            model_item,
            search_results,
        )
    )
    modeled_search = [_ for _ in modeled_search if _ is not None]

    # group modeled results based on item category and return
    return group_models(modeled_search)
