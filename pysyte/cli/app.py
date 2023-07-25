"""Provide a runnable app to pysyte"""

from bdb import BdbQuit
import sys

from contextlib import ContextDecorator

from pysyte.types.methods import Method
from pysyte.cli.exceptions import rich_exceptions
from pysyte import os


def exit(method, locals_=None):
    exit_code = os.EX_FAIL
    with rich_exceptions(locals_ if locals_ else {}):
        try:
            exit_code = os.EX_OK if method() else os.EX_FAIL
        except BdbQuit:
            exit_code = os.EX_OK
    sys.exit(exit_code)


class App(Method, ContextDecorator):
    def __enter__(self):
        self.exit_code = None
        return self

    def run(self, *args, **kwargs):
        kwargs["app"] = self
        self.exit_code = super().run(*args, **kwargs)

    def __exit__(self, *exc):
        return self.exit_code
