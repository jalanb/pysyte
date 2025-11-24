"""A collection of extended path classes and methods

The classes all inherit from the original path.path
"""

from __future__ import annotations

from fnmatch import fnmatch
import os

from pysyte.types.lists import flatten
from pysyte.types.trees.dirs import pwd
from pysyte.types.trees.makes import path
from pysyte.types.trees.strings import StringPath


def list_items(path_to_directory, glob, wanted=lambda x: True) -> list[StringPath]:
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


def contains_glob(path_to_directory, glob, wanted=lambda x: True):
    """Whether the given path contains an item matching the given glob"""
    return any(list_items(path_to_directory, glob, wanted))


def contains_directory(path_to_directory, glob):
    """Whether the given path contains a directory matching the given glob"""
    return contains_glob(path_to_directory, glob, os.path.isdir)


def contains_file(path_to_directory, glob):
    """Whether the given directory contains a file matching the given glob"""
    return contains_glob(path_to_directory, glob, os.path.isfile)


def environ_paths(key, default=""):
    return [path(_) for _ in os.environ.get(key, default).split(":")]


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


def tab_complete(strings, globber=add_stars):
    """Finish path names "left short" by bash's tab-completion

    strings is a string or strings
        if any string exists as a path return those as paths

    globber is a method which should return a list of globs
        default: add_stars(['fred.']) == ['fred.*']
            or, e.g: add_python(['fred', 'fred.']) == ['fred.py*']
        if any expanded paths exist return those
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
    result = [p for p in set(matches) if os.path.exists(p)]
    return result if result[1:] else strings


def pyc_to_py(path_to_file):
    """Change some file extensions to those which are more likely to be text

    >>> assert pyc_to_py("vim.pyc") == "vim.py"
    """
    stem, ext = os.path.splitext(path_to_file)
    if ext == ".pyc":
        return f"{stem}.py"
    return path_to_file
