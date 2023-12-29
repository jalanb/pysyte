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
from typing import Iterable
from typing import List

from pysyte.types.lists import flatten
from pysyte.types.trees import dirs
from pysyte.types.trees.makes import path
from pysyte.types.trees.paths import PathPath
from pysyte.types.trees.strings import NoPath
from pysyte.types.trees.strings import StringPath
from pysyte.types.trees.strings import StrPath


class PathError(Exception):
    """Something went wrong with a path"""

    prefix = "Path Error"


class MissingPath(PathError):
    def __init__(self, path_, desc=""):
        self.path = path_
        description = desc or "path"
        super().__init__(f"Missing {description}{path_}")


class MissingImport(MissingPath):
    def __init__(self, module):
        self.module = module
        try:
            path_ = module.__file__
        except AttributeError:
            path_ = module.__name__
        super().__init__(path_, desc="module")


class PathAssertions:
    """Assertions that can be made about paths"""

    def assertExists(self):
        if not self.exists():
            raise MissingPath(self)
        return self

    def assert_isdir(self):
        """Raise a PathError if this path is not a directory on disk"""
        if not self.isdir():
            raise PathError(f"{self} is not a directory")
        return self

    def assert_isfile(self):
        """Raise a PathError if this path is not a file on disk"""
        if not self.isfile():
            raise PathError(f"{self} is not a file")
        return self


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


class DotPath(StringPath):
    """This class add path-handling to a string"""

    def parent_directory(self):
        if self.isroot():
            return None
        return self.parent

    def parent_directories(self):
        if self.isroot():
            return []
        parent = self.parent
        return [parent] + parent.parent_directories()

    def directory(self):
        """Return a path to the path's directory"""
        return self.parent

    def dirnames(self):
        """Split the dirname into individual directory names

        An absolute path starts with an empty string, a relative path does not

        >>> DotPath('/path/to/module.py').dirnames() == ['/', 'path', 'to']
        True
        >>> DotPath('path/to/module.py').dirnames() == ['path', 'to']
        True
        """
        return [str(_) for _ in self.directory().split(os.path.sep)]

    def dirpaths(self):
        """Split the dirname into individual directory names

        An absolute path starts with an empty string, a relative path does not

        >>> p = DotPath('/path/to/x.py')
        >>> assert p.paths == p.dirpaths()
        """
        parts = self.split()
        result = [DotPath(parts[0] or "/")]
        for name in parts[1:]:
            result.append(result[-1] / name)
        return result

    def directories(self):
        """Split the dirname into individual directory names

        No empty parts are included

        >>> DotPath('path/to/module.py').directories() == ['path', 'to']
        True
        >>> DotPath('/path/to/module.py').directories() == ['/', 'path', 'to']
        True
        """
        return [d for d in self.dirnames() if d]

    parents = property(
        dirnames,
        None,
        None,
        """ This path's parent directories, as a list of strings.

        >>> DotPath('/path/to/module.py').parents == ['/', 'path', 'to']
        True
        """,
    )

    paths = property(
        dirpaths,
        None,
        None,
        """ This path's parent directories, as a sequence of paths.

        >>> paths = DotPath('/usr/bin/vim').paths
        >>> assert paths[-1].exists()  # vim might be a link
        >>> assert paths[-2] == paths[-1].parent
        >>> assert paths[-3] == paths[-2].parent
        >>> assert paths[-4] == paths[-3].parent
        >>> assert paths[-4] == paths[0]
        """,
    )

    def path_split(self, sep=None, maxsplit=-1):
        separator = sep or os.path.sep
        parts = super().split(separator, maxsplit)
        parts[0] = path(parts[0] if parts[0] else "/")
        return parts

    split = path_split

    def abspath(self):
        return path(os.path.abspath(str(self)))

    def slashpath(self):
        return self + "/" if self.isdir() else self

    def short_relative_path_to(self, destination):
        """The shorter of either the absolute path of the destination,
            or the relative path to it

        >>> print(
        ...     DotPath('/home/guido/bin').short_relative_path_to(
        ...         '/home/guido/build/python.tar'
        ...     )
        ... )
        ../build/python.tar
        >>> print(
        ...     DotPath('/home/guido/bin').short_relative_path_to(
        ...         '/mnt/guido/build/python.tar'
        ...     )
        ... )
        /mnt/guido/build/python.tar
        """
        relative = self.relpathto(destination)
        absolute = self.__class__(destination).abspath()
        if len(str(relative)) < len(str(absolute)):
            return relative
        return absolute

    def short_relative_path_to_here(self):
        """A short path relative to current working directory"""
        return self.short_relative_path_to(os.getcwd())

    def short_relative_path_from_here(self):
        """A short path relative to self to the current working directory"""
        return self.__class__(os.getcwd()).short_relative_path_to(self)

    def fnmatch_basename(self, glob):
        if glob.startswith(os.path.sep):
            glob = glob.lstrip(os.path.sep)
        string = self.basename()
        if fnmatch(string, glob):
            return self
        return None

    def fnmatch_directory(self, glob):
        if glob.startswith(os.path.sep) or glob.endswith(os.path.sep):
            glob = glob.strip(os.path.sep)
        if self.isdir():
            string = self.basename()
        else:
            string = self.parent.basename()
        if fnmatch(string, glob):
            return self
        return None

    def fnmatch_directories(self, glob):
        if glob.startswith(os.path.sep) or glob.endswith(os.path.sep):
            glob = glob.strip(os.path.sep)
        strings = reversed(self.directory().splitall()[1:])
        for string in strings:
            if fnmatch(string, glob):
                return self
        return None

    def fnmatch_part(self, glob):
        if self.fnmatch(glob):
            return self
        if self.fnmatch_basename(glob):
            return self
        if self.fnmatch_directory(glob):
            return self
        if self.fnmatch_directories(glob):
            return self
        return None

    def expand(self):
        """Expand the path completely

        This removes any "~" (for home dir) and any shell variables
            eliminates any symbolic links
            and converts from relative to absolute path
        """
        u = os.path.expanduser(str(self))
        v = os.path.expandvars(u)
        r = os.path.realpath(v)
        return path(r)

    def same_path(self, other):
        """Whether this path points to same place as the other"""
        return self.expand() == other.expand()

    def isroot(self):
        raise NotImplementedError("Only a directory path can be a root")

    def ishidden(self):
        """A 'hidden file' has a name starting with a '.'"""
        s = str(self.basename())
        return s and s[0] == "."

    def is_executable(self):
        """Whether the path is executable"""
        # pylint: disable=no-self-use
        return False

    def isexec(self):
        return self.is_executable()

    def has_executable(self):
        """Whether the path has any executable bits set"""
        executable_bits = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
        try:
            return bool(os.stat(self).st_mode & executable_bits)
        except OSError:
            return False


