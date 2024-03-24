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


@dataclass(repr=False)
class SearchAlbum:
    category: Optional[str]
    result_type: Optional[str]
    title: str
    type: str
    duration: Optional[str]
    year: Optional[str]
    artists: List[PartialArtist]
    browse_id: str
    is_explicit: bool
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class SearchArtist:
    category: Optional[str]
    result_type: Optional[str]
    artist: str
    shuffle_id: str
    radio_id: str
    browse_id: str
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class SearchPlaylist:
    category: Optional[str]
    result_type: Optional[str]
    title: str
    item_count: str
    author: str
    browse_id: str
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class SearchTrack:
    category: Optional[str]
    result_type: Optional[str]
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
    category: Optional[str]
    result_type: Optional[str]
    title: str
    video_id: str
    video_type: str
    duration: Optional[str]
    year: Optional[int]
    artists: List[PartialArtist]
    views: Optional[str]
    duration_seconds: Optional[int]
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)
