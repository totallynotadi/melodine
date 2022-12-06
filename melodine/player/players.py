import io
import os
import threading
import time
from typing import BinaryIO, List, Union

from ffpyplayer.player import MediaPlayer

from melodine.configs import TEMPFILES_DIR
from melodine.player.helpers import manage_stream, player_fade_in
from melodine.utils import singleton
import melodine

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
    player = MediaPlayer(location, loglevel='quiet', ff_opts={
                         **FF_OPTS, **{'volume': 0.0}}, thread_lib="SDL")
    time.sleep(1)
    player.set_volume(0.0)
    time.sleep(1)

    manager_thread = threading.Thread(
        target=manage_stream, args=(player, location, fade))
    if blocking:
        manager_thread.run()
    elif blocking is None:
        return player
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
        self.queue: List = []

        threading.Thread(target=self.player_handler, args=()).start()

    def player_handler(self):
        sleep_time = 0
        while True:
            for track in self.queue:
                self.queue.remove(track)
                self.now_playing = track
                self.__now_playing = play(
                    self.now_playing.url,
                    blocking=True,
                    fade=self.crossfade
                )
                self.recently_played.append(track)

            time.sleep(0.4)

    # pause state
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
        self.__now_playing.set_pause(mute)

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

    def add_to_queue(self, track):
        self.queue.append(track)

    def remove_from_queue(self, track: Union[int, "melodine.track.Track"]) -> None:
        if isinstance(track, int):
            del self.queue[track]
        else:
            self.queue.remove(track)

    def play(self, track) -> None:
        self.add_to_queue(track)
