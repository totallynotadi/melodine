from dataclasses import dataclass, field
from itertools import groupby
from typing import Iterable, List, Literal, Optional

from melodine.configs import YTMUSIC
from melodine.models.ytmusic import Album, Artist, Playlist, Track, Video
from melodine.utils import SearchResults

__all__ = ['search']

_TYPES = {"artist": Artist, "album": Album,
          "song": Track, "video": Video, "playlist": Playlist}
_SEARCH_TYPES = {"artists", "albums", "tracks", "videos", "playlists"}


@dataclass
class YTMusicSearchResults(SearchResults):
    ''' A dataclass for Search Results

    Inherits from the SearchResultsBase class for.

    Attributes
    ----------
    artists : List[:class:`Artist`]
        The artists of the search.
    playlists : List[:class:`Playlist`]
        The playlists of the search.
    albums : List[:class:`Album`]
        The albums of the search.
    tracks : List[:class:`Track`]
        The tracks of the search.
    videos: List[:class:`Video`]
        The videos from the search results
    '''

    tracks: Optional[List[Track]] = field(default_factory=list)
    albums: Optional[List[Album]] = field(default_factory=list)
    artists: Optional[List[Artist]] = field(default_factory=list)
    playlists: Optional[List[Playlist]] = field(default_factory=list)

    videos: Optional[List[Video]] = field(default_factory=list)


def search(
    q: str,
    *,
    types: Optional[Iterable[Literal['tracks', 'videos',
                                     'albums', 'artists', 'playlists']]] = [],
    limit: Optional[int] = 15,
) -> YTMusicSearchResults:

    data = []

    if types:

        if not hasattr(types, "__iter__"):
            raise TypeError("types must be an iterable.")

        types = set(types)

        if not types.issubset(_SEARCH_TYPES):
            raise ValueError('Bad queary type! got "%s" expected one or more of: tracks, playlists, artists, albums, videos' %
                             types.difference(_SEARCH_TYPES).pop())

        if 'tracks' in types:
            types.remove('tracks')
            types.add('songs')

        for type in types:
            results = YTMUSIC.search(
                q,
                filter=type,
                limit=limit
            )
            data.extend(results)
    else:
        results = YTMUSIC.search(q)
        data.extend(results)

    search_results = dict.fromkeys(_SEARCH_TYPES, [])
    def key_func(x): return x['resultType']
    for key, value in groupby(sorted(data, key=key_func), key_func):
        search_results[key + 's'] = list(value)

    search_results['tracks'] = search_results.pop('songs', [])

    return YTMusicSearchResults(
        **{
            ('tracks' if key == 'song' else key if key.endswith('s') else key + 's'): [
                _TYPES[_val['resultType']](_val)
                if _val['resultType'] != 'artist'
                else _TYPES[_val['resultType']].from_search(_val)
                for _val in value
            ]
            for key, value in search_results.items()
        }
    )
