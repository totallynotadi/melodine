from functools import cached_property
from typing import List, Optional, Union

from melodine.base.misc import URIBase
from melodine.base.track import TrackBase
from melodine.utils import Image
from melodine.ytmusic.models.misc_models import AlbumTrack
from melodine.ytmusic.models.search_models import SearchTrack
from melodine.ytmusic.models.top_result_models import TopResultTrack
from melodine.ytmusic.views.album import YTMusicAlbum
from melodine.ytmusic.views.artist import YTMusicArtist
from melodine.ytmusic.views.search import search


class YTMusicTrack(TrackBase, URIBase):
    def __init__(
        self,
        data: Union[TopResultTrack, SearchTrack, AlbumTrack],
    ) -> None:
        super().__init__()
        self.__base_data = data
        self.__album: Optional[YTMusicAlbum] = None

    @classmethod
    def from_id(cls, id: str) -> "YTMusicTrack":
        raise NotImplementedError()

    @classmethod
    def from_uri(cls, uri: str) -> "YTMusicTrack":
        raise NotImplementedError()

    @classmethod
    def from_album(
        cls,
        data: Union[TopResultTrack, SearchTrack, AlbumTrack],
        album: Union[YTMusicAlbum],
    ) -> "YTMusicTrack":
        track = cls(data)
        track.__album = album
        return track

    @cached_property
    def id(self) -> str:
        return self.__base_data.video_id

    @cached_property
    def name(self) -> str:
        return self.__base_data.title

    @cached_property
    def href(self) -> str:
        return "https://music.youtube.com/watch?v=" + self.id

    @cached_property
    def uri(self) -> str:
        return "ytmusic:track:" + self.id

    @cached_property
    def explicit(self) -> bool:
        if not isinstance(self.__base_data, TopResultTrack):
            return self.__base_data.is_explicit
        return False

    @cached_property
    def duration(self) -> str:
        return self.__base_data.duration

    @cached_property
    def images(self) -> List[Image]:
        return self.__base_data.thumbnails

    @cached_property
    def artists(self) -> List[YTMusicArtist]:
        return [YTMusicArtist(artist) for artist in self.__base_data.artists]

    @cached_property
    def album(self) -> YTMusicAlbum:
        print(self.__base_data.album)
        if not isinstance(self.__base_data, AlbumTrack):
            return YTMusicAlbum(self.__base_data.album)
        elif self.__album is not None:
            return self.__album
        else:
            raise ValueError("Album not available for Track: ", self)

    @cached_property
    def url(self) -> str:
        raise NotImplementedError

    @cached_property
    def get_recommendations(self):
        return NotImplementedError()


if __name__ == "__main__":
    srch = search("eiji")
    ytmtrack = YTMusicTrack(srch.tracks[0])

    print("\n", ytmtrack.album)
    print(ytmtrack.artists)
    print(ytmtrack.duration)
    print(ytmtrack.explicit)
    print(ytmtrack.name)
    print(ytmtrack.id)
    print(ytmtrack.href)
    print(ytmtrack.images)
    print(ytmtrack.uri)

    print(dir(ytmtrack))
