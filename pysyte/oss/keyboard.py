"""Some keyboard handling code"""


import sys


from pysyte.oss import getch


def _get_chosen_chars(chooser):
    while True:
        key = getch.get_as_key()
        try:
            if chooser(key):
                return key
        except AttributeError:
            print(key)
            continue


def get_digit():
    return _get_chosen_chars(lambda x: x.isdigit())


def get_letter():
    return _get_chosen_chars(lambda x: x.isupper() or x.islower())


def quit_on_q():
    try:
        key = getch.get_as_key()
        if key in "qQ":
            sys.exit()
        return key
    except KeyboardInterrupt:
        sys.exit()
