"""A collection of extended path classes and methods

The classes all inherit from the original path.path
"""
from __future__ import annotations

import os
import re
import stat
import sys
from dataclasses import dataclass
from fnmatch import fnmatch
from functools import singledispatch
from importlib import import_module
from typing import Iterable
from typing import List

from deprecated import deprecated

from pysyte.types.lists import flatten
from pysyte.types.trees.paths import PathPath
from pysyte.types.trees.files import FilePath
from pysyte.types.trees.dirs import DirectPath
from pysyte.types.trees.strings import NoPath
from pysyte.types.trees.errors import MissingImport
from pysyte.types.trees.errors import PathError


def ext_language(ext, exts=None, simple=True):
    """Language of the extension in those extensions

    If exts is supplied, then restrict recognition to those exts only
    If exts is not supplied, then use all known extensions

    >>> ext_language('.py') == 'python'
    True
    """
    languages = {
        ".py": "python",
        ".py2": "python" if simple else "python2",
        ".py3": "python" if simple else "python3",
        ".sh": "bash",
        ".bash": "bash",
        ".pl": "perl",
        ".txt": "english",
    }
    ext_languages = {_: languages[_] for _ in exts} if exts else languages
    return ext_languages.get(ext)


def ignore_fnmatches(ignores):
    def ignored(a_path):
        if not ignores:
            return False
        for ignore in ignores:
            if a_path.fnmatch_part(ignore):
                return True
        return False

    return ignored


class ChmodValues:
    # pylint: disable=too-few-public-methods
    readonly_file = 0o444
    readonly_directory = 0o555


def _make_module_path(arg):
    """Make a path from a thing that has a module

    classes and functions have modules, they'll be needing this
    """
    try:
        return makepath(import_module(arg.__module__))
    except (AttributeError, ModuleNotFoundError):
        return None


@singledispatch
def makepath(arg) -> StringPath:
    attribute = getattr(arg, "path", "")
    return makepath(attribute)
    if attribute:
        return attribute
    raise NotImplementedError(f"Cannot find a path in `{arg!r}`")


path = makepath


@makepath.register(type(None))
def _mp(arg) -> StringPath:
    """In the face of ambiguity, refuse the temptation to guess."""
    raise NotImplementedError(f"Zilch: {arg!r}")


@makepath.register(PathPath)
def __mp(arg) -> StringPath:
    return arg


@makepath.register(str)
def ____mp(arg) -> StringPath:
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
        return NoPath(arg)
    if os.path.exists(u):
        return makepath(u)
    return NoPath(arg)


def imports():
    return {sys, os, re, stat}


@makepath.register(type(os))
def _____mp(arg) -> StringPath:
    """Make a path from a module"""
    if arg.__name__ == "builtins":
        return NoPath("builtins")
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


@makepath.register(type(makepath))
def ______mp(arg) -> StringPath:
    """Make a path from a function's module"""
    terminal_regexp = re.compile("<(stdin|.*python-input.*)>")
    method = getattr(arg, "__wrapped__", arg)
    filename = method.__code__.co_filename
    if terminal_regexp.match(filename):
        return NoPath(filename)
    return _make_module_path(method)


@makepath.register(type(PathPath))
def _______mp(arg) -> StringPath:
    """Make a path from a class's module"""
    return _make_module_path(arg)


@singledispatch
def makepaths(arg) -> Paths:
    """In the face of ambiguity, refuse the temptation to guess."""
    raise NotImplementedError(f"Do not know the type of arg: {arg!r}")


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
def ____mps(arg) -> Paths:
    return Paths([arg])


@deprecated(reason="use pathstr()", version="0.7.57")
def makestr(string: str) -> StringPath:
    return pathstr(string)


def pathstr(string: str) -> StringPath:
    """Make a path from a string"""
    if os.path.isfile(string) or os.path.isdir(string):
        return makepath(string)
    return NoPath(string)


def cd(path_to: StringPath) -> bool:
    """cd to the given path

    If the path is a file, then cd to its parent directory

    Remember current directory before the cd
        so that we can cd back there with cd('-')
    """
    if path_to == "-":
        previous = getattr(cd, "previous", "")
        if not previous:
            raise PathError("No previous directory to return to")
        return cd(makepath(previous))
    if not hasattr(path_to, "cd"):
        path_to = makepath(path_to)
    try:
        previous = os.getcwd()
    except OSError as e:
        if "No such file or directory" not in str(e):
            raise
        previous = ""
    if path_to.isdir():
        cd_path = path_to
    elif path_to.isfile():
        cd_path = path_to.parent
    elif not path_to.exists():
        return False
    else:
        raise PathError(f"Cannot cd to {path_to}")
    cd.previous = previous  # type: ignore
    os.chdir(cd_path)
    return True


try:
    setattr(cd, "previous", os.getcwd())
except (OSError, AttributeError):
    setattr(cd, "previous", "")


def as_path(string_or_path):
    """Return the argument as a DirectPath

    If it is already one, return it unchanged
    If not, return the makepath()
    """
    if isinstance(string_or_path, DirectPath):
        return string_or_path
    return makepath(string_or_path)


def string_to_paths(string) -> List[StringPath]:
    for c in ":, ;":
        if c in string:
            return strings_to_paths(string.split(c))
    return [makepath(string)]


def strings_to_paths(strings) -> List[StringPath]:
    return [makepath(s) for s in strings]


