from typing import Dict, List, NamedTuple, Union

from ...domains import ytmusic  # pylint: disable=unused-import
from ...utils import YT, YTMUSIC, Image
from .video import Video


class Track(Video):
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

    def __init__(self, *args, **kwargs) -> None:
        # so that a ytmusic.Track object can be constructed either from a json response (data) or a ytmusic track's ID
        # by passing a keyword or a positional argument
        data: Union[str, dict] = str()
        if (args and isinstance(args[0], dict)) or "data" in kwargs:
            data = kwargs["data"] if 'data' in kwargs else args[0]
            if "artists" not in data or data['artists'][0]['id'] is None:
                data = YTMUSIC.get_song(data.get("videoId"))['videoDetails']
        elif (args and isinstance(args[0], str)) or "track_id" in kwargs:
            _id = kwargs["track_id"] if "track_id" in kwargs else args[0]
            data = YTMUSIC.get_song(_id)["videoDetails"]

        super().__init__(data=data)

        try:
            self.artists_: List[Dict] = (
                list(
                    map(
                        lambda artist: YTMUSIC.get_artist(artist.get("id"))
                        if "tracks" not in artist
                        else artist,
                        data.get("artists", []),
                    )
                )
                if "artists" in data
                else [YTMUSIC.get_artist(data.get("channelId", str()))]
            )
        except (KeyError, ValueError, AttributeError):
            Artist_ = NamedTuple(
                "Artist_",
                [
                    ("name", str),
                    ("images", List[Image])
                ]
            )
            self.artists_ = [
                Artist_(data.get('author'),
                        [Image(**image) for image in data.get('thumbnail', {}).get('thumbnails')])
            ]

        try:
            self.album_: Dict = (
                YTMUSIC.get_album(data.get("album", {}).get("id"))
                if "album" in data
                else kwargs.get("album", {})
            )
        except (KeyError, ValueError):
            self.album_ = {}

        self.id: str = data.get(
            "videoId", kwargs.get("track_id", None)
        )  # pylint: disable=invalid-name
        self.name: str = data.get("title", str())
        self.href: str = "https://music.youtube.com/watch?v=" + self.id
        self.uri: str = f"ytmusic:track:{self.id}"

        self.images: List[Image] = [
            Image(**image)
            for image in data.get(
                "thumbnails",
                data.get("thumbnail", {})
                if not "thumbnails" in data.get("thumbnail", {})
                else data.get("thumbnail", {}).get("thumbnails", {}),
            )
        ]

        self.url_: str = str()
        self.recs_: List[Dict] = []

    @property
    def album(self) -> "ytmusic.Album":
        """property getter for the album the given track is from"""
        from .album import Album

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


class PlaylistTrack(Track):
    def __init__(self, data: Dict, **kwargs) -> None:

        super().__init__(data=data)

        self.id = data.get('videoId')  # pylint: disable=invalid-name
        self.href = f'https://music.youtube.com/watch?v={self.id}'
        self.uri = f'ytmusic:playlist_track:{self.id}'

        self.name = data.get('title')

        self.album_ = {}
        self.artist_ = YT.get_channel_info(channel_id=self.id)
        self.artist = NamedTuple(
            "Artist",
            [
                ("name", data.get('author')),
                ("images", [Image(**image)
                 for image in data.get('thumbnail').get('thumbnails')])
            ]
        )
