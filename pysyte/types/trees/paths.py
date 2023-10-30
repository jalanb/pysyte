from dataclasses import dataclass
from functools import singledispatch

from pysyte.types.trees import makes
from pysyte.types.trees import strings


class ChmodValues:
    # pylint: disable=too-few-public-methods
    readonly_file = 0o444
    readonly_directory = 0o555


class RealPath(strings.StringPath):
    """This is a path to a real place, e.g. on a filesystem

    It might be a file, link, dir, ...

    We assume it has a familiar root
    """
    @property
    def root(self) -> strings.StringPath:
        """
        >>> assert RealPath('/usr/local').root == '/'
        """
        return strings.StringPath("/")

    def isroot(self) -> bool:
        """
        >>> assert RealPath('/').isroot()
        """
        return self == self.parent

    def isabs(self) -> bool:
        """
        >>> assert RealPath("/one/two").isabs()
        >>> assert not RealPath("one/two").isabs()
        """
        return self.startswith(self.root)


class Path(RealPath):
    """This class adds path-handling to a string"""

    @property
    def name(self) -> str:
        return str(super().basename())

    @property
    def stem(self) -> StringPath:
        stem, *_ = self.splitexts()
        return stem

    @property
    def stem_name(self) -> str:

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

        >>> Path('/path/to/module.py').dirnames() == ['/', 'path', 'to']
        True
        >>> Path('path/to/module.py').dirnames() == ['path', 'to']
        True
        """
        return [str(_) for _ in self.directory().split(os.path.sep)]

    def dirpaths(self):
        """Split the dirname into individual directory names

        An absolute path starts with an empty string, a relative path does not

        >>> p = Path('/path/to/x.py')
        >>> assert p.paths == p.dirpaths()
        """
        parts = self.split()
        result = [Path(parts[0] or "/")]
        for name in parts[1:]:
            result.append(result[-1] / name)
        return result

    def directories(self):
        """Split the dirname into individual directory names

        No empty parts are included

        >>> Path('path/to/module.py').directories() == ['path', 'to']
        True
        >>> Path('/path/to/module.py').directories() == ['/', 'path', 'to']
        True
        """
        return [d for d in self.dirnames() if d]

    parents = property(
        dirnames,
        None,
        None,
        """ This path's parent directories, as a list of strings.

        >>> Path('/path/to/module.py').parents == ['/', 'path', 'to']
        True
        """,
    )

    paths = property(
        dirpaths,
        None,
        None,
        """ This path's parent directories, as a sequence of paths.

        >>> paths = Path('/usr/bin/vim').paths
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

        >>> print(Path('/home/guido/bin').short_relative_path_to(
        ...     '/home/guido/build/python.tar'))
        ../build/python.tar
        >>> print(Path('/home/guido/bin').short_relative_path_to(
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


@makes.makepath.register(Path)
def make_path_path(arg) -> strings.StringPath:
    return arg
