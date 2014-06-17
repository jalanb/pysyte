"""Some keyboard handling code"""


import getch


def get_a_key():
    key = getch.getch()
    if ord(key) == 3:
        raise KeyboardInterrupt
    return key


def get_letter():
    for key in get_a_key():
        if key.isupper() or key.islower():
            return key
