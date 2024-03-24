from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from melodine.utils import Image, slots
from melodine.ytmusic.models.partial_models import PartialArtist

__all__ = [
    "FeedbackTokens",
    "LikeStatus",
    "AlbumTrack",
    "ArtistAlbum",
    "ArtistVideo",
    "ArtistRelatedArtists",
]


@dataclass(repr=False)
class FeedbackTokens:
    add: Optional[str]
    remove: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class LikeStatus(Enum):
    LIKE: bool = True
    INDIFFERENT: None = None
    DISLIKE: bool = False


@dataclass(repr=False)
class AlbumTrack:
    video_id: str
    title: str
    artists: List[PartialArtist]
    album: str
    like_status: LikeStatus
    thumbnails: Optional[List[Image]]
    is_available: bool
    is_explicit: bool
    video_type: str
    duration: str
    duration_seconds: int
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistAlbum:
    title: str
    year: Optional[str]
    browse_id: str
    thumbnails: List[Image]
    is_explicit: Optional[bool]


@dataclass(repr=False)
class ArtistVideo:
    title: str
    video_id: str
    artists: List[PartialArtist]
    playlist_id: str
    thumbnails: List[Image]
    views: str


@dataclass(repr=False)
class ArtistRelatedArtists:
    title: str
    browse_id: str
    subscribers: str
    thumbnails: List[Image]
