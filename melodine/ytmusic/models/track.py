from dataclasses import dataclass
from typing import List, Optional
from melodine.utils import slots

from melodine.ytmusic.models.album import PartialAlbum
from melodine.ytmusic.models.artist import PartialArtist
from melodine.ytmusic.models.misc import Image


@dataclass(repr=False, frozen=True)
class PartialTrack:
    ...


@dataclass(repr=False, frozen=True)
class TopResultTrack:
    category: Optional[str]
    result_type: Optional[str]
    videoId: Optional[str]
    videotype: Optional[str]
    title: Optional[str]
    artists: Optional[List[PartialArtist]]
    duration: Optional[str]
    duration_seconds: Optional[int]
    thumbnails: Optional[List[Image]]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class SearchTrack:
    category: Optional[str]
    result_type: Optional[str]
    title: Optional[str]
    album: Optional[PartialAlbum]
    feedback_tokens: Optional[dict]
    video_id: Optional[str]
    video_type: Optional[str]
    duration: Optional[str]
    year: Optional[int]
    artists: Optional[List[PartialArtist]]
    duration_seconds: Optional[int]
    is_explicit: Optional[bool]
    thumbnails: Optional[List[Image]]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class AlbumTrack:
    video_id: Optional[str]
    title: Optional[str]
    artists: Optional[List[PartialArtist]]
    album: Optional[str]  # since it itself is a track from an album
    like_status: Optional[str]
    thumbnails: Optional[List[Image]]
    is_available: Optional[bool]
    is_explicit: Optional[bool]
    video_type: Optional[str]
    duration: Optional[str]
    duration_seconds: Optional[int]
    feedback_tokens: Optional[dict]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class FullTrack:
    ...
