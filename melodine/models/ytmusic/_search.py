from dataclasses import dataclass, field
from itertools import groupby
from typing import Iterable, List, Literal, Optional, Union

from melodine.services import service
from melodine.models.ytmusic import Album, Artist, Playlist, Track, Video
from melodine.utils import SearchResults

__all__ = ["search"]

_TYPES = {
    "artist": Artist,
    "album": Album,
    "song": Track,
    "video": Video,
    "playlist": Playlist,
}
_SEARCH_TYPES = {"artists", "albums", "tracks", "videos", "playlists"}


@dataclass
class YTMusicSearchResults(SearchResults):
    """A dataclass for YTMusic Search Results

    Inherits from the SearchResultsBase class for.
    """

    top_result: Optional[Union[Track, Artist, Album]] = field(default_factory=list)
    more_from_youtube: Optional[List[Union[Track, Artist, Album]]] = field(
        default_factory=list
    )

    tracks: Optional[List[Track]] = field(default_factory=list)
    videos: Optional[List[Video]] = field(default_factory=list)
    albums: Optional[List[Album]] = field(default_factory=list)
    playlists: Optional[List[Playlist]] = field(default_factory=list)
    artists: Optional[List[Artist]] = field(default_factory=list)


def search(
    q: str,
    *,
    types: Optional[
        Iterable[Literal["tracks", "videos", "albums", "artists", "playlists"]]
    ] = [],
    limit: Optional[int] = 20,
) -> YTMusicSearchResults:
    data = []

    if types:
        if not hasattr(types, "__iter__"):
            raise TypeError("types must be an iterable.")

        types = set(types)

        if not types.issubset(_SEARCH_TYPES):
            raise ValueError(
                'Bad queary type! got "%s" expected one or more of: tracks, playlists, artists, albums, videos'
                % types.difference(_SEARCH_TYPES).pop()
            )

        if "tracks" in types:
            types.remove("tracks")
            types.add("songs")

        for type in types:
            results = service.ytmusic.search(q, filter=type, limit=limit)
            data.extend(results)
    else:
        results = service.ytmusic.search(q, limit=limit)
        data.extend(results)

    data = groupby(data, lambda x: x["category"])
    search_results = {}

    for key, val in data:
        new_key = (
            "More from YouTube"
            if key is None
            else "Playlists"
            if key == "Community playlists"
            else "Tracks"
            if key == "Songs"
            else key
        )
        search_results["_".join(new_key.lower().split(" "))] = list(val)

    return YTMusicSearchResults(
        **{
            key: [
                _TYPES[_val["resultType"]](_val)
                if _val["resultType"] != "artist"
                else (
                    _TYPES[_val["resultType"]].from_search(_val)
                    if "browseId" in _val
                    else _TYPES[_val["resultType"]].partial(_val["artists"][0])
                )
                for _val in value
            ]
            for key, value in search_results.items()
        }
    )
