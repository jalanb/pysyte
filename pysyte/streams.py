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

    >>> string = StringIO()
    >>> with swallow_stdout(string):
    ...     print('hello', end='')
    >>> assert string.getvalue() == 'hello'
    """
    saved = sys.stdout
    if stream is None:
        stream = StringIO()
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = saved


@contextmanager
def swallow_stderr(stream: Optional[TextIO] = None) -> Generator[TextIO, None, None]:
    saved = sys.stderr
    if stream is None:
        stream = StringIO()
    sys.stderr = stream
    try:
        yield
    finally:
        sys.stderr = saved


@contextmanager
def swallow_std(stream: Optional[TextIO] = None) -> Generator[TextIO, None, None]:
    raise NotImplementedError

def show_lines(lines: list, prefix: str, stream: TextIO) -> None:
    raise NotImplementedError
