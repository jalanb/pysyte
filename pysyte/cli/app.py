"""Provide a runnable app to pysyte"""

from contextlib import ContextDecorator

from pysyte.types.methods import Method


class App(Method, ContextDecorator):
    def __enter__(self):
        self.exit_code = None
        return self

    def run(self, *args, **kwargs):
        self.exit_code = super().run(*args, **kwargs)

    def __exit__(self, *exc):
        return self.exit_code
