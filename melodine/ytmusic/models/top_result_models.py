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
    category: str
    result_type: str
    title: str
    artists: List[PartialArtist]
    browse_id: str
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class TopResultArtist:
    category: str
    result_type: str
    subscribers: str
    artists: List[PartialArtist]
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class TopResultPlaylist: ...


@dataclass(repr=False)
class TopResultTrack:
    category: str
    result_type: str
    video_id: str
    video_type: str
    title: str
    artists: List[PartialArtist]
    album: PartialAlbum
    duration: str
    duration_seconds: int
    thumbnails: List[Image]
    is_explicit: Optional[bool]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class TopResultVideo:
    category: str
    result_type: str
    video_id: str
    video_type: str
    title: str
    artists: List[PartialArtist]
    views: Optional[str]
    duration: Optional[str]
    duration_seconds: Optional[int]
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)
