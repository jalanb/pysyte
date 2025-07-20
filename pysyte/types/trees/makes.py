import os
import re
import stat
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

from pysyte.types.trees import strings
from pysyte.types.trees.dirs import DirectPath
from pysyte.types.trees.errors import MissingImport
from pysyte.types.trees.files import FilePath
from pysyte.types.trees.paths import Path
from pysyte.types.trees.paths import Paths
from pysyte.types.trees.strings import NoPath


class Pathed(Protocol):
    path: Any


@singledispatch
def makepath(arg) -> strings.StringPath:
    raise TypeError(f"Refuse the temptation to guess the type of {arg!r}")
    return makepath(arg.path)


@makepath.register(type(None))
def _mp(arg) -> strings.StringPath:
    """In the face of ambiguity, refuse the temptation to guess."""
    raise NotImplementedError(f"Zilch: {arg!r}")


@makepath.register(Pathed)
def makepath(arg) -> strings.StringPath:
    return makepath(arg.path)


@makepath.register(str)
def ____mp(arg) -> strings.StringPath:
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
    v = os.path.expandvars(arg)
    u = os.path.expanduser(v)
    if arg == u:
        return strings.NoPath(arg)
    if os.path.exists(u):
        return makepath(u)
    return strings.NoPath(arg)


def imports():
    return {sys, os, re, stat}


@makepath.register(type(os))
def _____mp(arg) -> strings.StringPath:
    """Make a path from a module"""
    if arg.__name__ == "builtins":
        return strings.NoPath("builtins")
    try:
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
def ______mp(arg) -> strings.StringPath:
    """Make a path from a function's module"""
    terminal_regexp = re.compile("<(stdin|.*python-input.*)>")
    method = getattr(arg, "__wrapped__", arg)
    filename = method.__code__.co_filename
    if terminal_regexp.match(filename):
        return strings.NoPath(filename)
    return _make_module_path(method)


class Fred:
    pass


@makepath.register(type(Fred))
def _______mp(arg) -> strings.StringPath:
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
def make_path_path(arg) -> strings.StringPath:
    return arg


# Alias for backward compatibility
path = makepath
