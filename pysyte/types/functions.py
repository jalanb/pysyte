"""Handle functions for pysyte

>>> from pysyte.types import functions

>>> def fred(i: int = 0, s: str = "") -> str:
...     '''If in doubt, call it Fred'''
...     return "fred"

>>> foo = functions.function(fred)
>>> assert "def fred" in foo.code
"""

import ast
from contextlib import contextmanager
from dataclasses import dataclass
from functools import singledispatch
import inspect
from types import FrameType
from types import ModuleType
from collections.abc import Callable
from typing import Optional

from lazy import lazy
from pym.ast import parse


@dataclass
class Function:
    """A callable function with some convenience attributes"""

    callable: Callable

    def __post_init__(self):
        self.code = self.callable.__code__
        self.post_init_frame = inspect.currentframe()
        assert self.post_init_frame

    def __str__(self):
        return self.code

    def __repr__(self):
        return '\n'.join(
            [
                f"<{self.__class__.__name__} {self.module}{self.name}",
                "",
                self.doc,
            ]
        )

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        return self.callable(*args, **kwargs)

    @property
    def name(self) -> ModuleType | None:
        return self.callable.name

    @property
    def module(self) -> ModuleType | None:
        return inspect.getmodule(self.callable)

    @property
    def doc(self) -> str:
        return inspect.getdoc(self.callable) or ""

    @property
    def caller(self) -> FrameType | None:
        return self.post_init_frame.f_back

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            if name == "__file__":
                name = "filename"
            if hasattr(self.code, f"co_{name}"):
                return getattr(self.code, f"co_{name}")
            raise


class NoFunction(Function):
    """An empty function

    >>> nm = NoFunction()
    >>> assert not nm
    >>> assert nm == NoFunction(None) == NoFunction(0) == NoFunction(False)
    """

    def __init__(self, thing: Any = lambda: ""):
        def thingy():
            return ""

        self.thing = thing or thingy

    def __str__(self):
        return ""

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def __bool__(self):
        return False

    def __eq__(self, other):
        return not other


@singledispatch
def makefunction(arg) -> Function:
    """In the face of ambiguity, refuse the temptation to guess."""
    raise NotImplementedError(f"What is {arg!r} ?")


@makefunction.register(type(None))
def _mm(arg) -> Function:
    """Make no function from nothing

    >>> assert not makefunction(None)
    """
    return NoFunction()


@makefunction.register(Callable)
def __mm(arg) -> Function:
    """Make a function from a Callable

    >>> fred = lambda: "fred"
    >>> assert function(fred) == Function(fred)
    """
    return Function(arg)


@makefunction.register(types.FrameType)
def ___mm(arg) -> Function:
    """Find a function in the frame's caller"""
    if not arg:
        return NoFunction()
    caller = arg.f_back
    if not caller:
        return NoFunction()
    code = caller.f_globals.get(caller.f_code.co_name)
    if not code:
        return NoFunction()
    return Function(code)


# You’ll eventually want to handle:
#   •   CodeType: needs a lookup to find the real Callable that wraps it (check globals(), locals(), dir(cls) etc.)
#   •   FunctionType, BuiltinFunctionType: trivial if covered by Callable
#   •   MethodType: possibly worth special-casing to preserve self, __func__, etc.
#   •   staticmethod, classmethod: if needed, unwrap via .__func__
#   •   property: unwrap .fget
#   •   And maybe types.TracebackType, GeneratorType, or CoroutineType if you want to go deep

function = makefunction


@contextmanager
def caller():
    yield inspect.currentframe().f_back.f_back.f_back


def _represent_args(*args, **kwargs):
    """Represent the aruments in a form suitable as a key (hashable)

    And which will be recognisable to user in error messages
    >>> print(_represent_args([1, 2], **{"fred": "here"}))
    [1, 2], fred='here'
    """
    argument_strings = [repr(a) for a in args]
    keyword_strings = ["=".join((k, repr(v))) for k, v in kwargs.items()]
    return ", ".join(argument_strings + keyword_strings)


def none_args(*args, **kwargs):
    """Whether there are no args, or all args are falsy

    >>> assert none_args()
    >>> assert none_args(None)
    >>> assert none_args(x=None)
    >>> assert none_args(None, "", 0, x=None, y=[])
    >>> assert not none_args(1)
    """
    arguments = args + kwargs.values()
    return not arguments or all(not _ for _ in arguments)


def memoized(function):
    """A new function which acts like the given function but memoizeds args

    See https://en.wikipedia.org/wiki/Memoization for the general idea
        >>> @memoized
        ... def test(arg):
        ...     print("called")
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

    The returned function also has an attached method "invalidate"
        which removes given values from the cache
        Or empties the cache if no values are given
        >>> test.invalidate(2)
        >>> test(1)
        2
        >>> test(2)
        called
        3
    """
    function.cache = {}

    def invalidate(*args, **kwargs):
        key = _represent_args(*args, **kwargs)
        if not key:
            function.cache = {}
        elif key in function.cache:
            del function.cache[key]
        else:
            raise KeyError(f"Not prevously cached: {function.__name__}({key})")

    def new_function(*args, **kwargs):
        """Cache the args and return values of the call

        The key cached is the repr() of args
            This allows more types of values to be used as keys to the cache
            Such as lists and tuples
        """
        key = _represent_args(*args, **kwargs)
        if key not in function.cache:
            function.cache[key] = function(*args, **kwargs)
        return function.cache[key]

    new_function.invalidate = invalidate
    new_function.__doc__ = function.__doc__
    new_function.__name__ = f"memoized({function.__name__})"
    return new_function


def read_lines(path: str, line: int) -> list[str]:
    """Read the source of the function starting at that line in that file"""
    with open(path) as stream:
        text = stream.read()
        return text.splitlines()[line - 1 :]


@dataclass
class Def:
    path: str
    line: int
    source: str

    def __str__(self):
        return self.source

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.path}:{self.line}\n{self.source}\n>"

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
    for string in strings:
        if not string:
            continue
        indent = len(string) - len(string.lstrip())
        if indent <= def_indent:
            break
    source = "\n".join(lines[: len(strings)])
    return Def(path, line, source)
