# region Imports
import curses

import math
import os
import threading
import time
from curses import panel, wrapper
from curses.textpad import Textbox, rectangle
from ffpyplayer.player import MediaPlayer
from ffpyplayer.tools import loglevels, set_log_callback
from melodine import innertube, spotify, utils, ytmusic
from melodine.configs import APP_DIR
from melodine.player import Player

# endregion

# region to make ffpyplayer not output anything
loglevel_emit = "error"


def log_callback(message, level):
    if message and loglevels[level] <= loglevels[loglevel_emit]:
        print("error")


set_log_callback(log_callback)
# endregion

# region God Help Me


global ffs


class Menu:
    search_type = "tracks"
    with open(os.path.join(APP_DIR, "ffs.txt"), "w") as ffs:
        ffs.write(search_type)

    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(5, 12, 0, width - 13)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = "%d. %s" % (index, item[0])
                self.window.addstr(1 + index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord("\n")]:
                search_type = self.items[self.position][0].lower()

                with open(os.path.join(APP_DIR, "ffs.txt"), "w") as ffs:
                    ffs.write(search_type)
                break

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()


# endregion


def runner(stdscr):

    curses.noecho()
    stdscr.keypad(True)
    global height
    global width
    global player
    global index
    global autoplay
    autoplay = True
    index = -1
    height, width = stdscr.getmaxyx()

    # print(height)

    # Quits if terminal is too small
    if height < 14 or width < 60:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

        # print("Terminal too small!")

        quit()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    # Initialises search box and player window
    box = draw_search_box(stdscr)
    playerwin = draw_player(stdscr)
    menu = draw_type_menu(stdscr)
    autotoggle = stdscr.subwin(3, 9, 1,width - 23)
    autotoggle.border()
    autotoggle.addstr("autoplay")
    autotoggle.addstr(1, 1, "ON ")
    autotoggle.refresh()
    typewin = stdscr.subwin(3, 9, 1, width - 13)
    typewin.border()
    typewin.addstr(1, 1, menu.search_type)
    typewin.refresh()
    playerwin.refresh()
    curses.curs_set(0)
    while True:
        c = stdscr.getch()
        # If window resized redraw elements
        # FIXME: Does not redraw correctly
        if c == curses.KEY_RESIZE:
            stdscr.clear()
            stdscr = curses.initscr()
            height, width = stdscr.getmaxyx()
            if height < 14 or width < 60:
                curses.nocbreak()
                stdscr.keypad(False)
                curses.echo()
                curses.endwin()

                print("Terminal too small!")

                quit()
            box = draw_search_box(stdscr)
            menu = draw_type_menu(stdscr)
            autotoggle = stdscr.subwin(3, 9, 1,width - 23)
            autotoggle.border()
            autotoggle.addstr("autoplay")
            autotoggle.addstr(1, 1, "ON ")
            autotoggle.refresh()
            typewin = stdscr.subwin(3, 9, 1, width - 13)
            typewin.border()
            typewin.addstr(1, 1, menu.search_type)
            typewin.refresh()
            playerwin = draw_player(stdscr)
            playerwin.refresh()
            stdscr.refresh()

        elif c == ord("/"):
            results = search(box, stdscr, menu)
        elif c == ord("x"):
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            break

        elif c == curses.KEY_UP:
            if os.path.exists(os.path.join(APP_DIR, "History.txt")):
                with open(os.path.join(APP_DIR, "History.txt"), "r") as history:
                    search_term = history.readlines()[index]
                    newline = search_term.index("\n")
                    search_term = search_term[:newline]
                    if len(search_term) > 30:
                        search_term = search_term[:30]
                    results = search(box, stdscr, menu, search_term)
                    stdscr.addstr(2, 1, search_term)
                    if abs(index) < len(history.readlines()) - 1:
                        index -= 1

        elif c == curses.KEY_DOWN:
            if os.path.exists(os.path.join(APP_DIR, "History.txt")):
                with open(os.path.join(APP_DIR, "History.txt"), "r") as history:
                    search_term = history.readlines()[index]
                    results = search(box, stdscr, menu, search_term)
                    stdscr.addstr(2, 1, search_term[:30])
                    if index < len(history.readlines()) - 1:
                        index += 1

        elif c >= ord("0") and c <= ord("9"):
            selected = results[int(chr(c))]
            # utils.put_notification(selected)
            player_update(
                playerwin, "Playing", selected.artists[0].name, selected.name, selected.duration
            )
            # url = innertube.InnerTube().player(selected.id)['streamingData']['formats'][-1]['url']
            history = open(os.path.join(APP_DIR, "History.txt"), "a")
            history.write(selected.name + "\n")
            history.close()
            player = Player()
            player.play(selected)
            global bar
            bar = threading.Thread(
                target=progressbar, args=(playerwin, selected.duration)
            ).start()

        elif c == ord("a"):
            if autoplay == True:
                autoplay = False
                autotoggle.addstr(1, 1, "ON ")
            else:
                autoplay = True
                autotoggle.addstr(1, 1, "OFF")
            autotoggle.refresh()

        elif c == ord("l"):
            liked_path = os.path.join(APP_DIR, "Liked.txt")
            if not os.path.exists(os.path.join(APP_DIR, "Liked.txt")):
                with open(os.path.join(APP_DIR, "Liked.txt"), "a") as liked:
                    liked.write(selected.name + "\n")
            else:
                with open(os.path.join(APP_DIR, "Liked.txt")) as liked:
                    if selected.name not in liked.readlines():
                        liked.write(selected.name + "\n")
        
        elif c == ord("p"):
            if player:
                player.toggle_state()
                player_update(playerwin, "Paused", selected.artists[0].name, selected.name, selected.duration)
        elif c == ord("t"):
            menu.display()
            typewin = stdscr.subwin(3, 9, 1, width - 13)
            typewin.border()
            ffs = ""
            with open(os.path.join(APP_DIR, "ffs.txt"), "r") as help:
                ffs = help.read()
            typewin.addstr(1, 1, ffs)
            typewin.refresh()
        # TODO: Display queue
        elif c == ord("q"):
            continue



