from functools import cached_property
from typing import List, Optional, Union

from melodine.base.artist import ArtistBase
from melodine.base.misc import URIBase
from melodine.services import service
from melodine.utils import Image
from melodine.ytmusic.models.full_models import (
    ArtistAlbums,
    ArtistRelated,
    ArtistTracks,
    ArtistVideos,
    FullArtist,
)
from melodine.ytmusic.models.partial_models import PartialArtist
from melodine.ytmusic.models.search_models import SearchArtist
from melodine.ytmusic.models.top_result_models import TopResultArtist
from melodine.ytmusic.utils import model_item


class YTMusicArtist(ArtistBase, URIBase):
    def __init__(
        self, data: Union[TopResultArtist, SearchArtist, PartialArtist, FullArtist]
    ) -> None:
        super().__init__()
        self.__is_data_fetched: bool = False
        self.__data: FullArtist
        self.__base_data = data

        self.__id: str

    @classmethod
    def from_id(cls, resource_id: str) -> "YTMusicArtist":
        raise NotImplementedError()

    @classmethod
    def from_url(cls, url: str) -> "YTMusicArtist":
        raise NotImplementedError()

    def __get_data(self):
        if not self.__is_data_fetched:
            self.__data = model_item(
                service.ytmusic.get_artist(self.id),
                model_type=FullArtist,
            )
            self.__is_data_fetched = True
        return self.__data

    @property
    def id(self) -> str:
        if isinstance(self.__base_data, PartialArtist):
            self.__id = self.__base_data.id
        elif isinstance(self.__base_data, TopResultArtist):
            self.__id = self.__base_data.artists[0].id
        elif isinstance(self.__base_data, SearchArtist):
            self.__id = self.__base_data.browse_id
        elif isinstance(self.__base_data, FullArtist):
            self.__id = self.__base_data.channel_id

        if self.__id is None:
            raise ValueError("Could not resolve artist ID.")
        return self.__id

    @property
    def name(self) -> str:
        if isinstance(self.__base_data, (FullArtist, PartialArtist)):
            return self.__base_data.name
        elif isinstance(self.__base_data, TopResultArtist):
            return self.__base_data.artists[0].name
        elif isinstance(self.__base_data, SearchArtist):
            return self.__base_data.artist

    @property
    def href(self) -> str:
        return "https://music.youtube.com/channel/" + self.id

    @property
    def uri(self) -> str:
        return "ytmusic:artist:" + self.id

    @cached_property
    def radio_id(self) -> Optional[str]:
        if isinstance(self.__base_data, (FullArtist, SearchArtist)):
            return self.__base_data.radio_id
        return self.__get_data().radio_id

    @cached_property
    def shuffle_id(self) -> Optional[str]:
        if isinstance(self.__base_data, (FullArtist)):
            return self.__base_data.shuffle_id
        return self.__get_data().shuffle_id

    @cached_property
    def description(self) -> str:
        if isinstance(self.__base_data, (FullArtist)):
            return self.__base_data.description
        return self.__get_data().description

    @cached_property
    def views(self) -> str:
        if isinstance(self.__base_data, (FullArtist)):
            return self.__base_data.views
        return self.__get_data().views

    @cached_property
    def subscribers(self) -> str:
        if isinstance(self.__base_data, (FullArtist, TopResultArtist)):
            return self.__base_data.subscribers
        return self.__get_data().subscribers

    @cached_property
    def images(self) -> List[Image]:
        if isinstance(self.__base_data, (FullArtist, TopResultArtist, SearchArtist)):
            return self.__base_data.thumbnails
        return self.__get_data().thumbnails

    @cached_property
    def tracks(self) -> ArtistTracks:
        if isinstance(self.__base_data, (FullArtist)):
            return self.__base_data.tracks
        return self.__get_data().tracks

    @cached_property
    def albums(self) -> ArtistAlbums:
        if isinstance(self.__base_data, (FullArtist)):
            return self.__base_data.albums
        return self.__get_data().albums

    @cached_property
    def singles(self) -> ArtistAlbums:
        if isinstance(self.__base_data, (FullArtist)):
            return self.__base_data.singles
        return self.__get_data().singles

    @cached_property
    def videos(self) -> ArtistVideos:
        if isinstance(self.__base_data, (FullArtist)):
            return self.__base_data.videos
        return self.__get_data().videos

    @cached_property
    def related_artists(self) -> ArtistRelated:
        if isinstance(self.__base_data, (FullArtist)):
            return self.__base_data.related
        return self.__get_data().related


if __name__ == "__main__":
    from melodine.ytmusic.views.search import search

    srch = search("sewerslvt")
    artist = srch.top_result[0]

    ytmartist = YTMusicArtist(data=artist)
    print("\n", ytmartist.id)
    print(ytmartist.name)
    print(ytmartist.href)
    print(ytmartist.uri)
    print(ytmartist.radio_id)
    print(ytmartist.shuffle_id)
    print(ytmartist.description)
    print(ytmartist.subscribers)
    print(ytmartist.views)
    print(ytmartist.images)
    print(ytmartist.albums)
    print(ytmartist.singles)
    print(ytmartist.videos)
    print(ytmartist.tracks)
    print(ytmartist.related_artists)

    print(dir(ytmartist))
