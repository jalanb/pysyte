"""Make a method to suppress sys.stdout and/or sys.stderr

>>> from pysyte.streams import std

Doctest normally shows all streams

>>> std.out("Hello")
>>> std.err("World")
Hello
World

Suppress stderr
>>> with quietly as suppressor:
...     std.out("Hello")
...     std.err("World")
...
Hello

>>> assert "World" in suppressor.stderr

"""

from dataclasses import dataclass
import contextlib
import io
from sys import stderr as err
from sys import stdout as out
from typing import Callable

from _io import TextIOWrapper as Wrapper


@dataclass
class StdStreams:
    stdout: str = ""
    stderr: str = ""


def quieten(name: str, streams: list[Wrapper]) -> Callable:
    @contextlib.contextmanager
    def method():
        stdout = io.StringIO()
        stderr = io.StringIO()
        if out in streams:
            if err in streams:
                with contextlib.redirect_stdout(stdout):
                    with contextlib.redirect_stderr(stderr):
                        yield
            else:
                with contextlib.redirect_stdout(stdout):
                    yield
        elif err in streams:
            with contextlib.redirect_stderr(stderr):
                yield

        result = StdStreams(stdout.getvalue(), stderr.getvalue())
        return result

    return method


quietly = quieten("quietly", [err])
Quietly = quieten("Quietly", [out])
QUIETLY = quieten("QUIETLY", [out, err])
