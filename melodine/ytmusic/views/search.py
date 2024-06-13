from typing import Iterable, Literal

import dacite

from melodine.services import service
from melodine.ytmusic.models.search_result_model import YTMusicSearchResults
from melodine.ytmusic.utils import model_search_results

_SEARCH_TYPES = {"artists", "albums", "tracks", "videos", "playlists"}


def search(
    q: str,
    types: Iterable[
        Literal["tracks", "songs", "videos", "albums", "artists", "playlists"]
    ] = [],
    limit: int = 20,
) -> YTMusicSearchResults:
    search_results = []

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
            search_results.extend(results)
    else:
        results = service.ytmusic.search(q, limit=limit)
        search_results.extend(results)

    ## TODO: we're not supporting Podcasts and User Profiles on YTMusic yet.
    search_results = list(
        filter(
            lambda x: x["category"] not in ["Profiles", "Episodes", "Podcasts"],
            search_results,
        )
    )
    for result in search_results:
        if "resultType" in result:
            # hacky fix
            if result["resultType"] == "album":
                result["artists"] = list(
                    filter(lambda x: x["id"] is not None, result.pop("artists"))
                )

    # print(search_results)

    modeled_search_results = model_search_results(search_results)

    return dacite.from_dict(
        data_class=YTMusicSearchResults, data=modeled_search_results
    )
