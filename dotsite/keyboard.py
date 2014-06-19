"""Some keyboard handling code"""

import sys


import getch


def get_a_key():
    key = getch.getch()
    if ord(key) == 3:
        raise KeyboardInterrupt
    return key


def get_letter():
    while True:
        key = get_a_key()
        if key.isupper() or key.islower():
            return key


def quit_on_q():
    try:
        key = get_a_key()
        if key in 'qQ':
            sys.exit()
    except KeyboardInterrupt:
        sys.exit()
