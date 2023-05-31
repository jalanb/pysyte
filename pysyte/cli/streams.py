"""Module to handle streams of text from cli arguments"""

import os
import sys

from six import StringIO

from pysyte import iteration
from pysyte.cli import arguments
from pysyte.oss.platforms import get_clipboard_data


def parse_args(description=""):
    """Parse out command line arguments"""
    parser = arguments.parser(description or __doc__)
    parser.positional("streams", help="streams to use")
    parser.boolean("p", "paste", help="paste text from clipboard")
    parser.boolean("i", "stdin", help="wait for text from stdin")
    return parser.parse_args()


def args(parsed_args, name="streams", files_only=False):
    """Interpret parsed args to streams"""
    streams = []
    strings = parsed_args.get_strings(name)
    files = [s for s in strings if os.path.isfile(s)]
    if files:
        streams = [open(f) for f in files]
    if strings or files_only:
        return streams
    if "-" in files or getattr(parsed_args, "stdin", False):
        streams = [sys.stdin]
    if getattr(parsed_args, "paste", False):
        streams.append(clipboard_stream())
    return streams


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
