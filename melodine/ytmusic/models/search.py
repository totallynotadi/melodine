from dataclasses import dataclass
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


@dataclass
class YTMusicSearchResults(SearchResultsBase):
    top_result: Optional[
        List[Union[TopResultTrack, TopResultAlbum, TopResultArtist, TopResultVideo]]
    ]
    more_from_youtube: Optional[
        List[Union[SearchTrack, SearchArtist, SearchAlbum, SearchVideo, SearchPlaylist]]
    ] 
    tracks: Optional[List[SearchTrack]]
    videos: Optional[List[SearchVideo]]
    playlists: Optional[List[SearchPlaylist]]
    albums: Optional[List[SearchAlbum]]
    artists: Optional[List[SearchArtist]]
