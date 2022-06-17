from typing import List, Union

from ..ytmusic.video import Video
from ...utils import YT, YTMUSIC


def search(
    q: str,
    *,
    related_to_video_id: Union[str, None] = None,
    limit: int = 10,
) -> List[Video]:

    data = YT.search(
        q=q,
        related_to_video_id=related_to_video_id,
        limit=limit,
        return_json=True
    )

    return [
        Video(
            YTMUSIC.get_song(video['items'][0]['id']['videoId'])
        ) for video in data['items']
    ]
