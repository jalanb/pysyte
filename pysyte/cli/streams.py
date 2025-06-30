"""Module to handle streams of text from cli arguments"""

import os
import sys
from typing import TextIO

from dataclasses import dataclass
from io import StringIO

from pysyte import iteration
from pysyte.cli import arguments
from pysyte.oss.platforms import get_clipboard_data
from pysyte.types.trees.paths import path


@dataclass
class ParsedStreams:
    streams: list[TextIO]
    stdin: TextIO
    clipboard: TextIO


def parse_args(name:str="", docs:str="") -> ParsedStreams:
    """Parse out command line arguments"""
    parser = arguments.parser(docs or __doc__)
    if not name:
        name = "streams"
    parser.positional(name, help=f"{name} to use")
    parser.boolean("p", "paste", help="paste text from clipboard")
    parser.boolean("i", "stdin", help="wait for text from stdin")
    parsed = parser.parse_args()
    named = parsed.args(name)
    paths = [path(_) for _ in named]
    exists = [_ for _ in paths if _]
    return ParsedStreams(
        streams = [_.open() for _ in exists if _.isfile() or _.isdir()]
        stdin = parsed.stdin or StringIO("")
        clipboard = parsed.paste or StringIO("")
    )


def files(parsed_args, name=None):
    return args(parsed_args, name, True)


def all():
    yielded = False
    for path in _arg_files():
        with open(path) as stream:
            yield stream
        yielded = True
    if not yielded or "-" in sys.argv:
        yield sys.stdin


def some():
    if sys.argv[1:]:
        assert _arg_files()
    return any()


def clipboard_stream(name=None):
    stream = StringIO(get_clipboard_data())
    stream.name = name or "<clipboard>"
    return stream


def _arg_files():
    return [a for a in sys.argv[1:] if os.path.isfile(a)]


def _arg_streams():
    """yield streams to all arg.isfile()"""
    for path in _arg_files():
        with open(path) as stream:
            yield stream


def any():
    try:
        stream = iteration.first(_arg_streams())
        if stream:
            return _arg_streams()
    except ValueError:
        return iter([clipboard_stream(), sys.stdin])
