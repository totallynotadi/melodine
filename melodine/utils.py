import functools
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, FrozenSet, List, Optional, Union


# see https://stackoverflow.com/a/63658478/15146028
def slots(anotes: Dict[str, object]) -> FrozenSet[str]:
    return frozenset(anotes.keys())


@dataclass(repr=False)
class Image:
    """
    An object representing a Spotify image resource.

    Attributes
    ----------
    height : :class:`str`
        The height of the image.
    width : :class:`str`
        The width of the image.
    url : :class:`str`
        The URL of the image.
    """

    url: Optional[str]
    width: Optional[int]
    height: Optional[int]

    __slots__ = slots(__annotations__)


def singleton(cls):
    """class definitions marked singleton remember created instances and return that one same instance each time its object is instantialted.

    i.e. only one instance of an object can exist at any given time.
    """

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton


class CacheStrategy(Enum):
    NONE: bool = False
    MODERATE: None = None
    AGGRESSIVE: bool = True


def to_snake_case(x):
    return "_".join(x.lower().split(" "))


pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake_case(x):
    return pattern.sub("_", x).lower()


def sub_res_types(res_type: str) -> str:
    return (
        "More from YouTube"
        if res_type is None
        else (
            "Playlists"
            if res_type.lower() == "community playlists"
            else "Tracks"
            if res_type.lower() == "songs"
            else res_type
        )
    )


def transform_field_names(search_item: Union[Dict[str, Any], List[Dict[str, Any]]]):
    """
    convert a dictionary's key names from camelCase to snake_case recursively
    """
    if isinstance(search_item, list):
        transformed_sub_list = [transform_field_names(item) for item in search_item]
        return transformed_sub_list
    elif isinstance(search_item, dict):
        transformed_sub_item = {
            camel_to_snake_case(sub_res_types(key)): (
                transform_field_names(item) if isinstance(item, (dict, list)) else item
            )
            for (key, item) in search_item.items()
        }
        return transformed_sub_item
    else:
        return camel_to_snake_case(search_item)
