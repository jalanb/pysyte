"""A collection of extended path classes and methods

The classes all inherit from the original path.path
"""
from __future__ import annotations

import os
import re
import stat
import sys
from fnmatch import fnmatch
from typing import Iterable
from typing import List

from deprecated import deprecated

from pysyte.types.lists import flatten
from pysyte.types.trees.dirs import DirectPath
from pysyte.types.trees.makes import path
from pysyte.types.trees.paths import PathPath
from pysyte.types.trees.strings import NoPath
from pysyte.types.trees.strings import StringPath


def imports():
    return {sys, os, re, stat}


@deprecated(reason="use pathstr()", version="0.7.57")
def makestr(string: str) -> StringPath:
    return pathstr(string)


def pathstr(string: str) -> StringPath:
    """Make a path from a string"""
    if os.path.isfile(string) or os.path.isdir(string):
        return path(string)
    return NoPath(string)


def as_path(string_or_path):
    """Return the argument as a DirectPath

    If it is already one, return it unchanged
    If not, return the path()
    """
    if isinstance(string_or_path, DirectPath):
        return string_or_path
    return path(string_or_path)


def string_to_paths(string) -> List[StringPath]:
    for c in ":, ;":
        if c in string:
            return strings_to_paths(string.split(c))
    return [path(string)]


def strings_to_paths(strings) -> List[StringPath]:
    return [path(s) for s in strings]


def choose_paths(*strings, chooser) -> List[StringPath]:
    return [_ for _ in strings_to_paths(strings) if chooser(_)]


def paths(*strings: Iterable) -> List[StringPath]:
    return choose_paths(*strings, chooser=lambda p: p.exists())


def directories(*strings: Iterable) -> List[StringPath]:
    return choose_paths(*strings, chooser=lambda p: p.isdir())


def files(*strings: Iterable) -> List[StringPath]:
    return choose_paths(*strings, chooser=lambda p: p.isfile())


def root():
    return path("/")


def tmp():
    return path("/tmp")


def home():
    _home = path(os.path.expanduser("~"))
    assert _home
    _ = _home.expand()
    return _home


def pwd():
    return path(os.getcwd())


def first_dir(path_string):
    """Get the first directory in that path

    >>> first_dir("usr/local/bin") == "usr"
    True
    """
    parts = path_string.split(os.path.sep)
    return parts[0]


def first_dirs(path_strings):
    """Get the roots of those paths

    >>> first_dirs(["usr/bin", "bin"]) == ["usr", "bin"]
    True
    """
    return [first_dir(_) for _ in path_strings]


def unique_first_dirs(path_strings):
    """Get the unique roots of those paths

    >>> unique_first_dirs(["usr/local/bin", "bin"]) == set(["usr", "bin"])
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
    path_to_directory_ = path(path_to_directory)
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
    return [path(_) for _ in os.environ.get(key, default_).split(":")]


def environ_path(key, default=None):
    default_ = default or ""
    return path(os.environ.get(key, default_))


def default_environ_path(key, default):
    return path(os.environ.get(key, default))


def add_star(string):
    """Add '*' to string

    >>> assert add_star("fred") == "fred*"
    """
    return f"{string}*"


def add_stars(strings):
    """Add '.*' to each string

    >>> assert add_stars(["fred", "Fred."]) == ["fred*", "Fred.*"]
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

    >>> pyc_to_py("vim.pyc") == "vim.py"
    True
    """
    stem, ext = os.path.splitext(path_to_file)
    if ext == ".pyc":
        return f"{stem}.py"
    return path_to_file
