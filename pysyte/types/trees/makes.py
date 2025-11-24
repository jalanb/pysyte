import os
import re
import sys
from functools import singledispatch
from importlib import import_module
from typing import (
    Any,
    Protocol,
)

from pysyte.types.trees.errors import MissingImport
from pysyte.types.trees.paths import Path, Paths
from pysyte.types.trees.strings import NoPath, StringPath


class Pathed(Protocol):
    path: Any


@singledispatch
def makepath(arg: Pathed) -> StringPath:
    return makepath(arg.path)


@makepath.register(type(None))
def _mp(arg) -> StringPath:
    """Make no path from nothing

    >>> p = makepath(None)
    >>> assert not p
    """
    return NoPath()


@makepath.register(str)
def ____mp(arg) -> StringPath:
    """Make a path from a string

    Expand out any variables, home squiggles, and normalise it
    See also http://stackoverflow.com/questions/26403972

    See also Lynton Kwesi Johnson:
        The Eagle and The Bear
            Have people living in fear
            Of impending nuclear warfare
    """
    if not arg:
        return makepath(None)
    if os.path.isfile(arg):
        from pysyte.types.trees.files import FilePath

        return FilePath(arg)
    if os.path.isdir(arg):
        from pysyte.types.trees.dirs import DirectPath

        string = arg if arg == "/" else arg.rstrip("/")
        return DirectPath(string)
    expanded_path = os.path.expandvars(arg)
    full_path = os.path.expanduser(expanded_path)
    if arg == full_path:
        # then nothing has changed since we tried above
        return NoPath(arg)
    if os.path.exists(full_path):
        return makepath(full_path)
    return NoPath(arg)


@makepath.register(type(os))
def _____mp(arg) -> StringPath:
    """Make a path from a module

    >>> import os, sys
    >>> assert makepath(os)
    >>> assert not makepath(sys)
    """
    if arg.__name__ in sys.builtin_module_names:
        return NoPath(arg.__name__)
    if hasattr(arg, "__file__"):
        return makepath(arg.__file__)
    if hasattr(arg, '__path__'):
        p, *_ = arg.__path__
        return makepath(p)
    if hasattr(arg, '__spec__') and arg.__spec__:
        if arg.__spec__.origin:
            return makepath(arg.__spec__.origin)
        if arg.__spec__.submodule_search_locations:
            l, *_ = arg.__spec__.submodule_search_locations
            return makepath(l)
    if arg.__name__ not in sys.modules:
        raise MissingImport(arg)
    return NoPath(arg.__name__)


def _make_module_path(arg):
    """Make a path from a thing that has a module

    classes and functions have modules, they'll be needing this
    """
    try:
        return makepath(import_module(arg.__module__))
    except (AttributeError, ModuleNotFoundError):
        return None


@makepath.register(type(makepath))
def ______mp(arg) -> StringPath:
    """Make a path from a function's module"""
    terminal_regexp = re.compile("<(stdin|.*python-input.*)>")
    method = getattr(arg, "__wrapped__", arg)
    filename = method.__code__.co_filename
    if terminal_regexp.match(filename):
        return NoPath(filename)
    return _make_module_path(method)


class Fred:
    pass


@makepath.register(type(Fred))
def _______mp(arg) -> StringPath:
    """Make a path from a class's module"""
    return _make_module_path(arg)


@singledispatch
def makepaths(arg) -> Paths:
    """Refuse the temptation again."""
    return [makepath(arg)]


@makepaths.register(type(None))
def _mps(arg) -> Paths:
    return Paths([])


@makepaths.register(list)
def __mps(arg) -> Paths:
    return Paths([makepath(_) for _ in arg])


@makepaths.register(str)
def ___mps(arg) -> Paths:
    return Paths([makepath(arg)])


@makepaths.register(StringPath)
def make_string_paths(arg) -> Paths:
    return Paths([arg])


@makepath.register(Path)
def make_path_path(arg) -> StringPath:
    return arg


# Alias for backward compatibility
path = makepath
