"""Provide a getch() method to get single chars from a terminal


Do not wait on carriage returns

Adapted from
    http://code.activestate.com/recipes/134892/
    Without the redundant classes of that code
        but keeping the implementatation

    And reducing down to just the tty version
        No need here for Windows/Carbon
"""


import sys
import tty
import termios
import curses.ascii


def getch():
    """Read one byte from sys.stdin

    Use raw mode, and restore to unraw before returning
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_ord_ch():
    """Get the ord value of a byte from stdin"""
    return ord(getch())


def get_key():
    """Get a key value from stdin

    This method should be used to get non-ASCII keys, e.g. <F12>

    A tuple is returned with 1, 2, or 3 items
        which are the bytes from stdin for that key
        The first item is an int (ord value), others are chars
        e.g. for 'A' it returns (65,)
        e.g. for <F12> it returns (27, '[', '2')
    """
    i = get_ord_ch()
    if not i:
        return i, getch()
    if i == 27:
        return i, getch(), getch()
    return (i,)


def show_get_key():
    """Show output of the get_key() method"""
    key = get_key()
    k = key[0]
    c = chr(k)
    if curses.ascii.isgraph(c):
        print repr(c),
    else:
        print repr(k),
    print key[1:]


if __name__ == '__main__':
    show_get_key()
