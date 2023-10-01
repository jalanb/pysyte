from dataclasses import dataclass
from functools import singledispatch

from pysyte.types.trees import makes
from pysyte.types.trees import strings


class PathPath(strings.StringPath):
    """This class adds path-handling to a string"""

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

        >>> PathPath('/path/to/module.py').dirnames() == ['/', 'path', 'to']
        True
        >>> PathPath('path/to/module.py').dirnames() == ['path', 'to']
        True
        """
        return [str(_) for _ in self.directory().split(os.path.sep)]

    def dirpaths(self):
        """Split the dirname into individual directory names

        An absolute path starts with an empty string, a relative path does not

        >>> p = PathPath('/path/to/x.py')
        >>> assert p.paths == p.dirpaths()
        """
        parts = self.split()
        result = [PathPath(parts[0] or "/")]
        for name in parts[1:]:
            result.append(result[-1] / name)
        return result

    def directories(self):
        """Split the dirname into individual directory names

        No empty parts are included

        >>> PathPath('path/to/module.py').directories() == ['path', 'to']
        True
        >>> PathPath('/path/to/module.py').directories() == ['/', 'path', 'to']
        True
        """
        return [d for d in self.dirnames() if d]

    parents = property(
        dirnames,
        None,
        None,
        """ This path's parent directories, as a list of strings.

        >>> PathPath('/path/to/module.py').parents == ['/', 'path', 'to']
        True
        """,
    )

    paths = property(
        dirpaths,
        None,
        None,
        """ This path's parent directories, as a sequence of paths.

        >>> paths = PathPath('/usr/bin/vim').paths
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
        parts[0] = makes.path(parts[0] if parts[0] else "/")
        return parts

    split = path_split

    def abspath(self):
        return makes.path(os.path.abspath(str(self)))

    def slashpath(self):
        return self + "/" if self.isdir() else self

    def short_relative_path_to(self, destination):
        """The shorter of either the absolute path of the destination,
            or the relative path to it

        >>> print(PathPath('/home/guido/bin').short_relative_path_to(
        ...     '/home/guido/build/python.tar'))
        ../build/python.tar
        >>> print(PathPath('/home/guido/bin').short_relative_path_to(
        ...     '/mnt/guido/build/python.tar'))
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
        strings_ = reversed(self.directory().splitall()[1:])
        for string in strings_:
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
        return makes.path(r)

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


@dataclass
class Paths:
    """A collection of paths"""

    paths: list[strings.StrPath]

    def __iter__(self):
        yield self.paths


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




@makepaths.register(strings.StringPath)
def make_string_paths(arg) -> Paths:
    return Paths([arg])


@makes.makepath.register(PathPath)
def make_path_path(arg) -> strings.StringPath:
    return arg
