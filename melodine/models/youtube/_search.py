from typing import Any, List, Union

from melodine.models.ytmusic import Video
from melodine.configs import YT


def search(
    q: str,  #pylint: disable=invalid-name
    *,
    related_to_video_id: Union[str, None] = None,
    limit: int = 10,
) -> List[Video]:

    result: List[Union[Video, Any]] = []

    data = YT.search(
        q=q,
        related_to_video_id=related_to_video_id,
        limit=limit,
        return_json=True
    )

    for video in data['items']:
        video['snippet']['videoId'] = video['id']['videoId']
        if 'thumbnails' in video['snippet']:
            video['snippet']['thumbnails'] = list(video['snippet']['thumbnails'].values())
        video = Video(video['snippet'])
        result.append(video)

    return result
