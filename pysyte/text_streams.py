"""Module to handle streams of text"""

import os
import sys
import contextlib
from itertools import chain

from six import StringIO

from pysyte import args as arguments
from pysyte import iteration
from pysyte.platforms import get_clipboard_data

def parse_args():
    """Parse out command line arguments"""
    parser = arguments.parser(__doc__)
    parser.args('streams', help='streams to use')
    parser.opt('-p', '--paste', 'paste text from clipboard')
    parser.opt('-i', '--stdin', 'wait for text from stdin')
    return parser.parse_args()


def args(parsed_args, name=None):
    """Interpret parsed args to streams"""
    strings = parsed_args.get_strings(name)
    files = [s for s in strings if os.path.isfile(s)]
    if files:
        streams = [open(f) for f in files]
    else:
        streams = []
    if getattr(parsed_args, 'paste', not files):
        streams.append(clipboard_stream())
    if getattr(parsed_args, 'stdin', False):
        streams.append(sys.stdin)
    elif not streams:
        streams = [sys.stdin]
    return streams


def clipboard_stream(name=None):
    stream = StringIO(get_clipboard_data())
    stream.name = name or '<clipboard>'
    return stream


def _arg_files():
    return [a for a in sys.argv[1:] if os.path.isfile(a)]


def _arg_streams():
    """yield streams to all arg.isfile()"""
    for path in _arg_files():
        yield open(path)


def all():
    more = iter([clipboard_stream(), sys.stdin])
    return chain(_arg_streams(), more)


def first():
    return iteration.first(all())


def last():
    return iteration.last(all())


def some():
    if sys.argv[1:]:
        assert _arg_files()
    return any()


def _any():
    try:
        stream = iteration.first(_arg_streams())
        if stream:
            return _arg_streams()
    except ValueError:
        return iter([clipboard_stream(), sys.stdin])


def first_file():
    try:
        return iteration.first(_arg_streams())
    except ValueError:
        return None


def full_lines(stream):
    for line in stream.readlines():
        stripped = line.rstrip()
        if stripped:
            yield stripped
