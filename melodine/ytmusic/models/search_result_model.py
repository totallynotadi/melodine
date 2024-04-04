from dataclasses import dataclass, field
from typing import List, Optional, Union

from melodine.base.misc import SearchResultsBase
from melodine.ytmusic.models.search_models import (
    SearchAlbum,
    SearchArtist,
    SearchPlaylist,
    SearchTrack,
    SearchVideo,
)
from melodine.ytmusic.models.top_result_models import (
    TopResultAlbum,
    TopResultArtist,
    TopResultTrack,
    TopResultVideo,
)


@dataclass(frozen=True)
class YTMusicSearchResults(SearchResultsBase):
    top_result: Optional[
        List[Union[TopResultTrack, TopResultAlbum, TopResultArtist, TopResultVideo]]
    ]
    more_from_youtube: Optional[
        List[Union[SearchTrack, SearchArtist, SearchAlbum, SearchVideo, SearchPlaylist]]
    ]
    tracks: List[SearchTrack] = field(default_factory=list)
    videos: List[SearchVideo] = field(default_factory=list)
    playlists: List[SearchPlaylist] = field(default_factory=list)
    albums: List[SearchAlbum] = field(default_factory=list)
    artists: List[SearchArtist] = field(default_factory=list)
