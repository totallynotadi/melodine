from itertools import groupby
from typing import Any, Dict, List, Type, TypeVar

import dacite

from melodine.utils import sub_res_types, to_snake_case, transform_field_names
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

T = TypeVar("T")

_TYPES: Dict[str, Any] = {
    "artist": SearchArtist,
    "album": SearchAlbum,
    "song": SearchTrack,
    "video": SearchVideo,
    "playlist": SearchPlaylist,
}
_TOP_RES_TYPES: Dict[str, Any] = {
    "artist": TopResultArtist,
    "album": TopResultAlbum,
    "song": TopResultTrack,
    "video": TopResultVideo,
    "playlist": SearchPlaylist,
}


def model_item(search_item: Dict[str, Any], model_type: Type[T]) -> T:
    """
    Model a result item based on its `result_type` or a given dataclass model.
    Dataclass model, if provided will be prioritized over item's result type.
    """

    try:
        return dacite.from_dict(
            data_class=model_type,
            data=transform_field_names(search_item),
            config=dacite.Config(strict=True, strict_unions_match=True),
        )
    except dacite.MissingValueError as e:
        print("errored on search item:: ", e.field_path)
        print(e, "\n\n")
        [
            print(f"{key}: {val}")
            for key, val in transform_field_names(search_item).items()
        ]
        print(model_type, end="\n\n")
    except dacite.UnexpectedDataError as e:
        print("got unexpected data: ", e.args, e.keys)
        print(e, "\n\n")
        [
            print(f"{key}: {val}")
            for key, val in transform_field_names(search_item).items()
        ]
        print(model_type, end="\n\n")
    except dacite.WrongTypeError as e:
        print("data with wrong type found ", e, "\n\n")

        [
            print(f"{key}: {val}")
            for key, val in transform_field_names(search_item).items()
        ]
        print(model_type, end="\n\n")

    raise dacite.DaciteError()


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
            lambda x: model_item(
                search_item=x,
                model_type=(
                    _TOP_RES_TYPES[x["resultType"]]
                    if x["category"] == "Top result" or "category" not in x
                    else _TYPES[x["resultType"]]
                ),
            ),
            search_results,
        )
    )
    modeled_search = [item for item in modeled_search if item is not None]

    # group modeled results based on item category and return
    return group_models(modeled_search)
