"""Provide a runnable app to pysyte"""

from contextlib import ContextDecorator

from pysyte.types.methods import Callable
from pysyte.types.methods import MethodData



class App(ContextDecorator, MethodData):
    def __init__(self, method: Callable):
        super(MethodData, self).__init__(method, 'run')

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