# region Curses Functions
# Initialises player window with "Nothing Playing"


def draw_player(stdscr):
    playerwin = curses.newwin(5, width - 1, height - 5, 0)
    playerwin.border()
    playerwin.addstr(0, 1, "Nothing Playing", curses.color_pair(1) | curses.A_BOLD)
    playerwin.refresh()
    return playerwin

def draw_queue(tracks):
    result_num = height - 11
    if result_num > 10:
        result_num = 10
    result_box = curses.newwin(result_num + 2, width - 1, 4, 0)
    result_box.border()

    result_box.addstr(
        0, 1, "Queue", curses.color_pair(1) | curses.A_BOLD
    )
    line = 1
    for track in tracks[:result_num]:
        name = str(result.name)
        artists_list = []
        for artist in result.artists:
            artists_list.append(str(artist.name))
        artists = " & ".join(artists_list)
        if len(artists) > width / 3:
            artists = result.artists[0].name
        if len(name) > width / 3:
            name = name[: (int(width / 3))]

        duration_minute, duration_seconds = math.floor(
            result.duration / 60
        ), "{:02d}".format(math.floor(result.duration % 60))
        result_box.addstr(
            line,
            1,
            f"{line - 1}. |{name}{(int(width/3) - len(name)) * ' '}|{artists}{(int(width/3) - len(artists)) * ' '}|{duration_minute}:{duration_seconds}",
        )


# Method to draw search box
def draw_search_box(stdscr):
    stdscr.addstr(0, 0, "Search (/ to focus):", curses.color_pair(1) | curses.A_BOLD)
    stdscr.keypad(True)
    editwin = curses.newwin(1, 30, 2, 1)
    rectangle(stdscr, 1, 0, 1 + 1 + 1, 1 + 30 + 1)

    stdscr.refresh()
    box = Textbox(editwin)
    return box

# Method to draw panel for search type
def draw_type_menu(stdscr):
    menu_items = [
        ("Tracks", curses.flash),
        ("Artists", curses.flash),
        ("Albums", curses.flash),
    ]

    menu = Menu(menu_items, stdscr)
    return menu



# Updates player window with track data and progressbar


