import inspect
from dataclasses import dataclass
from typing import Callable


@dataclass
class MethodData:
    method: Callable


class Method(MethodData):
    """A callable method with some convenience attributes"""

    def __init__(self, method: Callable):
        super().__init__(method)
        self.code = self.method.__code__
        self.module = inspect.getmodule(self.method)
        self.doc = inspect.getdoc(self.method)
        frame = inspect.currentframe()
        self.caller = frame.f_back if frame else None

    def run(self, *args, **kwargs):
        return self.method(*args, **kwargs)

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            return getattr(self.code, f"co_{name}")


def _represent_args(*args, **kwargs):
    """Represent the aruments in a form suitable as a key (hashable)

    And which will be recognisable to user in error messages
    >>> print(_represent_args([1, 2], **{'fred':'here'}))
    [1, 2], fred='here'
    """
    argument_strings = [repr(a) for a in args]
    keyword_strings = ["=".join((k, repr(v))) for k, v in kwargs.items()]
    return ", ".join(argument_strings + keyword_strings)


def memoized(method):
    """A new method which acts like the given method but memoizeds args

    See https://en.wikipedia.org/wiki/Memoization for the general idea
        >>> @memoized
        ... def test(arg):
        ...     print('called')
        ...     return arg + 1
        >>> test(1)
        called
        2
        >>> test(2)
        called
        3
        >>> test(1)
        2

    The returned method also has an attached method "invalidate"
        which removes given values from the cache
        Or empties the cache if no values are given
        >>> test.invalidate(2)
        >>> test(1)
        2
        >>> test(2)
        called
        3
    """
    method.cache = {}

    def invalidate(*args, **kwargs):
        key = _represent_args(*args, **kwargs)
        if not key:
            method.cache = {}
        elif key in method.cache:
            del method.cache[key]
        else:
            raise KeyError(f"Not prevously cached: {method.__name__}({key})")

    def new_method(*args, **kwargs):
        """Cache the args and return values of the call

        The key cached is the repr() of args
            This allows more types of values to be used as keys to the cache
            Such as lists and tuples
        """
        key = _represent_args(*args, **kwargs)
        if key not in method.cache:
            method.cache[key] = method(*args, **kwargs)
        return method.cache[key]

    new_method.invalidate = invalidate
    new_method.__doc__ = method.__doc__
    new_method.__name__ = f"memoized({method.__name__})"
    return new_method
