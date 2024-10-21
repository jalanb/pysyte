import os

from pysyte.types.trees import errors
from pysyte.types.trees import files
from pysyte.types.trees import makes
from pysyte.types.trees import paths
from pysyte.types.trees import strings
from pysyte.types.trees.asserts import PathAssertions


class DirectPath(paths.PathPath, PathAssertions):
    """A path which knows it might be a directory

    And that files are in directories
    """

    __file_class__ = files.FilePath

    def __iter__(self):
        for a_path in self.listdir():
            yield a_path

    def __add__(self, other: strings.StringPath) -> strings.StringPath:
        return paths.makepath(f"{self}/{other}")

    def contains(self, other: strings.StrPath) -> bool:
        """If other is a path then use that sense of "in"

        So /path/to/here is "in" /path

        Otherwise see if other is listed "in" this directory
        """
        if isinstance(other, paths.PathPath):
            return self in other.parent_directories()
        return str(other) in [_.name for _ in self.listdir()] + [".", ".."]

    def directory(self):
        """Return a path to a directory.

        Either the path itself (if it is a directory), or its parent)
        """
        if self.isdir():
            return self
        return self.parent

    def remove_dir(self):
        """Try to remove the path

        If it is a directory, try recursive removal of contents too
        """
        if self.islink():
            self.unlink()
        elif self.isdir():
            self.empty_directory()
            if self.isdir():
                self.rmdir()
        else:
            return False
        return True

    def empty_directory(self):
        """Remove all contents of a directory

        Including any sub-directories and their contents"""
        for child in self.walkfiles():
            child.remove()
        for child in reversed([self.walkdirs()]):
            if child == self or not child.isdir():
                continue
            child.rmdir()

    def cd(self):  # pylint: disable=invalid-name
        """Change program's current directory to self"""
        return cd(strings.StringPath(self))

    def list_dirs(self, pattern=None):
        return self.list_dirs_files(pattern)[0]

    def list_files(self, pattern=None):
        return self.list_dirs_files(pattern)[1]

    def list_dirsfiles(self, pattern=None):
        dirs, others = self.list_dirs_files(pattern)
        return dirs + others

    def list_dirs_files(self, pattern=None):
        items = self.listdir(pattern)
        dirs = [_ for _ in items if _.isdir()]
        others = [_ for _ in items if not _.isdir()]
        return dirs, others

    def make_read_only(self):
        """chmod the directory permissions to -r-xr-xr-x"""
        self.chmod(paths.ChmodValues.readonly_directory)

    def touch_file(self, filename):
        """Touch a file in the directory"""
        path_to_file = self.__file_class__(os.path.join(self, filename))
        path_to_file.touch()
        return path_to_file

    def existing_sub_paths(self, sub_paths):
        """Those in the given list of sub_paths which do exist"""
        paths_to_subs = [self / _ for _ in sub_paths]
        return [_ for _ in paths_to_subs if _.exists()]

    # pylint: disable=arguments-differ
    def walkdirs(self, pattern=None, errors="strict", ignores=None):
        ignored = ignore_fnmatches(ignores)
        for path_to_dir in super(DirectPath, self).walkdirs(pattern, errors):
            if not ignored(path_to_dir.relpath(self)):
                yield path_to_dir

    # pylint: disable=arguments-differ
    def walkfiles(self, pattern=None, errors="strict", ignores=None):
        ignored = ignore_fnmatches(ignores)
        for path_to_file in super(DirectPath, self).walkfiles(pattern, errors):
            if not ignored(path_to_file.relpath(self)):
                yield path_to_file

    def listfiles(self, pattern=None, ignores=None):
        ignored = ignore_fnmatches(ignores)
        return [_ for _ in self.listdir(pattern) if _.isfile() and not ignored(_)]

    def isroot(self):
        return str(self) == "/"


def ignore_fnmatches(ignores):
    def ignored(a_path):
        if not ignores:
            return False
        for ignore in ignores:
            if a_path.fnmatch_part(ignore):
                return True
        return False

    return ignored


def cd(path_to: strings.StringPath) -> bool:
    """cd to the given path

    If the path is a file, then cd to its parent directory

    Remember current directory before the cd
        so that we can cd back there with cd('-')
    """
    if path_to == "-":
        previous = getattr(cd, "previous", "")
        if not previous:
            raise errors.PathError("No previous directory to return to")
        return cd(makes.path(previous))
    if not hasattr(path_to, "cd"):
        path_to = makes.path(path_to)
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
        raise errors.PathError(f"Cannot cd to {path_to}")
    cd.previous = previous  # type: ignore
    os.chdir(cd_path)
    return True


try:
    setattr(cd, "previous", os.getcwd())  # noqa
except (OSError, AttributeError):
    setattr(cd, "previous", "")  # noqa
