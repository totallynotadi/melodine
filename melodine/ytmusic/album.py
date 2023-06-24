from typing import Optional, Union
from melodine.base.album import AlbumBase
from melodine.base.misc import URIBase
from melodine.utils import singleton
from melodine.ytmusic.models.album import (
    PartialAlbum,
    TopResultAlbum,
    SearchAlbum,
    FullAlbum,
)


@singleton
class YTMusicAlbum(AlbumBase):
    def __init__(
        self, data: Union[PartialAlbum, TopResultAlbum, SearchAlbum, FullAlbum]
    ) -> None:
        self.__data: Optional[FullAlbum] = None
        self.__base_data = data

    def __get_data(self):
        pass

    def __ensure_data(self, func):
        def inner(*args, **kwargs):
            try:
                func_return = func()
                return func_return
            except Exception as e:
                self.__get_data()
                func_return = func()
                return func_return

        return inner