def player_update(player, playing, artist=None, title=None, duration=None):
    minutes = math.floor(duration / 60)
    seconds = math.floor(duration % 60)
    playerwin = curses.newwin(5, width - 1, height - 5, 0)
    length = width - 16
    playerwin.border()
    playerwin.addstr(0, 1, playing, curses.color_pair(1) | curses.A_BOLD)
    if artist and title:
        playerwin.addstr(1, 2, title, curses.color_pair(2) | curses.A_BOLD)
        playerwin.addstr(2, 2, artist, curses.color_pair(1))
        playerwin.addstr(3, 2, "0:00")
        playerwin.addstr(3, width - 7, f"{minutes}:{'{:02d}'.format(seconds)}")
        playerwin.addstr(3, 8, "-" * length)
    playerwin.refresh()


# Updates progressbar


def progressbar(playerwin, duration):
    while True:
        pts = player.get_current_timestamp()
        if pts == duration:
            break
        length = width - 16
        percent = duration / length
        position = math.floor(pts / percent)
        # playerwin.addstr(1, 30, f"dur: {duration}%: {round(percent,2)}, len: {round(length,2)}, pts%%: {round(pts % percent, 2)}, pos: {position}, pts: {'{:03d}'.format(pts)}")
        playerwin.addstr(3, 8, "=" * position)
        minutes = math.floor(pts / 60)
        seconds = math.floor(pts % 60)
        playerwin.addstr(3, 2, f"{minutes}:{'{:02d}'.format(seconds)}")
        playerwin.refresh()
        pts += 1
        time.sleep(1)


def search(
    box,
    stdscr,
    menu,
    search=None,
):
    curses.curs_set(1)
    if not search:
        box.edit()
        # Get resulting contents
        search = box.gather()
        # Print the window to the screen

    with open(os.path.join(APP_DIR, "ffs.txt"), "r") as help:
        ffs = help.read()
    search_type = ffs
    results = spotify.search(search, types=[search_type])

    color = curses.has_colors()
    # Print results based on screensize, maxed at 10
    result_num = height - 11
    if result_num > 10:
        result_num = 10
    result_box = curses.newwin(result_num + 2, width - 1, 4, 0)
    result_box.border()

    result_box.addstr(
        0, 1, "Enter index number to play", curses.color_pair(1) | curses.A_BOLD
    )
    line = 1

    if search_type == "tracks":
        results = results.tracks
    elif search_type == "artists":
        results = results.artists
    elif search_type == "albums":
        results = results.albums
    for result in results[:result_num]:
        if search_type == "tracks":
            name = str(result.name)
            artists_list = []
            for artist in result.artists:
                artists_list.append(str(artist.name))
            artists = " & ".join(artists_list)
            if len(artists) > width / 3:
                artists = result.artists[0].name
            if len(name) > width / 3:
                name = name[: (int(width / 3))]

            duration_minute, duration_seconds = math.floor(
                result.duration / 60
            ), "{:02d}".format(math.floor(result.duration % 60))
            result_box.addstr(
                line,
                1,
                f"{line - 1}. |{name}{(int(width/3) - len(name)) * ' '}|{artists}{(int(width/3) - len(artists)) * ' '}|{duration_minute}:{duration_seconds}",
            )

            line += 1
            curses.curs_set(0)
            result_box.refresh()
        elif search_type == "artists":
            name = str(result.name)
            if len(name) > width / 3:
                name = name[: (int(width / 3))]
            result_box.addstr(line, 1, f"{line - 1}. |{name}")
            line += 1
            curses.curs_set(0)
            result_box.refresh()
        elif search_type == "albums":
            name = str(result.name)
            artists_list = []
            for artist in result.artists:
                artists_list.append(str(artist.name))
            artists = " & ".join(artists_list)
            if len(artists) > width / 3:
                artists = result.artists[0].name
            if len(name) > width / 3:
                name = name[: (int(width / 3))]

            duration_minute, duration_seconds = math.floor(
                result.duration / 60
            ), "{:02d}".format(math.floor(result.duration % 60))
            result_box.addstr(
                line,
                1,
                f"{line - 1}. |{name}{(int(width/3) - len(name)) * ' '}|{artists}{(int(width/3) - len(artists)) * ' '}|{duration_minute}:{duration_seconds}",
            )

            line += 1
            curses.curs_set(0)
            result_box.refresh()
    return results


# endregion

if __name__ == "__main__":
    wrapper(runner)
