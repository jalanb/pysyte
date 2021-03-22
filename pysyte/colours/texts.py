"""Provide methods to put colours in texts


Inspired by http://stackoverflow.com/questions/384076/how-can-i-make-the-python-logging-output-to-be-colored  # noqa
# Conversion from RGB to xterm 256 colours based on values in http://www.frexx.de/xterm-256-notes/data/xterm-colortest  # noqa
Nicer version: https://jonasjacek.github.io/colors/
Conversion from rgb.txt names to RGB inspired by https://github.com/lilydjwg/winterpy/blob/master/pyexe/gui2term.py  # noqa
"""


from __future__ import absolute_import
from functools import partial

from pysyte.colours import ansi_escapes
from pysyte.colours import colour_names
from pysyte.colours import colour_numbers


class ColouredTail(object):
    """The tail of a string that is being coloured

    Also holds its head
        which is all of the string before the tail

    When treated as a string, gives head + tail
    """

    def __init__(self, head, tail):
        self.head = str(head) if head else ""
        self.tail = str(tail) if tail else ""
        self.add_colour_names()

    def add_colour_names(self):
        for colour_name in colour_names.cga():
            attr_name = colour_name.replace(" ", "_")
            setattr(self, attr_name, partial(self.colour_text, colour_name))
        setattr(self, "reddy", partial(self.colour_text, "light red"))
        setattr(self, "none", partial(self.colour_text, None))

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.head!r}{self.tail!r}>"

    def __str__(self):
        return f"{self.head}{self.tail}"

    def __eq__(self, other):
        return str(self) == str(other)

    def colour_text(self, *args):
        try:
            colour_name, text = args
        except ValueError:
            colour_name = None
            text = args[0]
        new = colour_text(colour_name, text, head="")
        return ColouredTail(str(self), new)

    colour = text = colour_text


def colour_text(colour_name, text, head=None):
    return ColouredTail(
        head or "",
        ansi_escapes.foreground_string(
            str(text),
            colour_numbers.name_to_id(colour_name),
        ),
    )


colour = text = colour_text

for name in colour_names.cga():
    globals()[name] = partial(colour_text, name)
none = partial(colour_text, None)


def colour_initial(colour_name, string):
    return colour(colour_name, string[0]).colour(None, string[1:])


def colour_initials(colour_name, strings):
    return "".join([str(colour_initial(colour_name, s)) for s in strings])


def prompt_text(colour_name, string):
    number = colour_numbers.name_to_id(colour_name)
    return ansi_escapes.prompt_string(string, number)
