from typing import List, Optional, Union
from melodine.services import service
from melodine.base.album import AlbumBase
from melodine.base.misc import URIBase
from melodine.utils import singleton
from melodine.ytmusic.artist import YTMusicArtist
from melodine.ytmusic.models.album import (
    PartialAlbum,
    TopResultAlbum,
    SearchAlbum,
    FullAlbum,
)
from melodine.ytmusic.models.artist import PartialArtist
from melodine.ytmusic.models.misc import Image


@singleton
class YTMusicAlbum(AlbumBase, URIBase):
    def __init__(
        self, data: Union[PartialAlbum, TopResultAlbum, SearchAlbum, FullAlbum]
    ) -> None:
        self.__data: Optional[FullAlbum] = None
        self.__base_data = data

        self.__id: Optional[str] = None
        self.__year: Optional[str] = self.__base_data.year

    @classmethod
    def from_id(cls, id: str) -> "YTMusicAlbum":
        ...

    @classmethod
    def from_url(cls, url: str) -> "YTMusicAlbum":
        ...

    def __find_album(
        artist: PartialArtist, title: str, thumbnails: Optional[List[Image]] = None
    ) -> SearchAlbum:
        ...

    def __get_data(self):
        if self.__data is None:
            self.__data = service.ytmusic.get_album(self.id)
        return self.__data

    def __ensure_data(func):

        def inner(self):
            try:
                func_return = func(self)
                if func_return is None:
                    self.__get_data()
                    func_return = func()
                    return func_return
                return func_return
            except AttributeError:
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
            else:
                self.__base_data = self.__find_album(self.__base_data.artists[0])
                self.__id = self.__base_data.id or self.__base_data.browse_id
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
        return self.__base_data.audio_playlist_id or self.__base_data.audio_playlist_id

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
        return (
            self.__base_data.duration_seconds
            or self.__data.duration_seconds
            or self.__base_data.duration
        )

    @property
    @__ensure_data
    def images(self) -> List[Image]:
        return self.__base_data.thumbnails or self.__data.thumbnails

    @property
    @__ensure_data
    def artists(self) -> List[YTMusicArtist]:
        return
