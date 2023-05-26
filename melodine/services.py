from dataclasses import dataclass, field
import json
import os
from typing import TYPE_CHECKING
from urllib.parse import parse_qs
import requests

import spotipy
from ytmusicapi import YTMusic
from innertube import InnerTube

from melodine.utils import singleton
from melodine.configs import *
from melodine.cipher import Cipher


if TYPE_CHECKING:
    from youtube_dl import YoutubeDL
    import pyyoutube


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
YTM_HEADERS["cookie"] = YTMUSIC_COOKIE


@dataclass
class SpotifyCredentials:
    client_id: str = CLIENT_ID
    client_secret: str = CLIENT_SECRET
    scopes: str = SCOPES
    cache_path: str = CACHE_PATH


@dataclass
class ConfigParams:
    # ytm-cookies, yt-key, spotify-creds
    spotify_creds: SpotifyCredentials = field(default_factory=SpotifyCredentials)
    ytm_headers: dict = field(default_factory=lambda: YTM_HEADERS)
    yt_api_key: str = YT_API_KEY
    ytdl_config: dict = field(default_factory=lambda: YTDL_CONFIG)


@singleton
class Services:
    def __init__(self, config_params: ConfigParams = ConfigParams()):
        self.config = config_params

        self._spotify = None
        self._ytmusic = None
        self._yt = None
        self._ytdl = None
        self._innertube = None

        self._base_js_url = None
        self._base_js_content = None

        self._base_js_path = os.path.join(APP_DIR, "base-js-cache.json")
        self._cipher = None

    @property
    def spotify(self) -> "spotipy.Spotify":
        if self._spotify is None:
            if os.path.exists(CACHE_PATH):
                self._spotify = spotipy.Spotify(
                    auth_manager=spotipy.SpotifyOAuth(
                        scope=self.config.spotify_creds.scopes,
                        client_id=self.config.spotify_creds.client_id,
                        client_secret=self.config.spotify_creds.client_secret,
                        redirect_uri="http://localhost:8080/",
                        cache_handler=spotipy.CacheFileHandler(cache_path=CACHE_PATH),
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

    @property
    def ytmusic(self) -> YTMusic:
        if self._ytmusic is None:
            self._ytmusic = YTMusic(auth=json.dumps(self.config.ytm_headers))
        return self._ytmusic

    @property
    def yt(self) -> "YoutubeDL":
        from youtube_dl import YoutubeDL

        if self._ytdl is None:
            self._ytdl = YoutubeDL(self.config.ytdl_config)
        return self._ytdl

    @property
    def ytdl(self) -> "pyyoutube.Api":
        import pyyoutube

        if self._yt is None:
            self._yt = pyyoutube.Api(self.config.yt_api_key)
        return self._yt

    @property
    def innertube(self) -> InnerTube:
        if self._innertube is None:
            self._innertube = InnerTube("WEB_MUSIC")
        return self._innertube

    def _get_base_js(self):
        self._base_js_url = self.ytmusic.get_basejs_url()
        return {
            "base_js_url": self._base_js_url,
            "base_js_content": requests.get(self._base_js_url).text,
        }

    @property
    def basejs(self) -> str:
        if os.path.exists(self._base_js_path):
            with open(self._base_js_path, "w", encoding="utf-8") as basejs:
                json.dump(self._get_base_js(), basejs)
        with open(self._base_js_path, "r", encoding="utf") as basejs:
            data: dict = json.load(basejs)
            self._base_js_url, self._base_js_content = data.values()
        return self._base_js_content

    @property
    def cipher(self) -> Cipher:
        if self._cipher is None:
            self._cipher = Cipher(js=self.basejs)
        return self._cipher

    def sign_url(self, sig_cipher: str) -> str:
        sig_cipher = parse_qs(sig_cipher)
        signature = self.cipher.get_signature(ciphered_signature=sig_cipher["s"][0])
        signed_url = sig_cipher["url"][0] + "&sig=" + signature + "&ratebypass=yes"
        return signed_url

    def spotify_auth(self, client_id, client_secret):
        return

    def ytmusic_oauth(self):
        return


service = Services()

if os.path.exists(TEMPFILES_DIR):
    os.rmdir(TEMPFILES_DIR)
