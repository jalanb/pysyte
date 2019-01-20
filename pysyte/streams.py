"""Methods to handle streams"""


import sys
from contextlib import contextmanager

from six import StringIO


@contextmanager
def swallow_stdout(stream=None):
    """Divert stdout into the given stream

    >>> string = StringIO()
    >>> with swallow_stdout(string):
    ...     print('hello')
    >>> assert string.getvalue().rstrip() == 'hello'
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
def swallow_stderr(stream=None):
    saved = sys.stderr
    if stream is None:
        stream = StringIO()
    sys.stderr = stream
    try:
        yield
    finally:
        sys.stderr = saved
