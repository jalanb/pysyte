"""Make a method to suppress sys.stdout and/or sys.stderr

>>> from pysyte.streams import std

Doctest normally shows all streams

>>> print_out("Hello")
>>> print_err("World")
Hello
World

Suppress stderr
>>> with quietly as suppressor:
...     print_out("Hello")
...     print_err("World")
...
Hello

>>> assert "World" in suppressor.stderr

"""

import contextlib
import io


@contextlib.contextmanager
def quietly():
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
        yield


@contextlib.contextmanager
def Quietly():
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        yield


@contextlib.contextmanager
def QUIETLY():
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        with contextlib.redirect_stderr(stderr):
            yield
