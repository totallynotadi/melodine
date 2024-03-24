import json
import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, Optional
from urllib.parse import parse_qs

import requests
import spotipy
from innertube import InnerTube
from ytmusicapi import YTMusic

from melodine import configs as CONFIG
from melodine.cipher import Cipher
from melodine.utils import singleton

if TYPE_CHECKING:
    import pyyoutube
    from youtube_dl import YoutubeDL


SCOPES = """
            user-read-playback-state
            user-follow-read
            user-follow-modify
            playlist-read-private
            playlist-read-collaborative
            playlist-modify-private
            playlist-modify-public
            user-read-recently-played
            user-library-read
            user-library-modify
            user-top-read
            user-read-private
        """  # pylint: disable=invalid-name

YTM_HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "SAPISIDHASH 1643090086_74cc0985095757af3f1af65902686e81b6637950",
    "content-encoding": "gzip",
    "content-type": "application/json",
    "cookie": "",
    "dnt": "1",
    "origin": "https://music.youtube.com",
    "referer": "https://music.youtube.com/",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"97.0.4692.71"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"14.0.0"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "same-origin",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "x-client-data": "CIq2yQEIo7bJAQjBtskBCKmdygEI7enKAQjq8ssBCJ75ywEI1/zLAQjmhMwBCIOVzAEI9pXMAQ==",
    "x-goog-authuser": "0",
    "x-goog-visitor-id": "Cgt1eVA1clJ4TlFoayikob6PBg%3D%3D",
    "x-origin": "https://music.youtube.com",
    "x-youtube-client-name": "67",
    "x-youtube-client-version": "1.20220119.00.00",
}


@dataclass
class SpotifyCredentials:
    client_id: str = CONFIG.CLIENT_ID
    client_secret: str = CONFIG.CLIENT_SECRET
    scopes: str = SCOPES
    app_path: str = CONFIG.APP_DIR


@dataclass
class ConfigParams:
    # ytm-cookies, yt-key, spotify-creds
    spotify_creds: SpotifyCredentials = field(default_factory=SpotifyCredentials)
    ytm_headers: dict = field(default_factory=lambda: YTM_HEADERS)
    ytm_cookie: str = field(default_factory=lambda: CONFIG.YTMUSIC_COOKIE)
    yt_api_key: str = CONFIG.YT_API_KEY
    ytdl_config: dict = field(default_factory=lambda: CONFIG.YTDL_CONFIG)


@singleton
class Services:
    def __init__(self, config_params: ConfigParams = ConfigParams()):
        self.config = config_params

        self._spotify: Optional[spotipy.Spotify] = None
        self.__ytmusic: Optional[YTMusic] = None
        self.__yt: Optional[pyyoutube.Api] = None
        self.__ytdl: Optional[YoutubeDL] = None
        self.__innertube: Optional[InnerTube] = None

        self._base_js_url: Optional[str] = None
        self._base_js_content: Optional[str] = None

        self._base_js_path = os.path.join(CONFIG.APP_DIR, "base-js-cache.json")
        self._cipher: Optional[Cipher] = None

    @property
    def spotify(self) -> "spotipy.Spotify":
        if self._spotify is None:
            if os.path.exists(self.config.spotify_creds.app_path):
                self._spotify = spotipy.Spotify(
                    auth_manager=spotipy.SpotifyOAuth(
                        scope=self.config.spotify_creds.scopes,
                        client_id=self.config.spotify_creds.client_id,
                        client_secret=self.config.spotify_creds.client_secret,
                        redirect_uri="http://localhost:8080/",
                        cache_handler=spotipy.CacheFileHandler(
                            cache_path=os.path.join(
                                self.config.spotify_creds.app_path, "spotify-cache"
                            )
                        ),
                    )
                )
            else:
                self._spotify = spotipy.Spotify(
                    auth_manager=spotipy.SpotifyClientCredentials(
                        client_id=self.config.spotify_creds.client_id,
                        client_secret=self.config.spotify_creds.client_secret,
                    )
                )
        return self._spotify

    def _ytmusic(self, cookie: Optional[str] = None) -> YTMusic:
        """exists only to get a YTM object explicitly from the cookie given as the param"""
        return (
            YTMusic(auth=json.dumps(self.config.ytm_headers.update({"cookie": cookie})))
            if cookie
            else self.ytmusic
        )

    @property
    def ytmusic(self) -> YTMusic:
        if self.__ytmusic is None:
            self.config.ytm_headers.update({"cookie": CONFIG.YTMUSIC_COOKIE})
            self.__ytmusic = YTMusic(auth=json.dumps(self.config.ytm_headers))
        return self.__ytmusic

    @property
    def ytdl(self) -> "YoutubeDL":
        from youtube_dl import YoutubeDL

        if self.__ytdl is None:
            self.__ytdl = YoutubeDL(self.config.ytdl_config)
        return self.__ytdl

    @property
    def yt(self) -> "pyyoutube.Api":
        import pyyoutube

        if self.__yt is None:
            self.__yt = pyyoutube.Api(self.config.yt_api_key)
        return self.__yt

    @property
    def innertube(self) -> InnerTube:
        if self.__innertube is None:
            self.__innertube = InnerTube("WEB_MUSIC")
        return self.__innertube

    def _get_base_js(self):
        self._base_js_url = self.ytmusic.get_basejs_url()
        return {
            "base_js_url": self._base_js_url,
            "base_js_content": requests.get(self._base_js_url, timeout=30).text,
        }

    @property
    def basejs(self) -> str:
        if not os.path.exists(self._base_js_path):
            with open(self._base_js_path, "w", encoding="utf-8") as basejs:
                json.dump(self._get_base_js(), basejs)
        with open(self._base_js_path, "r", encoding="utf") as basejs:
            data: Dict[str, str] = json.load(basejs)
            (
                self._base_js_url,
                self._base_js_content,
            ) = data.values()
        return self._base_js_content

    @property
    def cipher(self) -> Cipher:
        if self._cipher is None:
            self._cipher = Cipher(js=self.basejs)
        return self._cipher

    def sign_url(self, sig_cipher: str) -> str:
        parsed_query = parse_qs(sig_cipher)
        signature = self.cipher.get_signature(ciphered_signature=parsed_query["s"][0])
        signed_url = parsed_query["url"][0] + "&sig=" + signature + "&ratebypass=yes"
        return signed_url

    def spotify_auth(self, client_id, client_secret):
        return

    def ytmusic_oauth(self):
        return


service = Services()

if os.path.exists(CONFIG.TEMPFILES_DIR):
    os.rmdir(CONFIG.TEMPFILES_DIR)
