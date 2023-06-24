from dataclasses import dataclass
from typing import List, Optional
from melodine.utils import slots

from melodine.ytmusic.models.misc import Image


@dataclass(repr=False, frozen=True)
class PartialPlaylist:
    ...


@dataclass(repr=False, frozen=True)
class SearchPlaylist:
    category: Optional[str]
    result_type: Optional[str]
    title: Optional[str]
    item_count: Optional[str]
    author: Optional[str]
    browse_id: Optional[str]
    thumbnails: Optional[List[Image]]

    __slots__ = slots(__annotations__)


@dataclass(repr=False, frozen=True)
class FullPlaylist:
    ...
