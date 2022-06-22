from typing import Iterable

from ...utils import SPOTIFY, SearchResults
from . import (
    Artist,
    Album,
    Track,
    Playlist,
    Episode,
    Show
)


__all__ = ["search"]

_TYPES = {"artist": Artist, "album": Album, "track": Track,
          "playlist": Playlist, "show": Show, "episode": Episode}
_SEARCH_TYPES = {"artist", "album", "track", "playlist", "show", "episode"}


def search(
    q: str,  # pylint: disable=invalid-name
    *,
    types: Iterable[str] = ("track", "playlist", "artist", "album", "show", "episode"),
    limit: int = 20,
    offset: int = 0,
) -> SearchResults:
    '''Get search results for a query'''

    if types is None:
        types = ("track", "playlist", "artist", "album", "show", "episode")

    if not hasattr(types, "__iter__"):
        raise TypeError("types must be an iterable.")

    types_ = set(types)

    if not types_.issubset(_SEARCH_TYPES):
        raise ValueError('Bad queary type! got "%s" expected any of: track, playlist, artist, album' %
                         types_.difference(_SEARCH_TYPES).pop())

    query_type = ",".join(tp.strip() for tp in types)

    data = SPOTIFY.search(
        q=q,
        limit=limit,
        offset=offset,
        type=query_type,
    )

    return SearchResults(
        **{
            key: [_TYPES[_val['type']](_val) for _val in value['items']]
            for key, value in data.items()
        }
    )
