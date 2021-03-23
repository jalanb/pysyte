"""Methods to handle streams"""


import sys
from contextlib import contextmanager
from typing import Optional
from typing import TextIO
from typing import Generator

from six import StringIO


@contextmanager
def swallow_stdout(stream: Optional[TextIO] = None) -> Generator[TextIO, None, None]:
    """Divert stdout into the given stream

    >>> with swallow_stdout() as stream:
    ...     print('hello', end='')
    >>> assert stream.getvalue() == 'hello'
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
    """Divert stdout into the given stream

    >>> with swallow_stdout() as string:
    ...     print('hello', end='', stream=sys.stderr)
    >>> assert string.getvalue() == 'hello'
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
def swallow_std(stream: Optional[TextIO] = None) -> Generator[TextIO, None, None]:
    """Divert stdout and stderr to the given stream

    >>> with swallow_std() as streams:
    ...     print('hello', end=' ', stream=sys.stderr)
    ...     print('world', end='', stream=sys.stderr)
    >>> assert streams[0].get_value() + streams[1].get_value() == 'hello world'
    """
    raise NotImplementedError


def show_lines(lines: list, prefix: str, stream: TextIO) -> None:
    """Print those lines, with that prefix, to that stream

    >>> show_lines(('1', '2'), 'line ', sys.stdout)
    line 1
    line 2
    """
    print("\n{prefix}".join(lines))
