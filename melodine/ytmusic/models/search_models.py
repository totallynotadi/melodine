from dataclasses import dataclass
from typing import List, Optional

from melodine.utils import Image, slots
from melodine.ytmusic.models.partial_models import PartialAlbum, PartialArtist

__all__ = [
    "SearchAlbum",
    "SearchArtist",
    "SearchPlaylist",
    "SearchTrack",
    "SearchVideo",
]


@dataclass(repr=False, frozen=True)
class SearchAlbum:
    category: str
    result_type: str
    title: str
    type: str
    duration: Optional[str]
    year: str
    artists: List[PartialArtist]
    browse_id: str
    is_explicit: bool
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class SearchArtist:
    category: str
    result_type: str
    artist: str
    shuffle_id: Optional[str]
    radio_id: Optional[str]
    browse_id: str
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class SearchPlaylist:
    category: str
    result_type: str
    title: str
    item_count: str
    author: str
    browse_id: str
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class SearchTrack:
    category: str
    result_type: str
    title: str
    album: PartialAlbum
    feedback_tokens: dict
    video_id: str
    video_type: str
    duration: Optional[str]
    year: Optional[int]
    artists: List[PartialArtist]
    duration_seconds: int
    is_explicit: bool
    in_library: bool
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class SearchVideo:
    category: str
    result_type: str
    title: str
    video_id: str
    video_type: str
    duration: Optional[str]
    year: Optional[int]
    artists: List[PartialArtist]
    views: str
    duration_seconds: int
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)