class FilePath(DotPath, PathAssertions):
    """A path to a known file"""

    def __truediv__(self, child):
        raise PathError("%r has no children" % self)

    def __iter__(self):
        for line in self.stripped_lines():
            yield line

    def contains(self, other: StrPath) -> bool:
        """Whether other is in this file's text"""
        return str(other) in self.text()

    def stripped_lines(self):
        """A list of all lines without trailing whitespace

        If lines can not be read (e.g. no such file) then an empty list
        """
        try:
            return [_.rstrip() for _ in self.lines(retain=False)]
        except (OSError, UnicodeDecodeError):
            return []

    def stripped_whole_lines(self):
        """A list of all lines without trailing whitespace or blank lines"""
        return [_ for _ in self.stripped_lines() if _]

    def non_comment_lines(self):
        """A list of all non-empty, non-comment lines"""
        return [_ for _ in self.stripped_whole_lines() if not _.startswith("#")]

    def isroot(self):
        """A file cannot be root of a filesystem"""
        return False

    def is_executable(self):
        """Whether the file has any executable bits set"""
        return self.has_executable()

    def has_line(self, string):
        for line in self:
            if string == line:
                return True
        return False

    def any_line_has(self, string):
        for line in self:
            if string in line:
                return True
        return False

    def as_python(self):
        """The path to the file with a .py extension

        >>> assert FilePath("/path/to/fred.txt").as_python() == "/path/to/fred.py"
        """
        return self.extend_by(".py")

    def make_read_only(self):
        """chmod the file permissions to -r--r--r--"""
        self.chmod(ChmodValues.readonly_file)

    def cd(self):  # pylint: disable=invalid-name
        """Change program's current directory to self"""
        return dirs.cd(self.parent)

    def dirname(self):
        return dirs.DirectPath(os.path.dirname(self))

    parent = property(dirname)

    def shebang(self):
        """The  #! entry from the first line of the file

        If no shebang is present, return an empty string
        """
        try:
            first_line = self.stripped_lines()[0]
            if first_line.startswith("#!"):
                return first_line[2:].strip()
        except IndexError:
            pass
        return ""

    def mv(self, destination):  # pylint: disable=invalid-name
        return self.move(destination)

    @property
    def language(self):
        """The language of this file"""
        try:
            return self._language
        except AttributeError:
            self._language = ext_language(self.ext)
        return self._language

    @language.setter
    def language(self, value):
        self._language = value


@dataclass
class FileTypeData:
    type_: type
    ext: str


class FileType(FileTypeData):
    def file(self, path_):
        return path_.add_missing_ext(self.ext)

    def typed(self, path_):
        file = self.file(path_)
        if file:
            return self.type_(file)
        return None


@dataclass
class FileTypesData:
    file_types: List[FileType]


class FileTypes(FileTypesData):
    def types(self):
        types_ = self.file_types
        return [_ if isinstance(_, FileType) else FileType(*_) for _ in types_]

    def files(self, path_):
        for file_type in self.types():
            file = file_type.file(path_)
            if file:
                yield file

    def typed(self, path_):
        for file_type in self.types():
            typed = file_type.typed(path_)
            if typed:
                yield typed


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


def imports():
    return {sys, os, re, stat}


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
    if isinstance(string_or_path, dirs.DirectPath):
        return string_or_path
    return path(string_or_path)


def string_to_paths(string: str) -> List[StringPath]:
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


def paths_in_directory(path_: StringPath) -> List[DotPath]:
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
    here = dirs.here()
    matches = []
    for glob_ in globs:
        if "/" in glob_:
            directory, base = os.path.split(glob_)
            dir_ = here / directory
        else:
            dir_ = here
            base = glob_
        match = [p for p in dir_.listdir() if p.fnmatch_basename(base)]
        matches.extend(match)
    result = [p for p in set(matches) if os.path.exists(p)]
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
