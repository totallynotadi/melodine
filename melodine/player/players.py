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
    'vn': True,
    'sync': 'audio',
    'genpts': True,
    'infbuf': True
}


def playsound(location: Union[str, BinaryIO], *, blocking: bool = False):
    file_name = None
    if isinstance(location, io.IOBase):
        file_name = os.path.join(TEMPFILES_DIR, id(location))
        with open(file_name) as file:
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
    filters = 'silenceremove=stop_periods=1:stop_threshold=0dB:stop_mode=any:detection=peak'
    # filters = 'silenceremove=start_periods=1:start_duration=1:start_threshold=-50dB:detection=peak,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,areverse'
    # filters = ''
    FF_OPTS.update({'volume': 0.0, 'af': filters})
    player = MediaPlayer(location, ff_opts=FF_OPTS)
    # time.sleep(1)

    time.sleep(2)
    player.set_volume(0.0)
    player.toggle_pause()
    # time.sleep(1)

    if fade_in:
        player_fade_in(player, fade)
    else:   player.set_volume(1.0)
    
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
