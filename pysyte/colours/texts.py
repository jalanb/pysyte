"""Provide methods to put colours in texts


Inspired by http://stackoverflow.com/questions/384076/how-can-i-make-the-python-logging-output-to-be-colored  # noqa
Conversion from RGB to xterm 256 colours based on values in http://www.frexx.de/xterm-256-notes/data/xterm-colortest  # noqa
Conversion from rgb.txt names to RGB inspired by https://github.com/lilydjwg/winterpy/blob/master/pyexe/gui2term.py  # noqa
"""


from __future__ import absolute_import
import os

from pysyte.colours import ansi_escapes
from pysyte.colours import colour_numbers


class ColouredTail(object):
    """The tail of a string that is being coloured

    Also holds a head, all of string before the tail
        When treated as a string, gives head + tail
    """
    def __init__(self, head, string):
        self._tail = string
        self._head = head

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.head!r}{self.tail!r}>'

    def __str__(self):
        return ''.join((self.head, self.tail))

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def head(self):
        if self._head:
            return str(self._head)
        return ''

    @property
    def tail(self):
        if self._tail:
            return str(self._tail)
        return ''

    def colour_text(self, *args):
        new = colour_text(*args, head='')
        return ColouredTail(str(self), new)

    colour = text = colour_text


def colour_text(text, name=None, head=None):
    string = str(text)
    colour_ = colour_numbers.name_to_int(name) if name else False
    return ColouredTail(
        head or '',
        ansi_escapes.foreground_string(string, colour_) if colour_ else string
    )

colour = text = colour_text


def colour_initial(string, name):
    return colour(string[0], name).colour(string[1:])


def colour_initials(strings, name):
    return colour(''.join([str(colour_initial(s, name)) for s in strings]))


def prompt_text(string, name):
    number = colour_numbers.name_to_int(name)
    return ansi_escapes.prompt_string(string, number)
