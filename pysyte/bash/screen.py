import atexit

from pysyte.bash.shell import run

_alt_screen_started = False

def _stop_alt_screen():
    if _alt_screen_started:
        run('tput rmcup')


def _start_alt_screen():
    _alt_screen_started = True
    run('tput smcup')


def get_alt_screens():
    return _start_alt_screen, _stop_alt_screen


def alt_screen():
    atexit.register(_stop_alt_screen)
    return _start_alt_screen
