import io
import os
import threading
import time
from typing import BinaryIO, Union

from ffpyplayer.player import MediaPlayer
from melodine.configs import TEMPFILES_DIR
from melodine.player.helpers import manage_stream, player_fade_in
from melodine.utils import singleton

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


def play(location: str, *, blocking: bool = False, fade: int = 0, fade_in: bool = False) -> None:
    player = MediaPlayer(location, loglevel='quiet', ff_opts={
                         **FF_OPTS, **{'volume': 0.0}}, thread_lib="SDL")
    time.sleep(1)
    player.set_volume(0.0)
    time.sleep(1)

    manager_thread = threading.Thread(
        target=manage_stream, args=(player, location, fade))
    if blocking:
        manager_thread.run()
    else:
        manager_thread.start()


@singleton
class Player:
    def __new__(self, autoplay: bool = False, crossfade: int = 6):
        self.crossfade = crossfade
        self.autoplay = autoplay
        self.now_playing = None
        self.queue = []

        threading.Thread(target=self.player_handler, args=(self,)).start()

    def player_handler(self):
        while True:
            for track in self.queue:
                self.now_playing = track
                self.queue.remove(track)
            time.sleep(0.4)
