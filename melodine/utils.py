from dataclasses import dataclass
import functools
from enum import Enum
from typing import Dict, FrozenSet, List, Optional
from melodine.base.misc import SearchResultsBase

from melodine.base.track import TrackBase
from melodine.base.artist import ArtistBase
from melodine.base.album import AlbumBase
from melodine.base.playlist import PlaylistBase


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

    __slots__ = ("height", "width", "url")

    def __init__(self, *, height: str, width: str, url: str):
        self.height = height
        self.width = width
        self.url = url

    def __repr__(self):
        return f"<melo.Image: {self.url!r} (width: {self.width!r}, height: {self.height!r})>"

    def __eq__(self, other):
        return type(self) is type(other) and self.url == other.url


# @dataclass(frozen=True)
# class SearchResults(SearchResultsBase):
#     tracks: Optional[List[TrackBase]]
#     artists: Optional[List[ArtistBase]]
#     albums: Optional[List[AlbumBase]]
#     playlists: Optional[List[PlaylistBase]]


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


# weird workaround for using slots on dataclasses
# see https://stackoverflow.com/a/63658478/15146028
def slots(anotes: Dict[str, object]) -> FrozenSet[str]:
    return frozenset(anotes.keys())
