from typing import List, Optional, Union

from melodine.base.album import AlbumBase
from melodine.base.misc import URIBase
from melodine.services import service
from melodine.utils import Image, transform_field_names
from melodine.ytmusic.models.full_models import FullAlbum
from melodine.ytmusic.models.misc_models import AlbumTrack
from melodine.ytmusic.models.partial_models import PartialAlbum, PartialArtist
from melodine.ytmusic.models.search_models import SearchAlbum
from melodine.ytmusic.models.top_result_models import TopResultAlbum
from melodine.ytmusic.utils import ensure_data, model_item


class YTMusicAlbum(AlbumBase, URIBase):
    def __init__(
        self, data: Union[PartialAlbum, TopResultAlbum, SearchAlbum, FullAlbum]
    ) -> None:
        self.__data: Optional[FullAlbum] = None
        self.__base_data = data

        self.__id: Optional[str] = None

    @classmethod
    def from_id(cls, resource_id: str) -> "YTMusicAlbum":
        raise NotImplementedError()

    @classmethod
    def from_url(cls, url: str) -> "YTMusicAlbum":
        raise NotImplementedError()

    # def __find_album(
    #     self,
    #     artist: PartialArtist,
    #     title: str,
    #     thumbnails: Optional[List[Image]] = None,
    # ) -> SearchAlbum:
    #     """
    #     for cases when an album's `browseId` is not available.

    #     use the present artists's `browseId` to fetch it's data \
    #     and find this given albums among the artist's albums.
    #     """
    #     ...

    def _get_data(self):
        if self.__data is None:
            self.__data = model_item(
                service.ytmusic.get_album(self.id),
                model=FullAlbum,
            )

        return self.__data

    @property
    def id(self) -> str:
        if isinstance(self.__base_data, PartialAlbum):
            self.__id = self.__base_data.id
        elif isinstance(self.__base_data, (TopResultAlbum, SearchAlbum)):
            self.__id = self.__base_data.browse_id
        elif isinstance(self.__base_data, FullAlbum):
            self.__id = service.ytmusic.get_album_browse_id(
                self.__base_data.audio_playlist_id
            )
        if self.__id is None:
            raise ValueError("Could not resolve album ID.")
        return self.__id

    @property
    def name(self) -> str:
        return (
            self.__base_data.name
            if isinstance(self.__base_data, PartialAlbum)
            else self.__base_data.title
        )

    @property
    def href(self) -> str:
        return "https://music.youtube.com/playlist?list=" + self.audio_playlist_id

    @property
    def uri(self) -> str:
        return "ytmusic:album:" + self.id

    @property
    @ensure_data
    def audio_playlist_id(self) -> str:
        """`
        the `audio_playlist_id` is used to get the recommended items related to a song/video from ytmusic using `get_song_related(audio_playlist_id)`
        """
        if self.__data is not None:
            return self.__data.audio_playlist_id
        # cause AttributeError is we're sure that `audio_playlist_id` doesnt exist on `base_data` and `data` is None.
        return self.__base_data.audio_playlist_id

    @property
    @ensure_data
    def type(self):
        if self.__data is not None:
            return self.__data.type
        # cause AttributeError is we're sure that `type` doesnt exist on `base_data` and `data` is None.
        return self.__base_data.type

    @property
    @ensure_data
    def year(self) -> int:
        if self.__data is not None:
            return int(self.__data.year)
        # cause AttributeError is we're sure that `year` doesnt exist on `base_data` and `data` is None.
        return int(self.__base_data.year)

    @property
    @ensure_data
    def total_tracks(self) -> int:
        if self.__data is not None:
            return int(self.__data.track_count)
        # cause AttributeError is we're sure that `track_count` doesnt exist on `base_data` and `data` is None.
        return int(self.__base_data.track_count)

    @property
    @ensure_data
    def duration(self) -> Union[int, str]:
        if self.__data is not None:
            return self.__data.duration_seconds
        # cause AttributeError is we're sure that `duration_seconds` doesnt exist on `base_data` and `data` is None.
        return self.__base_data.duration_seconds

    @property
    @ensure_data
    def images(self) -> List[Image]:
        if self.__data is not None:
            return self.__data.thumbnails
        # cause AttributeError is we're sure that `thumbnails` doesnt exist on `base_data` and `data` is None.
        return self.__base_data.thumbnails

    @property
    @ensure_data
    def artists(self) -> List[PartialArtist]:
        if self.__data is not None:
            return self.__data.artists
        return self.__base_data.artists

    @property
    @ensure_data
    def tracks(self) -> List[AlbumTrack]:
        if self.__data is not None:
            return self.__data.tracks
        return self.__base_data.tracks


if __name__ == "__main__":
    from melodine.ytmusic.views.search import search

    srch = search("sewerslvt", types=["albums"])
    album = srch.albums[0]

    ytmalbum = YTMusicAlbum(data=album)
    print("\n", ytmalbum.artists)
    print(ytmalbum.audio_playlist_id)
    print(ytmalbum.duration)
    print(ytmalbum.href)
    print(ytmalbum.id)
    print(ytmalbum.images)
    print(ytmalbum.name)
    print(ytmalbum.total_tracks)
    print(ytmalbum.tracks)
    print(ytmalbum.type)
    print(ytmalbum.uri)
    print(ytmalbum.year)

    print(dir(ytmalbum))
