"""Methods to handle streams"""


import sys
from contextlib import contextmanager
from typing import Generator
from typing import Optional
from typing import TextIO
from typing import Tuple

from six import StringIO


class Print():
    """
    """
    def out(*args, **kwargs):
        """Direct print() to sys.stdout"""
        kwargs["file"] = sys.stdout
        print(*args, **kwargs)

    def err(*args, **kwargs):
        """Direct print() to sys.stderr"""
        kwargs["file"] = sys.stderr
        print(*args, **kwargs)

std = Print()


def print_out(*args, **kwargs):
    """Direct print() to sys.stdout

    This function only exists to rhyme with print_err() below
    """
    print(*args, **kwargs)


def print_err(*args, **kwargs):
    """Direct print() to sys.stderr"""
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


@contextmanager
def swallow_stdout(stream: Optional[TextIO] = None) -> Generator[TextIO, None, None]:
    """Divert stdout into the given stream

    >>> with swallow_stdout() as stream:
    ...     print("hello", end="")
    ...
    >>> assert stream.getvalue() == "hello"
    """
    saved = sys.stdout
    if stream is None:
        stream = StringIO()
    sys.stdout = stream
    try:
        yield stream
    finally:
        sys.stdout = saved


@contextmanager
def swallow_stderr(stream: Optional[TextIO] = None) -> Generator[TextIO, None, None]:
    """Divert stderr into the given stream

    >>> with swallow_stderr() as string:
    ...     print("hello", end="", file=sys.stderr)
    ...
    >>> assert string.getvalue() == "hello"
    """
    saved = sys.stderr
    if stream is None:
        stream = StringIO()
    sys.stderr = stream
    try:
        yield stream
    finally:
        sys.stderr = saved


@contextmanager
def swallow_std() -> Generator[Tuple[TextIO, TextIO], None, None]:
    """Divert stdout and stderr to the given stream

    >>> with swallow_std() as streams:
    ...     print("hello", end=" ", file=sys.stderr)
    ...     print("world", end="", file=sys.stderr)
    ...
    >>> assert streams[0].getvalue() + streams[1].getvalue() == "hello world"
    """
    saved = sys.stdout, sys.stderr
    out, err = StringIO(), StringIO()
    sys.stdout = out
    sys.stderr = err
    try:
        yield out, err
    finally:
        sys.stdout, sys.stderr = saved
