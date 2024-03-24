from dataclasses import dataclass
from typing import Any, List, Optional

from melodine.utils import Image, slots
from melodine.ytmusic.models.misc_models import (
    AlbumTrack,
    ArtistAlbum,
    ArtistRelatedArtists,
    ArtistVideo,
    FeedbackTokens,
    LikeStatus,
)
from melodine.ytmusic.models.partial_models import PartialAlbum, PartialArtist

__all__ = ["FullAlbum", "FullArtist", "FullPlaylist", "FullVideo"]


@dataclass(repr=False)
class FullAlbum:
    title: str
    type: str
    thumbnails: List[Image]
    artists: List[PartialArtist]
    year: Optional[str]
    track_count: int
    duration: Optional[str]
    audio_playlist_id: str
    tracks: List[AlbumTrack]
    duration_seconds: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class FullTrack:
    video_id: str
    title: str
    artists: List[PartialArtist]
    album: PartialAlbum
    like_status: LikeStatus
    thumbnails: List[Image]
    is_available: bool
    is_explicit: bool
    video_type: str
    duration: Optional[str]
    duration_seconds: Optional[int]
    feedback_tokens: FeedbackTokens
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistTracks:
    browse_id: str
    results: List[FullTrack]
    params: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistAlbums:
    browse_id: str
    results: List[ArtistAlbum]
    params: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistSingles:
    browse_id: str
    results: List[ArtistAlbum]
    params: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistVideos:
    browse_id: str
    results: List[ArtistVideo]
    params: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class ArtistRelated:
    browse_id: str
    results: List[ArtistRelatedArtists]
    params: Optional[str]
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class FullArtist:
    description: str
    views: str
    name: str
    channel_id: str
    shuffle_id: str
    radio_id: str
    subscribers: str
    subscribed: bool
    thumbnails: List[Image]
    songs: ArtistTracks
    albums: ArtistAlbums
    singles: ArtistSingles
    videos: ArtistVideos
    related: ArtistRelated
    __slots__ = slots(__annotations__)


@dataclass(repr=False)
class FullPlaylist: ...


@dataclass(repr=False)
class FullVideo: ...
