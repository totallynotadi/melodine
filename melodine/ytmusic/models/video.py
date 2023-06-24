from dataclasses import dataclass
from typing import List, Optional
from melodine.utils import slots

from melodine.ytmusic.models.artist import PartialArtist
from melodine.ytmusic.models.misc import Image


@dataclass(repr=False, frozen=True)
class PartialVideo:
    ...


@dataclass(repr=False, frozen=True)
class TopResultVideo:
    category: Optional[str]
    result_type: Optional[str]
    video_id: Optional[str]
    video_type: Optional[str]
    title: Optional[str]
    artists: Optional[List[PartialArtist]]
    views: Optional[str]
    duration: Optional[str]
    duration_seconds: Optional[int]
    thumbnails: Optional[List[Image]]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class SearchVideo:
    category: Optional[str]
    result_type: Optional[str]
    title: Optional[str]
    video_id: Optional[str]
    video_type: Optional[str]
    duration: Optional[str]
    year: Optional[int]
    artists: Optional[List[PartialArtist]]
    views: Optional[str]
    duration_seconds: Optional[int]
    thumbnails: Optional[List[Image]]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class FullhVideo:
    ...
