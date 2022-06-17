from typing import Iterable, Literal, Optional, Union

from .domains import spotify, ytmusic
from .utils import SearchResults

__all__ = ['search']


def search(
    q: str,  # pylint: disable=invalid-name
    *,
    source: Optional[Union[Iterable[Literal['spotify', 'ytmusic']], None]] = None,
    types: Optional[Iterable[Literal['track',
                                     'artist', 'album', 'playlist']]] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
):
    '''Get search results from spotify as well as ytmusic.

    The query is primarily searched on spotify, then on ytmusic if spotify returns an empty response
    '''

    result: SearchResults = SearchResults()

    if source:
        for src in source:
            if src == 'spotify':
                data = spotify.search(
                    q=q, types=types, limit=limit, offset=offset)
                result += data
            if src == 'ytmusic':
                data = ytmusic.search(q=q, types=types, limit=limit)
                result += data
    else:
        data = spotify.search(q=q, types=types, limit=limit, offset=offset)
        print(bool(data))
        if not data:
            data = ytmusic.search(q=q, types=types, limit=limit)
        result = data
    return result
