"""Methods to handle streams"""


import sys
from contextlib import contextmanager

from six import StringIO


@contextmanager
def swallow_stdout_stderr():
    """Divert stdout, stderr to strings"""
    saved_out = sys.stdout
    saved_err = sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    try:
        yield sys.stdout.getvalue(), sys.stderr.getvalue()
    finally:
        sys.stdout = saved_out
        sys.stderr = saved_err


@contextmanager
def swallow_stdout(stream=None):
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
def swallow_stderr(stream=None):
    saved = sys.stderr
    if stream is None:
        stream = StringIO()
    sys.stderr = stream
    try:
        yield
    finally:
        sys.stderr = saved
