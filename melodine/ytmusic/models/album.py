from dataclasses import dataclass
from typing import List, Optional
from melodine.utils import slots

from melodine.ytmusic.models.artist import PartialArtist
from melodine.ytmusic.models.track import AlbumTrack
from melodine.ytmusic.models.misc import Image


@dataclass(repr=False, frozen=True)
class PartialAlbum:
    name: Optional[str]
    id: Optional[str]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class TopResultAlbum:
    category: Optional[str]
    result_type: Optional[str]
    title: Optional[str]
    artists: Optional[List[PartialArtist]]
    thumbnails: Optional[List[Image]]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class SearchAlbum:
    category: Optional[str]
    result_type: Optional[str]
    title: Optional[str]
    type: Optional[str]
    duration: Optional[str]
    year: Optional[str]
    artists: Optional[List[PartialArtist]]
    browse_id: Optional[str]
    is_explicit: Optional[bool]
    thumbnails: Optional[List[Image]]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class FullAlbum:
    title: Optional[str]
    type: Optional[str]
    thumbnails: Optional[List[Image]]
    artists: Optional[List[PartialArtist]]
    year: Optional[str]
    track_count: Optional[int]
    duration: Optional[str]
    audio_playlist_id: Optional[str]
    tracks: Optional[List[AlbumTrack]]
    duration_seconds: Optional[int]

    __slots__ = slots(__annotations__)
