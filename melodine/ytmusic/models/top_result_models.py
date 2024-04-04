from dataclasses import dataclass
from typing import List, Optional

from melodine.utils import Image, slots
from melodine.ytmusic.models.partial_models import PartialAlbum, PartialArtist

__all__ = [
    "TopResultAlbum",
    "TopResultArtist",
    "TopResultPlaylist",
    "TopResultTrack",
    "TopResultVideo",
]


@dataclass(repr=False)
class TopResultAlbum:
    category: Optional[str]
    result_type: Optional[str]
    title: str
    artists: List[PartialArtist]
    browse_id: str
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class TopResultArtist:
    category: Optional[str]
    result_type: Optional[str]
    subscribers: str
    artists: List[PartialArtist]
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class TopResultPlaylist: ...


@dataclass(repr=False)
class TopResultTrack:
    category: Optional[str]
    result_type: Optional[str]
    video_id: str
    video_type: str
    title: str
    album: PartialAlbum
    artists: List["PartialArtist"]
    duration: str
    duration_seconds: int
    thumbnails: List["Image"]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class TopResultVideo:
    category: str
    result_type: Optional[str]
    video_id: str
    video_type: str
    title: str
    artists: List[PartialArtist]
    views: Optional[str]
    duration: Optional[str]
    duration_seconds: Optional[int]
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)
