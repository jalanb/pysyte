"""Some keyboard handling code"""

from __future__ import print_function

import sys


from getch import get_as_key


def get_letter():
    while True:
        key = get_as_key()
        try:
            if key.isupper() or key.islower():
                return key
        except AttributeError:
            print(key)
            continue


def quit_on_q():
    try:
        key = get_as_key()
        if key in 'qQ':
            sys.exit()
        return key
    except KeyboardInterrupt:
        sys.exit()
