"""Methods to handle streams"""

from contextlib import contextmanager
from typing import Generator
from typing import Optional
from typing import TextIO
from typing import Tuple

from io import StringIO


class Print:
    """ """

    def in_(self, *args, **kwargs) -> str:
        """Read from sys.stdin"""
        return sys.stdin.read(*args, **kwargs)

    def out(*args, **kwargs):
        """Direct print() to sys.stdout"""
        kwargs["file"] = sys.stdout
        print(*args, **kwargs)

    def err(*args, **kwargs):
        """Direct print() to sys.stderr"""
        kwargs["file"] = sys.stderr
        print(*args, **kwargs)

    def write(text: str):
        return sys.stdout.write(text)

    def flush():
        return sys.stdout.flush()

    def in_fileno(self):
        """Get stdin's fileno"""
        return sys.stdin.fileno()


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
        stream.seek(0)
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
        stream.seek(0)
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
    out_stream = StringIO()
    err_stream = StringIO()
    with swallow_stdout(out_stream), swallow_stderr(err_stream):
        yield out_stream, err_stream
        out_stream.seek(0)
        err_stream.seek(0)

@contextmanager
def swallow_stdin(text: str) -> Generator[StringIO, None, None]:
    """Feed the given text into sys.stdin as if typed

    >>> from pysyte.oss import getch
    >>> with swallow_stdin("Hello"):
    ...     assert getch.get_key() == 'H'
    """
    saved = sys.stdin
    stream = StringIO(text)
    sys.stdin = stream
    try:
        yield stream
    finally:
        sys.stdin = saved
