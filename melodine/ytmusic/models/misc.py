from dataclasses import dataclass
from typing import Optional

from melodine.utils import slots


@dataclass(repr=False, frozen=True)
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


@dataclass(repr=False, frozen=True)
class FeedbackTokens:
    add: Optional[str]
    remove: Optional[str]

    __slots__ = slots(__annotations__)
