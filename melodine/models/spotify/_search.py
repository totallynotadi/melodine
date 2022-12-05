from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from melodine.utils import SearchResults
from melodine.configs import SPOTIFY
from melodine.models.spotify import (
    Album,
    Artist,
    Episode,
    Playlist,
    Show,
    Track
)

__all__ = ["search"]

_TYPES = {"artist": Artist, "album": Album, "track": Track,
          "playlist": Playlist, "show": Show, "episode": Episode}
_SEARCH_TYPES = {"artists", "albums", "tracks", "playlists", "shows", "episodes"}

@dataclass
class SpotifySearchResults(SearchResults):
    ''' A dataclass for Search Results

    Inherits from the base SearchResults class.

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
    
    artists: Optional[List[Artist]] = field(default_factory=list)
    albums: Optional[List[Album]] = field(default_factory=list)
    tracks: Optional[List[Track]] = field(default_factory=list)
    playlists: Optional[List[Playlist]] = field(default_factory=list)

    shows: Optional[List[Show]] = field(default_factory=list)
    episodes: Optional[List[Episode]] = field(default_factory=list)


def search(
    q: str,  # pylint: disable=invalid-name
    *,
    types: Iterable[str] = ("tracks", "playlists", "artists", "albums", "shows", "episodes"),
    limit: int = 20,
    offset: int = 0,
) -> SpotifySearchResults:
    '''Get search results for a query'''

    if types is None:
        types = ("track", "playlists", "artists", "albums", "shows", "episodes")

    if not hasattr(types, "__iter__"):
        raise TypeError("types must be an iterable.")

    types_ = set(types)

    if not types_.issubset(_SEARCH_TYPES):
        raise ValueError('Bad queary type! got "%s" expected any of: tracks, playlists, artists, albums, shows, episodes' %
                         types_.difference(_SEARCH_TYPES).pop())

    types = list(map(lambda type: type[:-1] if type.endswith('s') else type, types))
    
    query_type = ",".join(tp.strip() for tp in types)

    data = SPOTIFY.search(
        q=q,
        limit=limit,
        offset=offset,
        type=query_type,
    )

    return SpotifySearchResults(
        **{
            key: [_TYPES[_val['type']](_val) for _val in value['items']]
            for key, value in data.items()
        }
    )
