"""Make a method to suppress sys.stdout and/or sys.stderr

>>> from pysyte.streams import print_out, print_err

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

from _io import TextIOWrapper as Wrapper
from sys import stderr as err
from sys import stdout as out
from typing import Callable
from typing import List
import contextlib
import io


def quieten(name: str, streams: List[Wrapper]) -> Callable:
    @contextlib.contextmanager
    def method():
        stdout = io.StringIO()
        stderr = io.StringIO()
        if out in streams:
            if err in streams:
                with contextlib.redirect_stdout(stdout):
                    with contextlib.redirect_stderr(sdtderr):
                        yield
            else:
                with contextlib.redirect_stdout(stdout):
                    yield
        elif err in streams:
            with contextlib.redirect_stderr(sdtderr):
                yield

        method.stdout, method.stderr = stdout.getvalue(), stderr.getvalue()

    method.stdout, method.stderr = "", ""
    return method


quietly = quieten("quietly", [err])
Quietly = quieten("Quietly", [out])
QUIETLY = quieten("QUIETLY", [out, err])