def choose_paths(*strings, chooser) -> List[StringPath]:
    return [_ for _ in strings_to_paths(strings) if chooser(_)]


def paths(*strings: Iterable) -> List[StringPath]:
    return choose_paths(*strings, chooser=lambda p: p.exists())


def directories(*strings: Iterable) -> List[StringPath]:
    return choose_paths(*strings, chooser=lambda p: p.isdir())


def files(*strings: Iterable) -> List[StringPath]:
    return choose_paths(*strings, chooser=lambda p: p.isfile())


def root():
    return makepath("/")


def tmp():
    return makepath("/tmp")


def home():
    _home = makepath(os.path.expanduser("~"))
    assert _home
    _ = _home.expand()
    return _home


def pwd():
    return makepath(os.getcwd())


def first_dir(path_string):
    """Get the first directory in that path

    >>> first_dir('usr/local/bin') == 'usr'
    True
    """
    parts = path_string.split(os.path.sep)
    return parts[0]


def first_dirs(path_strings):
    """Get the roots of those paths

    >>> first_dirs(['usr/bin', 'bin']) == ['usr', 'bin']
    True
    """
    return [first_dir(_) for _ in path_strings]


def unique_first_dirs(path_strings):
    """Get the unique roots of those paths

    >>> unique_first_dirs(['usr/local/bin', 'bin']) == set(['usr', 'bin'])
    True
    """
    return set(first_dirs(path_strings))


def paths_in_directory(path_: StringPath) -> List[PathPath]:
    """Get all items in the given directory

    Swallow errors to give an empty list
    """
    try:
        return [_ for _ in path_.listdir() if _]
    except OSError:
        return []


def list_matcher(pattern, path_to_directory, wanted):
    """Gives a method to check if an item matches the pattern, and is wanted

    If path_to_directory is given then items are checked there
    By default, every item is wanted
    """
    return lambda x: fnmatch(x, pattern) and wanted(os.path.join(path_to_directory, x))


def list_items(path_to_directory, glob, wanted=lambda x: True) -> List[StringPath]:
    """All items in the given path which match the given glob and are wanted

    By default, every path is wanted
    """
    path_to_directory_ = makepath(path_to_directory)
    if not path_to_directory_:
        return []
    result = []
    for path_to_item in path_to_directory_.listdir():
        if not fnmatch(path_to_item.name, glob):
            continue
        if wanted(path_to_item):
            result.append(path_to_item)
    return result


def list_sub_directories(path_to_directory, glob):
    """All sub-directories of the given directory matching the given glob"""
    return list_items(path_to_directory, glob, os.path.isdir)


def set_items(path_to_directory, glob, wanted):
    return set(list_items(path_to_directory, glob, wanted))


def set_files(path_to_directory, glob):
    """A list of all files in the given directory matching the given glob"""
    return set_items(path_to_directory, glob, os.path.isfile)


def contains_glob(path_to_directory, glob, wanted=lambda x: True):
    """Whether the given path contains an item matching the given glob"""
    return any(list_items(path_to_directory, glob, wanted))


def contains_directory(path_to_directory, glob):
    """Whether the given path contains a directory matching the given glob"""
    return contains_glob(path_to_directory, glob, os.path.isdir)


def contains_file(path_to_directory, glob):
    """Whether the given directory contains a file matching the given glob"""
    return contains_glob(path_to_directory, glob, os.path.isfile)


def environ_paths(key, default=None):
    default_ = default or ""
    return [makepath(_) for _ in os.environ.get(key, default_).split(":")]


def environ_path(key, default=None):
    default_ = default or ""
    return makepath(os.environ.get(key, default_))


def default_environ_path(key, default):
    return makepath(os.environ.get(key, default))


def add_star(string):
    """Add '*' to string

    >>> assert add_star('fred') == 'fred*'
    """
    return f"{string}*"


def add_stars(strings):
    """Add '.*' to each string

    >>> assert add_stars(['fred', 'Fred.']) == ['fred*', 'Fred.*']
    """
    paths_ = [strings] if isinstance(strings, str) else strings
    return [add_star(p) for p in paths_]


def tab_complete(strings, globber=add_stars, select=os.path.exists):
    """Finish path names "left short" by bash's tab-completion

    strings is a string or strings
        if any string exists as a path return those as paths

    globber is a method which should return a list of globs
        default: add_stars(['fred.']) == ['fred.*']
            or, e.g: add_python(['fred', 'fred.']) == ['fred.py*']
        if any expanded paths exist return those

    select is a method to choose wanted paths
        Defaults to selecting existing paths
    """
    strings_ = [strings] if isinstance(strings, str) else strings
    globs = flatten([globber(s) for s in strings_])
    here_ = pwd()
    matches = []
    for glob_ in globs:
        if "/" in glob_:
            directory, base = os.path.split(glob_)
            dir_ = here_ / directory
        else:
            dir_ = here_
            base = glob_
        match = [p for p in dir_.listdir() if p.fnmatch_basename(base)]
        matches.extend(match)
    result = [p for p in set(matches) if select(p)]
    return result if result[1:] else strings


def pyc_to_py(path_to_file):
    """Change some file extensions to those which are more likely to be text

    >>> pyc_to_py('vim.pyc') == 'vim.py'
    True
    """
    stem, ext = os.path.splitext(path_to_file)
    if ext == ".pyc":
        return f"{stem}.py"
    return path_to_file
