"""
describes models for the response from the `get_<object>()` endpoints from ytmusicapi.
for e.g. get_song(), get_artist(), get_album(), get_channel(), get_playlist(), etc.
"""

from dataclasses import dataclass
from typing import List, Literal, Optional

from melodine.utils import Image, slots
from melodine.ytmusic.models.misc_models import (
    AlbumTrack,
    ArtistAlbum,
    ArtistRelatedArtist,
    ArtistSingle,
    ArtistVideo,
    FeedbackTokens,
)
from melodine.ytmusic.models.partial_models import PartialAlbum, PartialArtist

__all__ = ["FullAlbum", "FullArtist", "FullPlaylist", "FullVideo"]


@dataclass(repr=False)
class FullAlbum:
    title: str
    type: str
    thumbnails: List[Image]
    is_explicit: bool
    description: Optional[str]
    artists: List[PartialArtist]
    year: str
    track_count: int
    duration: str
    audio_playlist_id: str
    tracks: List[AlbumTrack]
    duration_seconds: int
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class FullTrack:
    video_id: str
    title: str
    artists: List[PartialArtist]
    album: PartialAlbum
    like_status: Literal["LIKE", "INDIFFERENT", "DISLIKE"]
    thumbnails: List[Image]
    in_library: Optional[bool]
    is_available: bool
    is_explicit: bool
    video_type: str
    views: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistTracks:
    browse_id: Optional[str]
    results: List[FullTrack]
    params: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistAlbums:
    browse_id: Optional[str]
    results: List[ArtistAlbum]
    params: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistSignles:
    browse_id: Optional[str]
    results: List[ArtistSingle]
    params: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistVideos:
    browse_id: Optional[str]
    results: List[ArtistVideo]
    params: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistRelated:
    browse_id: Optional[str]
    results: List[ArtistRelatedArtist]
    params: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class FullArtist:
    description: str
    views: str
    name: str
    channel_id: str
    shuffle_id: Optional[str]
    radio_id: Optional[str]
    subscribers: str
    subscribed: bool
    thumbnails: List[Image]
    tracks: ArtistTracks
    albums: ArtistAlbums
    singles: ArtistAlbums
    videos: ArtistVideos
    related: ArtistRelated
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class FullPlaylist: ...


@dataclass(repr=False)
class FullVideo: ...
