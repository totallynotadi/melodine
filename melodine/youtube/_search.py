from typing import Any, List, Optional, Union
from dataclasses import dataclass, field

from melodine.ytmusic import Video

from melodine.services import service
from melodine.base.misc import SearchResultsBase


@dataclass(frozen=True)
class YoutubeSearchResults(SearchResultsBase):
    """A dataclass for Search Results

    Inherits from the base SearchResults class.

    Attributes
    ----------

    videos: List[`:class:Video`]
        The videos from the search results
    """

    videos: List[Video] = field(default_factory=list)


def search(
    q: str,  # pylint: disable=invalid-name
    *,
    related_to_video_id: Union[str, None] = None,
    limit: int = 10,
) -> List[Video]:
    result: List[Union[Video, Any]] = []

    data = service.yt.search(
        q=q, related_to_video_id=related_to_video_id, limit=limit, return_json=True
    )

    for video in data["items"]:
        video_kind = video["id"]["kind"].split("#")[1]
        if video_kind == "video":
            video["snippet"]["videoId"] = video["id"]["videoId"]
            if "thumbnails" in video["snippet"]:
                video["snippet"]["thumbnails"] = list(
                    video["snippet"]["thumbnails"].values()
                )
            video = Video(video["snippet"])
            result.append(video)

    return YoutubeSearchResults(videos=result)
