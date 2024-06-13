from functools import cached_property
from typing import List, Union

from melodine.base.album import AlbumBase
from melodine.base.misc import URIBase
from melodine.services import service
from melodine.utils import Image
from melodine.ytmusic.models.full_models import FullAlbum
from melodine.ytmusic.models.misc_models import AlbumTrack
from melodine.ytmusic.models.partial_models import PartialAlbum, PartialArtist
from melodine.ytmusic.models.search_models import SearchAlbum
from melodine.ytmusic.models.top_result_models import TopResultAlbum
from melodine.ytmusic.utils import model_item


class YTMusicAlbum(AlbumBase, URIBase):
    def __init__(
        self, data: Union[PartialAlbum, TopResultAlbum, SearchAlbum, FullAlbum]
    ) -> None:
        super().__init__()
        self.__data: FullAlbum
        self.__base_data = data

        self.__id: str

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

    def __get_data(self) -> FullAlbum:
        if not isinstance(self.__base_data, FullAlbum):
            self.__data = model_item(
                service.ytmusic.get_album(self.id),
                model_type=FullAlbum,
            )
        return self.__data

    @cached_property
    def id(self) -> str:
        if isinstance(self.__base_data, PartialAlbum):
            self.__id = self.__base_data.id
        elif isinstance(self.__base_data, (TopResultAlbum, SearchAlbum)):
            self.__id = self.__base_data.browse_id
        elif isinstance(self.__base_data, FullAlbum):
            if self.__id is not None:
                self.__id = service.ytmusic.get_album_browse_id(
                    self.__base_data.audio_playlist_id
                )
        if self.__id is None:
            raise ValueError("Could not resolve album ID.")
        return self.__id

    @cached_property
    def name(self) -> str:
        return (
            self.__base_data.name
            if isinstance(self.__base_data, PartialAlbum)
            else self.__base_data.title
        )

    @cached_property
    def href(self) -> str:
        return "https://music.youtube.com/playlist?list=" + self.audio_playlist_id

    @cached_property
    def uri(self) -> str:
        return "ytmusic:album:" + self.id

    @cached_property
    def audio_playlist_id(self) -> str:
        """`
        the `audio_playlist_id` is used to get the recommended items related to a song/video from ytmusic using `get_song_related(audio_playlist_id)`
        """
        if isinstance(self.__base_data, FullAlbum):
            return self.__base_data.audio_playlist_id
        return self.__get_data().audio_playlist_id

    @cached_property
    def type(self):
        if isinstance(self.__base_data, (TopResultAlbum, FullAlbum)):
            return self.__base_data.type
        return self.__get_data().type

    @cached_property
    def year(self) -> str:
        if isinstance(self.__base_data, (FullAlbum, SearchAlbum)):
            return self.__base_data.year
        return self.__get_data().year

    @cached_property
    def total_tracks(self) -> int:
        if isinstance(self.__base_data, FullAlbum):
            return self.__base_data.duration_seconds
        return self.__get_data().duration_seconds

    @cached_property
    def duration(self) -> str:
        if isinstance(self.__base_data, (SearchAlbum, FullAlbum)):
            if self.__base_data.duration is not None:
                return self.__base_data.duration
            else:
                pass
        return self.__get_data().duration

    @cached_property
    def images(self) -> List[Image]:
        if not isinstance(self.__base_data, PartialAlbum):
            return self.__base_data.thumbnails
        return self.__get_data().thumbnails

    @cached_property
    def artists(self) -> List[PartialArtist]:
        if not isinstance(self.__base_data, PartialAlbum):
            return self.__base_data.artists
        return self.__get_data().artists

    @cached_property
    def tracks(self) -> List[AlbumTrack]:
        if isinstance(self.__base_data, FullAlbum):
            return self.__base_data.tracks
        return self.__get_data().tracks


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
