import os
import re
import stat
import sys
from functools import singledispatch
from importlib import import_module

from pysyte.types.trees import strings
from pysyte.types.trees.dirs import DirectPath
from pysyte.types.trees.errors import MissingImport
from pysyte.types.trees.files import FilePath


@singledispatch
def makepath(arg) -> strings.StringPath:
    attribute = getattr(arg, "path", "")
    return makepath(attribute)
    if attribute:
        return attribute
    raise NotImplementedError(f"Cannot find a path in `{arg!r}`")


path = makepath


@makepath.register(type(None))
def _mp(arg) -> strings.StringPath:
    """In the face of ambiguity, refuse the temptation to guess."""
    raise NotImplementedError(f"Zilch: {arg!r}")


@makepath.register(str)
def ____mp(arg) -> strings.StringPath:
    """Make a path from a string

    Expand out any variables, home squiggles, and normalise it
    See also http://stackoverflow.com/questions/26403972

    See also Lynton Kwesi Johnson:
        The Eagle and The Bear have people living in fear
        Of impending nuclear warfare
    """
    if not arg:
        return makepath(None)
    if os.path.isfile(arg):
        return FilePath(arg)
    if os.path.isdir(arg):
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
    except AttributeError:
        if arg not in imports() and arg not in sys.path:
            raise MissingImport(arg)
        python_ = makepath(sys.executable)
        assert str(python_.parent.name) == "bin"
        bin_ = python_.parent
        root_ = bin_.parent
        lib = root_ / "lib"
        assert lib.isdir()
        module = lib / f"{arg}.py"
        if module.isfile():
            return module
        package = lib / arg
        if package.isdir():
            return package
        raise ModuleNotFoundError(arg)


def _make_module_path(arg):
    """Make a path from a thing that has a module

    classes and functions have modules, they'll be needing this
    """
    try:
        return path(import_module(arg.__module__))
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
