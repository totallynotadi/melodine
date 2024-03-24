from dataclasses import dataclass
from typing import Optional

from melodine.utils import slots

__all__ = [
    "PartialAlbum",
    "PartialArtist",
    "PartialPlaylist",
    "PartialTrack",
    "PartialVideo",
]


@dataclass(repr=False)
class PartialAlbum:
    name: Optional[str]
    id: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class PartialArtist:
    name: Optional[str]
    id: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class PartialPlaylist: ...


@dataclass(repr=False)
class PartialTrack: ...


@dataclass(repr=False)
class PartialVideo: ...
