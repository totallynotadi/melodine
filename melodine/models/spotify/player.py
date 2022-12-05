from dataclasses import dataclass
from typing import Dict, List

from melodine.models import spotify  # pylint: disable=unused-import

from melodine.models.spotify.device import Device
from melodine.models.spotify.track import Track


@dataclass
class PlayerContext:
    '''the "Playing From" context for particular playback state'''

    def __init__(self, data: Dict) -> None:
        self.external_urls: List[Dict[str, str]] = data.get('external_urls')
        self.type: str = data.get('type')
        self.uri: str = data.get('uri')
        self.href: str = f'open.spotify.com/{type}/{self.uri.split(":")[2]}'


class Player:
    def __init__(self, data: Dict, user: "spotify.User") -> None:
        self.user = user

        self.device: Device = Device(data.get('device'))
        self.shuffle_state: bool = data.get('shuffle_state')
        self.repeat_state: bool = data.get('repeat_state')
        self.context: PlayerContext = data.get('context')
        self.progress = data.get('progress_ms') * 1000
        self.item: Track = Track(data.get('item'))
        self.currently_playing_type = data.get('currently_playing_type')
        self.is_playing: bool = data.get('is_playing')

    def __repr__(self):
        return f"<spotify.Player: {self.user!r}>"

    # TODO - check if basic player modifications works for non-premium users and implement those methods
