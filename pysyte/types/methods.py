"""Handle methods for pysyte

>>> from pysyte.types import methods

>>> def fred(i: int = 0, s: str = "") -> str:
...     '''If in doubt, call it Fred'''
...     return "fred"

>>> foo = methods.method(fred)
>>> assert "def fred" in foo.code
"""

import inspect
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable
from typing import Optional
from types import FrameType
from types import ModuleType


def unwrap(method: Callable) -> Callable:
    """Get the original method from a method, even if it's wrapped """
    return getattr(method, "__wrapped__", method)


@dataclass
class Method:
    """A callable object, usually a function or method"""

    method: Callable

    def __post_init__(self):
        self.code = self.method.__code__
        unwrapped = unwrap(self.method)
        self.wrapped = unwrapped if unwrapped != self.method else None
        self.init_frame = inspect.currentframe()
        self.callers = [self.init_frame.f_back]

    def __str__(self):
        return self.code

    def __repr__(self):
        return f"""<{self.__class__.__name__} {self.module}{self.name}

{self.doc}
>"""

    def run(self, *args, **kwargs):
        return self.method(*args, **kwargs)

    @property
    def name(self) -> Optional[ModuleType]:
        return self.method.name

    def __call__(self, *args, **kwargs):
        call_frame = inspect.currentframe()
        self.callers.append(call_frame.f_back)
        return self.method(*args, **kwargs)

    @property
    def caller(self) -> Optional[FrameType]:
        return self.callers[-1]

    @property
    def filename(self) -> str:
        return self.code.co_filename

    @property
    def module(self) -> Optional[ModuleType]:
        return inspect.getmodule(self.method)

    @property
    def module_name(self) -> Optional[ModuleType]:
        return self.method.__module__

    @property
    def doc(self) -> str:
        return inspect.getdoc(self.method) or ""

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            if name == "__file__":
                name = "filename"
            if hasattr(self.code, f"co_{name}"):
                return getattr(self.code, f"co_{name}")
            raise


def method(callable: Callable) -> Method:
    """Convenience method to avoid importing capitals

    >>> fred = lambda : "fred"
    >>> assert method(fred) == Method(fred)
    """
    return Method(callable)


@contextmanager
def caller():
    yield inspect.currentframe().f_back.f_back.f_back


def _represent_args(*args, **kwargs):
    """Represent the aruments in a form suitable as a key (hashable)

    And which will be recognisable to user in error messages
    >>> print(_represent_args([1, 2], **{'fred': 'here'}))
    [1, 2], fred='here'
    """
    argument_strings = [repr(a) for a in args]
    keyword_strings = ["=".join((k, repr(v))) for k, v in kwargs.items()]
    return ", ".join(argument_strings + keyword_strings)


def none_args(*args, **kwargs)
    """Whether there are no args, or all args are falsy

    >>> assert none_args()
    >>> assert none_args(None)
    >>> assert none_args(x=None)
    >>> assert none_args(None, "", 0, x=None, y=[])
    >>> assert not none_args(1)
    """
    arguments = args + kwargs.values()
    return not arguments or all(not _ for _ in arguments)


def memoized(method):
    """A new method which acts like the given method but memoizeds args

    See https://en.wikipedia.org/wiki/Memoization for the general idea
        >>> @memoized
        ... def test(arg):
        ...     print('called')
        ...     return arg + 1
        ...
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


def read_lines(path: str, line: int) -> list[str]:
    """Read the source of the function starting at that line in that file"""
    with open(path) as stream:
        text = stream.read()
        return text.splitlines()[line - 1:]

@dataclass
class Def:
    path: str
    line: int
    source: str

    def __str__(self):
        return self.source

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.path}:{self.line}\n{self.source}\n>'

    @lazy
    def ast(self) -> ast.AST:
        return parse(self.source)

    @lazy
    def lines(self) -> list[str]:
        return self.source.splitlines()


def read_def(path: str, line: int) -> Def:
    """Read the function definition starting at that line in that file"""
    lines = read_lines(path, line)
    def_line, *strings = lines
    def_indent = len(def_line) - len(def_line.lstrip())
    for i, string in enumerate(strings):
        if not string:
            continue
        indent = len(string) - len(string.lstrip())
        if indent <= def_indent:
            break
    source = '\n'.join(lines[:i+1])
    return Def(path, line, source)
