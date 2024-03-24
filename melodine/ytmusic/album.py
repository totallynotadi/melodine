from typing import Callable, List, Optional, Union

from melodine.base.album import AlbumBase
from melodine.base.misc import URIBase
from melodine.services import service
from melodine.utils import Image
from melodine.ytmusic._artist import YTMusicArtist
from melodine.ytmusic.models.full_models import FullAlbum
from melodine.ytmusic.models.partial_models import PartialAlbum, PartialArtist
from melodine.ytmusic.models.search_models import SearchAlbum
from melodine.ytmusic.models.top_result_models import TopResultAlbum
from melodine.ytmusic.track import YTMusicTrack


class YTMusicAlbum(AlbumBase, URIBase):
    def __init__(
        self, data: Union[PartialAlbum, TopResultAlbum, SearchAlbum, FullAlbum]
    ) -> None:
        self.__data: Optional[FullAlbum] = {}
        self.__base_data = data

        self.__id: Optional[str] = None

    @classmethod
    def from_id(cls, resource_id: str) -> "YTMusicAlbum":
        pass

    @classmethod
    def from_url(cls, url: str) -> "YTMusicAlbum":
        pass

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

    def __get_data(self):
        if self.__data is None:
            self.__data = service.ytmusic.get_album(self.id)
        return self.__data

    def __ensure_data(func: Callable):
        print("lmao")

        def inner(self):
            try:
                print(f"passed function inside try: {func} {self}")
                func_return = func(self)
                if func_return is None:
                    self.__get_data()
                    func_return = func()
                    return func_return
                return func_return
            except AttributeError:
                print("inside except")
                self.__get_data()
                func_return = func()
                return func_return

        return inner

    @property
    def id(self) -> str:
        self.__id = self.__base_data.browse_id or self.__base_data.id
        if self.__id is None:
            if self.__base_data.audio_playlist_id:
                self.__id = service.ytmusic.get_album_browse_id(
                    self.__data.audio_playlist_id
                )
            # uncomment this later when __find_album is implemented
            # else:
            #     self.__base_data = self.__find_album(
            #         self.__base_data.artists[0],
            #         self.__base_data.title,
            #         self.__base_data.thumbnails,
            #     )
            #     self.__id = self.__base_data.id or self.__base_data.browse_id
        return self.__id

    @property
    def name(self) -> str:
        return self.__base_data.name or self.__base_data.title

    @property
    def href(self) -> str:
        return "https://music.youtube.com/playlist?list=" + self.audio_playlist_id

    @property
    def uri(self) -> str:
        return "ytmusic:album:" + self.id

    @property
    @__ensure_data
    def audio_playlist_id(self) -> str:
        return self.__base_data.audio_playlist_id or self.__data.audio_playlist_id
        # return self.__base_data.audio_playlist_id

    @property
    @__ensure_data
    def type(self):
        return self.__base_data.type or self.__data.type

    @property
    @__ensure_data
    def year(self) -> int:
        return self.__base_data.year or self.__data.year

    @property
    @__ensure_data
    def total_tracks(self) -> int:
        return self.__base_data.track_count or self.__data.track_count

    @property
    @__ensure_data
    def duration(self) -> Union[int, str]:
        # or self.__base_data.duration
        return self.__base_data.duration_seconds or self.__data.duration_seconds

    @property
    @__ensure_data
    def images(self) -> List[Image]:
        return self.__base_data.thumbnails or self.__data.thumbnails

    @property
    @__ensure_data
    def artists(self) -> List[YTMusicArtist]:
        return

    @property
    @__ensure_data
    def tracks(self) -> List[YTMusicTrack]:
        return


if __name__ == "__maim__":
    from melodine.ytmusic.search import search

    album = search("sewerslvt", types=["albums"]).albums[0]
    ytmalbum = YTMusicAlbum(data=album)
    print(ytmalbum.audio_playlist_id)
    # dir(ytmalbum)
