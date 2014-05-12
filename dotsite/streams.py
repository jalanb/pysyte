"""Methods to handle streams"""


import sys
from cStringIO import StringIO
from contextlib import contextmanager


@contextmanager
def swallow_stdout(stream=None):
    """Divert stdout into the given stream

    >>> from cStringIO import StringIO
    >>> string = StringIO()
    >>> with swallow_stdout(string):
    ...     print 'hello',
    >>> string.getvalue() == 'hello'
    True
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
