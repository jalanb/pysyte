"""Provide a runnable app to pysyte"""

import os
import sys

from contextlib import ContextDecorator

from pysyte.types.methods import Method
from pysyte.cli.exceptions import rich_exceptions

PASS = os.EX_OK
FAIL = not PASS


def exit(method, locals_=None):
    exit_code = FAIL
    with rich_exceptions(locals_ if locals_ else {}):
        exit_code = PASS if method() else FAIL
    sys.exit(exit_code)


class App(Method, ContextDecorator):
    def __enter__(self):
        self.exit_code = None
        return self

    def run(self, *args, **kwargs):
        self.exit_code = super().run(*args, **kwargs)

    def __exit__(self, *exc):
        return self.exit_code
