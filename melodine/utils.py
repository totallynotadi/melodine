from dataclasses import dataclass
import functools
from enum import Enum
import re
from typing import Dict, FrozenSet, Optional


# weird workaround for using slots on dataclasses
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

    i.e. only one instance of an object can exist at any given time."""

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


to_snake_case = lambda x: "_".join(x.lower().split(" "))

pattern = re.compile(r"(?<!^)(?=[A-Z])")
camel_to_snake_case = lambda x: pattern.sub("_", x).lower()
