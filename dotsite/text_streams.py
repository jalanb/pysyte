"""Module to handle streams of text"""

import os
import sys
import contextlib
from io import StringIO

from dotsite.platforms import get_clipboard_data


def clipboard_stream(name=None):
    stream = StringIO(get_clipboard_data())
    stream.name = name or '<clipboard>'
    return stream


@contextlib.contextmanager
def clipin():
    yield clipboard_stream()


@contextlib.contextmanager
def files():
    """Yield streams of text given to a program

    If there are files in sys.argv, yield them
    yield sys.stdin
    """
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            yield open(arg)


@contextlib.contextmanager
def all():
    with files() as streams:
        yield streams
    yield clipboard_stream()
    yield sys.stdin


def first_file():
    try:
        arg_stream = files()
        first, *_rest = arg_stream
        return first
    except StopIteration:
        return ''


def full_lines(stream):
    for line in stream.readlines():
        stripped = line.rstrip()
        if stripped:
            yield stripped
