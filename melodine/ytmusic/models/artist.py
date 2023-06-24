from dataclasses import dataclass
from typing import List, Optional
from melodine.utils import slots

from melodine.ytmusic.models.misc import Image


@dataclass(repr=False, frozen=True)
class PartialArtist:
    name: Optional[str]
    id: Optional[str]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class TopResultArtist:
    category: Optional[str]
    result_type: Optional[str]
    subscribers: Optional[str]
    artists: Optional[List[PartialArtist]]
    thumbnails: Optional[List[Image]]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class SearchArtist:
    category: Optional[str]
    result_type: Optional[str]
    artist: Optional[str]
    shuffle_id: Optional[str]
    radio_id: Optional[str]
    browse_id: Optional[str]
    thumbnails: Optional[List[Image]]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class FullArtist:
    ...
