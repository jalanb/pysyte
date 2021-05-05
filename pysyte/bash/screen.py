import os
import atexit

from pysyte.bash.shell import run

_alt_screen_started = False

_TERM = "xterm"


def _stop_alt_screen():
    if _alt_screen_started:
        run(f"TERM={_TERM} tput rmcup")


def _start_alt_screen():
    global _alt_screen_started
    _alt_screen_started = True
    run("tput smcup")


def get_alt_screens():
    return _start_alt_screen, _stop_alt_screen


def alt_screen():
    global _TERM
    _TERM = os.environ.get("TERM", "xterm")
    atexit.register(_stop_alt_screen)
    return _start_alt_screen
