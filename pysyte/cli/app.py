"""Provide a runnable app to pysyte"""

import sys
from bdb import BdbQuit
from contextlib import ContextDecorator

from pysyte.cli import exits
from pysyte.cli.exceptions import rich_exceptions
from pysyte.types.functions import Function


def exit(function, locals_=None):
    exit_code = os.EX_FAIL
    with rich_exceptions(locals_ if locals_ else {}):
        try:
            exit_code = os.EX_OK if function() else os.EX_FAIL
        except BdbQuit:
            exit_code = exits.pass_
    sys.exit(exit_code)


class App(Function, ContextDecorator):
    def __enter__(self):
        self.exit_code = None
        return self

    def run(self, *args, **kwargs):
        kwargs["app"] = self
        self.exit_code = super().run(*args, **kwargs)

    def __exit__(self, *exc):
        return self.exit_code
