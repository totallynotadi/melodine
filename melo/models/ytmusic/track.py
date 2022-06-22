from typing import Dict, List, Union

from ...models import ytmusic  # pylint: disable=unused-import
from ...utils import YTMUSIC, Image, URIBase
from .video import Video


class Track(Video, URIBase):
    """A YTMusic Track object

    Attributes
    ----------
    id : str
        The YouTube video ID for the track
    name : str
        The name of the track
    href : str
        The music.youtbe URL which is the link to the ytmusic page
        for the track
    uri : str
        The YTMusic uri for the track
    artists : List[Artist]
        A list of Artist objects representing the artists for a track
    album: List[Album]
        A list of Album objects representing the album the track is from
    url: str
        The audio playback url for the track
    images List[Image]
        A list of images for the cover art of the track
    """

    __slots__ = ["album_"]

    def __init__(self, data: Union[Dict, str], **kwargs) -> None:
        if isinstance(data, str):
            data = YTMUSIC.get_song(data)['videoDetails']

        print(data)
        super().__init__(data=data)

        self.artists_: List[Union[Dict, str]] = (
            list(
                map(
                    lambda artist: artist.get("id")
                    if "tracks" not in artist
                    else artist,
                    data.get("artists", []),
                )
            ) if "artists" in data 
            else [data.get("channelId", data.get('browseId', str()))]
        )

        self.album_: Union[Dict, str] = (
            data.get("album", {}).get("id") if "album" in data
            else kwargs.get("album", {})
        )

        self.id: str = data.get("videoId", kwargs.get("track_id", str()))  # pylint: disable=invalid-name
        self.name: str = data.get("title", str())
        self.href: str = "https://music.youtube.com/watch?v=" + self.id
        self.uri: str = f"ytmusic:track:{self.id}"

        self.images: List[Image] = [
            Image(**image)
            for image in data.get(
                "thumbnails",
                data.get("thumbnail", {})
                if "thumbnails" not in data.get("thumbnail", {})
                else data.get("thumbnail", {}).get("thumbnails", {}),
            )
        ]

        self.url_: str = str()
        self.recs_: List[Dict] = []

    def __repr__(self) -> str:
        return f"melo.Track - {(self.name or self.id or self.uri)!r}"

    def __str__(self) -> str:
        return str(self.id)

    @property
    def artists(self) -> List["ytmusic.Artist"]:
        """Get a list of all Artists from the track"""
        from .artist import Artist

        for idx, artist in enumerate(self.artists_.copy()):
            if artist:
                artist = Artist(artist)
                self.artists_.insert(idx, artist)
                del self.artists_[idx + 1]
        return self.artists_

    @property
    def album(self) -> "ytmusic.Album":
        """property getter for the album the given track is from"""
        from .album import Album

        if isinstance(self.album_, str):
            try:
                self.album_ = YTMUSIC.get_album(self.album_)
            except (KeyError, ValueError, AttributeError):
                self.album_ = {}

        if not self.album_ or isinstance(self.album_, Album):
            return self.album_

        if self.album_:
            self.album_ = Album(data=self.album_)
        return self.album_

    def get_recommendations(self, limit: int = 1) -> List["Track"]:
        """Get recommendations for this particular tracksd"""
        if not self.recs_:
            self.recs_ = YTMUSIC.get_watch_playlist(self.id, f"RDAMVM{self.id}")[
                "tracks"
            ]

        recs: List[Dict] = self.recs_[:limit]
        return [Track(track) for track in recs]

    def test_run():  # pylint: disable=no-method-argument
        return Track(YTMUSIC.search(query="sewerslvt-pretty cvnt", filter="songs")[0])
