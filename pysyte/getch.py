"""Provide a getch() method to get single chars from a terminal


Do not wait on carriage returns

Adapted from
    http://code.activestate.com/recipes/134892/
    Without the redundant classes of that code
        but keeping the implementatation

    And reducing down to just the tty version
        No need here for Windows/Carbon
"""

import re
import signal
import sys
import tty
from curses import ascii

import termios


class NoKeys(StopIteration):
    """Better name for StopIteration caused by running out of keys"""
    pass


def get_ord():
    """The integer ordinal of the next byte read from sys.stdin"""
    return ord(sys.stdin.read(1))


class TerminalContext(object):
    """Context wrapper to set up termios values"""
    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.fd = None
        self.old_settings = None

    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        mode = termios.tcgetattr(self.fd)
        mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, mode)
        return self

    def __exit__(self, typ, value, traceback):
        if typ is not None:
            pass  # exception
        if self.old_settings:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)


class Timeout(Exception):
    """A timeout has occurred"""
    pass


def timeout_raiser(_signum, _frame):
    """Raise a timeout exception"""
    raise Timeout()


class TimerContext(object):
    """Context wrapper for a timeout"""
    # pylint: disable=too-few-public-methods
    def __init__(self, seconds):
        self.seconds = seconds
        self.old_handler = None
        self.timed_out = False

    def __enter__(self):
        self.old_handler = signal.signal(signal.SIGALRM, timeout_raiser)
        signal.setitimer(signal.ITIMER_REAL, self.seconds)
        return self

    def __exit__(self, typ_, value, traceback):
        signal.setitimer(signal.ITIMER_REAL, 0)
        if self.old_handler:
            signal.signal(signal.SIGALRM, self.old_handler)
        if isinstance(value, Timeout):
            self.timed_out = True
            return True


_key_cache = []


def cache_keys(keys):
    """Allow debugging via PyCharm"""
    d = known_keys()
    known_names = dict(zip(d.values(), d.keys()))
    for k in keys:
        i = (ord(k),) if len(k) == 1 else known_names[k]
        _key_cache.insert(0, i)


def _get_keycodes():
    """Read keypress giving a tuple of key codes

    A 'key code' is the ordinal value of characters read

    For example, pressing 'A' will give (65,)
    """
    try:
        return _key_cache.pop()
    except IndexError:
        pass
    result = []
    terminators = 'ABCDFHPQRS~'
    with TerminalContext():
        code = get_ord()
        result.append(code)
        if code == 27:
            with TimerContext(0.1) as timer:
                code = get_ord()
            if not timer.timed_out:
                result.append(code)
                result.append(get_ord())
                if 64 < result[-1] < 69:
                    pass
                elif result[1] == 91:
                    while True:
                        code = get_ord()
                        result.append(code)
                        if chr(code) in terminators:
                            break
    return tuple(result)


class ExtendedKey(Exception):
    """Raised for an unrecognised Extended key code"""
    def __init__(self, codes):
        super(ExtendedKey, self).__init__(
            'Too many key codes: %s' % repr(codes))
        self.codes = codes


def getch():
    """Get a char or and ExtendedKey from a keyboard"""
    codes = _get_keycodes()
    if len(codes) == 1:
        return chr(codes[0])
    raise ExtendedKey(codes)


def get_codes():
    """Get a tuple of stringified keycodes from the keyboard"""
    return tuple(str(_) for _ in _get_keycodes())


def get_key():
    """Get a key from the keyboard as a string

    A 'key' will be a single char, or the name of an extended key
    """
    character_name = chr
    codes = _get_keycodes()
    if len(codes) == 1:
        code = codes[0]
        if code >= 32:
            return character_name(code)
        return control_key_name(code)
    return get_extended_key_name(codes)


def get_menu(**kwargs):
    key = get_key()
    for name, string in kwargs.items():
        match = re.match('^%s$' % string, key)
        if match:
            return name
        if key in name or key in string:
            return name
    return key


def get_ascii():
    """Get ASCII key from stdin

    return None for others
    """
    try:
        return getch()
    except ExtendedKey:
        return None


def get_ASCII():
    """Get ASCII key from stdin

    raise error on other
    """
    try:
        return getch()
    except ExtendedKey:
        raise KeyboardInterrupt


def get_as_key():
    """Get key from stdin

    return ASCII keys as (single char) strings
    others as tuples
    """
    try:
        return getch()
    except ExtendedKey as e:
        return e.codes


def control_key_name(code):
    """Prefix the name of a control key with '^'"""
    return '^%s' % (chr(code - 1 + ord('A')))


def get_extended_key_name(codes):
    """Get a name for the extended key with those codes

    Names are defined herein
    """
    return known_keys()[codes]


def known_keys():
    return {
        (27, 79, 70): 'end',
        (27, 79, 72): 'home',
        (27, 79, 80): 'F1',
        (27, 79, 81): 'F2',
        (27, 79, 82): 'F3',
        (27, 79, 83): 'F4',
        (27, 91, 49, 53, 126): 'F5',
        (27, 91, 49, 55, 126): 'F6',
        (27, 91, 49, 56, 126): 'F7',
        (27, 91, 49, 57, 126): 'F8',
        (27, 91, 50): 'insert',
        (27, 91, 50, 48, 126): 'F9',
        (27, 91, 50, 49, 126): 'F10',
        (27, 91, 50, 51, 126): 'F11',
        (27, 91, 50, 52, 126): 'F12',
        (27, 91, 49, 59, 50, 80): 'F13',
        (27, 91, 49, 59, 50, 83): 'F16',
        (27, 91, 49, 53, 59, 50, 126): 'F17',
        (27, 91, 49, 55, 59, 50, 126): 'F18',
        (27, 91, 49, 56, 59, 50, 126): 'F19',
        (27, 91, 51, 126): 'Del',
        (27, 91, 51): 'delete',
        (27, 91, 53): 'page up',
        (27, 91, 53, 126): 'page up',
        (27, 91, 54): 'page down',
        (27, 91, 54, 126): 'page down',
        (27, 91, 65): 'up',
        (27, 91, 66): 'down',
        (27, 91, 67): 'right',
        (27, 91, 68): 'left',
    }


def _yielder(getter):
    """Keep yielding from that getter until KeyboardInteruptted"""
    def yield_till_stopped():
        """Yield from the getter until KeyboardInteruptted"""
        while True:
            try:
                yield getter()
            except KeyboardInterrupt:
                raise NoKeys

    return yield_till_stopped


yield_keycodes = _yielder(_get_keycodes)
yield_asciis = _yielder(get_ascii)
yield_ASCIIs = _yielder(get_ASCII)
yield_as_keys = _yielder(get_as_key)


def get_string():
    """A better str(_get_keycodes()) method"""
    keycodes = _get_keycodes()
    initial_code, codes = keycodes[0], keycodes[1:]
    initial_char = chr(initial_code)
    if initial_code == 27:
        initial_char = '\\e'
    elif not ascii.isgraph(initial_char):
        initial_char = '\\x%x' % initial_code
    chars = ''.join([chr(c) for c in codes])
    return ''.join((initial_char, chars))


def yield_asciis_old():
    """This one is deprecated"""
    k = get_ascii()
    while True:
        yield k


def ask_user(prompt, default=None):
    prompt_default = str('[%s]' % default) if default else ''
    print('%s %s? ' % (prompt, prompt_default), end='')
    result = getch().lower().strip()
    print()
    return result or default
