"""Module to handle streams of text"""

import os
import sys
import contextlib
from itertools import chain

from six import StringIO

from pysyte import iteration
from pysyte.platforms import get_clipboard_data


def clipboard_stream(name=None):
    stream = StringIO(get_clipboard_data())
    stream.name = name or '<clipboard>'
    return stream


@contextlib.contextmanager
def clipin():
    yield clipboard_stream()


def arg_paths():
    return [a for a in sys.argv[1:] if os.path.isfile(a)]


def arg_files():
    """yield streams to all arg.isfile()"""
    for path in arg_paths():
        yield open(path)


def all():
    some = False
    for path in arg_paths():
        yield open(path)
        some = True
    if not some:
        yield sys.stdin


def first():
    return iteration.first(all())


def last():
    return iteration.last(all())


def any():
    try:
        stream = iteration.first(arg_files())
        if stream:
            return arg_files()
    except ValueError:
        return iter([clipboard_stream(), sys.stdin])


def first_file():
    try:
        return iteration.first(arg_files())
    except ValueError:
        return None


def full_lines(stream):
    for line in stream.readlines():
        stripped = line.rstrip()
        if stripped:
            yield stripped
