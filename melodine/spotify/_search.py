from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from melodine.base.misc import SearchResultsBase
from melodine.services import service
from melodine.spotify import Album, Artist, Episode, Playlist, Show, Track

__all__ = ["search"]

_TYPES = {
    "artist": Artist,
    "album": Album,
    "track": Track,
    "playlist": Playlist,
    "show": Show,
    "episode": Episode,
}
_SEARCH_TYPES = {"artists", "albums", "tracks", "playlists", "shows", "episodes"}


@dataclass(repr=False, frozen=True)
class SpotifySearchResults(SearchResultsBase):
    """A dataclass for Spotify Search Results

    Inherits from the base SearchResults class.

    Attributes
    ----------
    `artists` - `List[Artist]`
        A list of all the artists in the search results.

    `playlists` - `List[Playlist]`
        A list of all the playlists in the search results.

    `albums` - `List[Album]`
        A list of all the albums in the search results.

    `tracks` - `List[Track]`
        A list of all the tracks in the search results.

    `shows` - `List[Show]`
        A list of all the shows in the search results.

    `episodes` - `List[Episode]`
        A list of all the episodes in the search results.
    """

    artists: List[Artist] = field(default_factory=list)
    playlists: List[Playlist] = field(default_factory=list)
    albums: List[Album] = field(default_factory=list)
    tracks: List[Track] = field(default_factory=list)

    shows: List[Show] = field(default_factory=list)
    episodes: List[Episode] = field(default_factory=list)


def search(
    q: str,  # pylint: disable=invalid-name
    *,
    types: Iterable[str] = (
        "tracks",
        "playlists",
        "artists",
        "albums",
        "shows",
        "episodes",
    ),
    limit: int = 20,
    offset: int = 0,
) -> SpotifySearchResults:
    """Get search results for a query"""

    if types is None:
        types = ("track", "playlists", "artists", "albums", "shows", "episodes")

    if not hasattr(types, "__iter__"):
        raise TypeError("types must be an iterable.")

    types_ = set(types)

    if not types_.issubset(_SEARCH_TYPES):
        raise ValueError(
            'Bad queary type! got "%s" expected any of: tracks, playlists, artists, albums, shows, episodes'
            % types_.difference(_SEARCH_TYPES).pop()
        )

    types = list(map(lambda type: type[:-1] if type.endswith("s") else type, types))

    query_type = ",".join(tp.strip() for tp in types)

    data = service.spotify.search(
        q=q,
        limit=limit,
        offset=offset,
        type=query_type,
    )

    return SpotifySearchResults(
        **{
            key: [
                _TYPES[_val["type"]](_val)
                for _val in (
                    value["items"] if len(list(filter(None, value["items"]))) else []
                )
            ]
            for key, value in data.items()
        }
    )
