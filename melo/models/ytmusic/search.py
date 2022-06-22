from dataclasses import dataclass, field
from typing import Iterable, List, Literal, Optional, Union

from ...utils import YTMUSIC, SearchResults
from .album import Album
from .artist import Artist
from .playlist import Playlist
from .track import Track
from .video import Video

__all__ = ['search']

_TYPES = {"artist": Artist, "album": Album,
          "track": Track, "video": Video, "playlist": Playlist}
_SEARCH_TYPES = {"artist", "album", "track", "video", "playlist"}


@dataclass
class YTMSearchResults(SearchResults):
    '''a dataclass of search results

    extends from the base SearchResults class to add some parameters

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

    videos: Optional[List] = field(default_factory=list)


def search(
    q: str,  # pylint: disable=invalid-name
    *,
    types: Union[Iterable[Literal['track', 'video',
                                  'artist', 'album', 'playlist']], None] = None,
    limit: Optional[int] = 10,
) -> YTMSearchResults:
    '''Get search results for a query'''

    # types = [type_ + 's' for type_ in types]

    if types:

        if not hasattr(types, "__iter__"):
            raise TypeError("types must be an iterable.")

        types_ = set(types)

        if not types_.issubset(_SEARCH_TYPES):
            raise ValueError('Bad queary type! got "%s" expected any of: track, playlist, artist, album, video' %
                             types_.difference(_SEARCH_TYPES).pop())

        if 'track' in types:
            types = list(types)
            if 'track' in types:
                track_index = types.index('track')
                types.remove('track')
                types.insert(track_index, 'song')
            types_ = set(types)
        
        types_ = [type_+'s' for type_ in types_]
        print(types_)

        results = []
        # print('::from types')
        for idx, type_ in enumerate(types_):
            # print(f'::limit {((limit // len(types)) + 1) if idx + 1 == len(types) and len(types) % 2 == 1 else (limit // len(types))}')
            # print(f'::type {type_}')
            data = YTMUSIC.search(
                q,
                filter=type_,
                limit=((limit // len(types)) + 1)
                if idx + 1 == len(types) and len(types) % 2 == 1
                else (limit // len(types))
            )
            results.extend(data)
            print(f'::: {type_}{results}\n\n')
    else:
        results = YTMUSIC.search(q, limit=limit)

    search_results = {}
    for search_type in _SEARCH_TYPES:
        search_results[search_type + 's'] = []
        for result in results:
            if result['resultType'] == search_type or (result['resultType'] == 'song' and search_type == 'track'):
                print(result['resultType'], '-', search_type)
                print(_TYPES[search_type])
                if result['resultType'] == search_type == 'artist':
                    print(result)
                search_results[
                    search_type + 's'
                ].append(_TYPES[search_type](data=result))
                # print(search_results)

    return YTMSearchResults(**search_results)
