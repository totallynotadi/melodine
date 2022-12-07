import io
import os
import threading
import time
from typing import BinaryIO, List, Union

from ffpyplayer.player import MediaPlayer
from ffpyplayer.tools import loglevels, set_log_callback

import melodine
from melodine.configs import TEMPFILES_DIR
from melodine.models import base
from melodine.player.helpers import manage_stream
from melodine.utils import singleton

loglevel_emit = 'error'


def log_callback(message, level):
    if message and loglevels[level] <= loglevels[loglevel_emit]:
        print("error")


set_log_callback(log_callback)

FF_OPTS = {
    'paused': True,
    'sync': 'audio',
    'vn': True,
    'genpts': True,
    'infbuf': True
}


def playsound(location: Union[str, BinaryIO], *, blocking: bool = False):
    file_name = None
    if isinstance(location, io.IOBase):
        file_mode = 'w' + 'b' if isinstance(location, io.FileIO) else ''
        file_name = os.path.join(TEMPFILES_DIR, id(location))
        with open(file_name, file_mode) as file:
            file.write(location.read())
        location = file_name

    player = MediaPlayer(location, ff_opts=FF_OPTS)
    time.sleep(1)
    player.toggle_pause()
    # time.sleep(2)

    manager_thread = threading.Thread(
        target=manage_stream, args=(player, location))
    if blocking:
        manager_thread.run()
    else:
        manager_thread.start()
    if file_name is None:
        os.remove(file_name)


def play(location: str, *, blocking: bool = False, fade: int = 0, fade_in: bool = False) -> Union[MediaPlayer, None]:
    time.sleep(0.5)
    player = MediaPlayer(location, ff_opts={**FF_OPTS, **{'volume': 0.0}})
    time.sleep(1.5)
    player.set_volume(0.0)
    time.sleep(0.5)

    manager_thread = threading.Thread(
        target=manage_stream, args=(player, location, fade), daemon=True)
    if blocking:
        manager_thread.run()
    elif blocking is None:
        return player, manager_thread
    else:
        manager_thread.start()
        return player


@singleton
class Player:
    def __init__(self, autoplay: bool = False, crossfade: int = 6):
        self.crossfade: int = crossfade
        self.autoplay: bool = autoplay

        self.shuffle: bool = False
        self.repeast: bool = False

        self.recently_played: List = []
        self.now_playing = None
        self.__now_playing = None
        self.queue: List[base.TrackBase] = []

        thread = threading.Thread(
            target=self.player_handler, args=(), daemon=True)
        thread.start()

    def player_handler(self):
        sleep_time = 0
        while True:
            for track in self.queue:
                print(f'new track - {track}')
                self.queue.remove(track)
                self.now_playing = track
                self.__now_playing, self.__now_playing_thread = play(
                    self.now_playing.url,
                    blocking=None,
                    fade=self.crossfade,
                    fade_in=True
                )
                print(self.__now_playing)
                print(self.now_playing)
                self.__now_playing_thread.run()
                self.recently_played.append(track)
                print(self.queue)
            time.sleep(0.4)

    # pause state
    def pause(self):
        self.__now_playing.set_pause(True)

    def get_state(self) -> bool:
        return self.__now_playing.get_pause()

    def set_state(self, state: bool) -> None:
        self.__now_playing.set_pause(state)

    def toggle_state(self) -> None:
        self.__now_playing.toggle_pause()

    # player volume
    def get_volume(self) -> int:
        return self.__now_playing.get_volume()

    def set_volume(self, volume: int) -> None:
        self.__now_playing.set_volume(volume)

    # mute
    def get_mute(self) -> bool:
        return self.__now_playing.get_mute()

    def set_mute(self, mute: bool) -> None:
        self.__now_playing.set_mute(mute)

    def toggle_mute(self) -> None:
        self.__now_playing.set_mute(not self.__now_playing.get_mute())

    # playback progress
    def get_current_timestamp(self) -> int:
        return int(self.__now_playing.get_pts())

    def seek(self, pts: int) -> None:
        self.__now_playing.seek(pts, relative=False, accurate=False)

    def get_shuffle(self) -> bool:
        return self.shuffle

    def set_shuffle(self, shuffle: bool) -> None:
        self.shuffle = shuffle

    def toggle_shuffle(self) -> None:
        self.shuffle = not self.shuffle

    # queing
    def play_next(self, track):
        self.queue.insert(0, track)

    def add_to_queue(self, item: Union[base.TrackBase, base.PlaylistBase, base.AlbumBase]):
        # if isinstance(item, (base.PlaylistBase, base.AlbumBase)):
        #     for track in item.tracks:
        #         self.queue.append(track)
        # else:
        self.queue.append(item)

    def remove_from_queue(self, track: Union[int, base.TrackBase]) -> None:
        if isinstance(track, int):
            del self.queue[track]
        else:
            self.queue.remove(track)

    # playback
    def play(self, track: Union[Union[base.TrackBase, base.ArtistBase, base.PlaylistBase, base.AlbumBase], None] = None) -> None:
        if track is None:
            self.__now_playing.set_pause(False)
        else:
            self.add_to_queue(track)

    def next(self): ...
    def previous(self): ...
    def rewind(self): ...

    # for duration / stream metadata (like audio quality)
    def get_metadata(self):
        return self.__now_playing.get_metadata()
