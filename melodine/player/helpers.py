import threading
import time

from ffpyplayer.player import MediaPlayer


FADE_IN_STEPS = [x / 10000000.0 for x in range(00000, 10078125, 78125)]
FADE_OUT_STEPS = [x / 10000000.0 for x in range(00000, 10078125, 78125)]
FADE_OUT_STEPS.reverse()
SMOOTHNESS_FACTOR = 32
FF_OPTS = {
    'paused': True,
    'vn': True,
    'sync': 'audio',
    'genpts': True,
    'infbuf': True
}


def close_player(player):
    print(f':: CLOSING PLAYER at {player.get_pts()}')
    player.toggle_pause()
    time.sleep(1)
    player.close_player()


def close_stream(player: MediaPlayer, fade: bool = True) -> None:
    # print(f'::: current_pts: {current_pts}, {DURATION - current_pts} seconds left')

    DURATION = player.get_metadata()['duration']

    print('::: entered closing')
    if fade:
        player_fade_out(player)
    print(':: BROKE')


def player_fade_in(player: MediaPlayer, fade: int = 0):
    for step in FADE_IN_STEPS:
        delta = fade - player.get_pts()
        player.set_volume(step)
        print(player.get_volume(), player.get_pts(), delta, step)
        time.sleep(delta / SMOOTHNESS_FACTOR)


def player_fade_out(player: MediaPlayer):
    DURATION = player.get_metadata()['duration']

    print('::: entered closing')
    for step in FADE_OUT_STEPS[FADE_OUT_STEPS.index(player.get_volume()):]:
        delta = DURATION - player.get_pts()
        player.set_volume(step)
        print(player.get_volume(), player.get_pts(), delta, step)
        time.sleep(delta / SMOOTHNESS_FACTOR)
    else:
        close_player(player)


def manage_stream(player: MediaPlayer, source: str, fade: int = 0, fade_in: bool = True) -> None:
    last_pts = 10
    updated_pts = 0

    threading.Thread(
        target=player_fade_in,
        args=(player, fade)
    ).start() if fade_in else player.set_volume(1.0)
    if player.get_pause():
        player.toggle_pause()

    DURATION = player.get_metadata()['duration']

    last_buffered_pts = 0
    buffer_repeat_count = 0
    print(f":: METADATA: {player.get_metadata()}")
    while True:

        print(updated_pts)
        updated_pts = int(str(player.get_pts()).split('.', maxsplit=1)[0])

        while player.get_pause():
            time.sleep(0.4)

        if (updated_pts == last_pts != 0 and
                not updated_pts == last_pts == DURATION):
            player.toggle_pause()
            print(f"buffered out, pausing: {buffer_repeat_count}")
            # player.seek(-1, relative=True, accurate=False)
            player.toggle_pause()
            time.sleep(2)
            updated_pts = int(str(player.get_pts()).split('.', maxsplit=1)[0])
            last_buffered_pts = last_pts
            if last_buffered_pts == updated_pts:
                buffer_repeat_count += 1

        if updated_pts != last_buffered_pts:
            last_buffered_pts = 0
            buffer_repeat_count = 0

        if buffer_repeat_count == 2:
            print('reviving stream')
            player.toggle_pause()
            player.close_player()
            time.sleep(1)
            del player
            print('::: closed stream')
            time.sleep(1)
            player = MediaPlayer(source, ff_opts=FF_OPTS)
            time.sleep(2)
            print('::: created new player')
            # player.seek(updated_pts + 1, accurate=False)
            player.seek(updated_pts, accurate=False)
            time.sleep(1)
            player.toggle_pause()
            buffer_repeat_count = 0

        # fade aka refenrece point to begin closing
        current_pts = int(str(player.get_pts()).split('.', maxsplit=1)[0])
        if current_pts + abs(fade) >= DURATION:
            if fade <= 3:
                if fade > 0:
                    time.sleep(fade)
                buffer_repeat_count = 0
                close_player(player)
                break
            print(
                f"breaking from the handler thread, at timestamp: {current_pts}")
            threading.Thread(
                target=close_stream,
                args=(player, bool(fade))
            ).start()
            break
        last_pts = updated_pts
        time.sleep(1)
    print('\r::: broke..\n>>> ', end='')
