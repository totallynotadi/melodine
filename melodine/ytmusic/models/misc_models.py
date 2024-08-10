from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, Optional

from melodine.utils import Image, slots
from melodine.ytmusic.models.partial_models import PartialArtist

__all__ = [
    "FeedbackTokens",
    "LikeStatus",
    "AlbumTrack",
    "ArtistAlbum",
    "ArtistVideo",
    "ArtistRelatedArtist",
]


@dataclass(repr=False)
class FeedbackTokens:
    add: Optional[str]
    remove: Optional[str]
    __slots__ = slots(__annotations__)


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
    like_status: Literal["LIKE", "INDIFFERENT", "DISLIKE"]
    in_library: Optional[bool]
    thumbnails: Optional[
        List[Image]
    ]  # images are optional since they can be referenced from their parent album.
    is_available: bool
    is_explicit: bool
    video_type: str
    views: str
    track_number: int
    duration: str
    duration_seconds: int
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistAlbum:
    title: str
    type: Optional[Literal["Album", "EP"]]
    year: Optional[str]
    artists: Optional[List[PartialArtist]]
    browse_id: str
    audio_playlist_id: Optional[str]
    thumbnails: List[Image]
    is_explicit: Optional[bool]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistSingle:
    title: str
    browse_id: str
    audio_playlist_id: Optional[str]
    thumbnails: List[Image]
    is_explicit: Optional[bool]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistVideo:
    title: str
    video_id: str
    artists: List[PartialArtist]
    playlist_id: str
    thumbnails: List[Image]
    views: str
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistRelatedArtist:
    title: str
    browse_id: str
    subscribers: str
    thumbnails: List[Image]
    __slots__ = slots(__annotations__)
