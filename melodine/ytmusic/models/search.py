from dataclasses import dataclass
from typing import List, Optional, Union

from melodine.base.misc import SearchResultsBase
from melodine.utils import slots
from melodine.ytmusic.models.album import SearchAlbum, TopResultAlbum
from melodine.ytmusic.models.artist import SearchArtist, TopResultArtist
from melodine.ytmusic.models.playlist import SearchPlaylist
from melodine.ytmusic.models.track import SearchTrack, TopResultTrack
from melodine.ytmusic.models.video import SearchVideo, TopResultVideo


@dataclass(repr=False, frozen=True)
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

    __slots__ = slots(__annotations__)


# @dataclass(repr=False, frozen=True)
# class MoreFromYouTube:
#     category: Optional[str]
#     result_type: Optional[str]
#     title: Optional[str]
#     album: Optional[PartialAlbum]
#     feedback_tokens: Optional[FeedbackTokens]
#     video_id: Optional[str]
#     video_type: Optional[str]
#     duration: Optional[str]
#     year: Optional[str]
#     artists: Optional[List[PartialArtist]]
#     duration_seconds: Optional[int]
#     is_explicit: Optional[bool]
#     images: Optional[List[Image]]
