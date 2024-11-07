import os
from typing import Tuple

from pysyte.types.trees import dirs
from pysyte.types.trees import errors
from pysyte.types.trees import paths
from pysyte.types.trees import chmod
from pysyte.types.trees import strings
from pysyte.types.trees.asserts import PathAssertions
from pysyte.types.trees.makes import makepath
from pysyte.types.trees.strings import StringPath


class FilePath(paths.Path, PathAssertions):
    """A path to a known file"""

    def __truediv__(self, child):
        raise errors.PathError("%r has no children" % self)

    def __iter__(self):
        for line in self.stripped_lines():
            yield line

    def __add__(self, other: strings.StrPath) -> strings.StringPath:
        return self.addext(other)

    def contains(self, other: strings.StrPath) -> bool:
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
        self.chmod(chmod.readonly_file)

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

    def write(self, string: str):
        self.file.write_text(string)


def ext_language(ext, exts=None, simple=True):
    """Language of the extension in those extensions

    If exts is supplied, then restrict recognition to those exts only
    If exts is not supplied, then use all known extensions

    >>> ext_language(".py") == "python"
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


class StringFile(FilePath):
    """A path to an unknown file with a string"""

    def __init__(self, *args: str):
        self.file = files.FilePath()
        self.file.write(*args)
        super().__init__(*args)


class ExtendedPath(FilePath):
    """A path with extensions"""

    def dezip(self) -> Tuple[StringPath, str]:
        """Split all zipping extensions from the path

        >>> p = FilePath("here/fred.tar.gz")
        >>> assert p.dezip() == ("here/fred", ".tar.gz")
        """
        copy = self[:]
        filename, ext = os.path.splitext(copy)
        zippers = (
            ".gz",
            ".bz",
            ".zip",
            ".bzip",
        )
        for zipper in zippers:
            if ext == zipper:
                filename, ext_ = os.path.splitext(filename)
                ext = f"{ext_}{zipper}"
        return self.__class__(filename), ext

    def add_ext(self, *args) -> StringPath:
        """Join all args as extensions

        Strip any leading `.` from args

        >>> file = makepath(__file__)
        >>> new = file.add_ext("txt", "new")
        >>> newer = file.add_ext(".txt", ".new")
        >>> newest = file.add_ext([".txt", "new"])

        >>> assert new.name.endswith(".py.txt.new")
        >>> assert newer == new == newest
        """
        exts = [(a[1:] if a[0] == "." else a) for a in args]
        string = ".".join([self] + list(exts))
        return makepath(string)

    def __add__(self, ext: str) -> StringPath:
        return self.add_ext(ext)

    def add_missing_ext(self, ext: str) -> StringPath:
        """Add that extension, if it is missing

        >>> fred = makepath("fred")
        >>> assert fred.add_missing_ext("") == fred
        >>> fred_py = makepath("fred.py")
        >>> fred_py_py = fred.add_missing_ext(".py")
        >>> assert fred_py_py == fred_py
        >>> assert fred_py_py.add_missing_ext(".txt") == "fred.py.txt"
        """
        dot_ext = f'.{ext.lstrip(".")}'
        copy = self[:]
        _, self_ext = os.path.splitext(copy)
        return makepath(self) if self_ext == dot_ext else self.add_ext(dot_ext)

    def extend_by(self, ext: str) -> StringPath:
        """The path to the file changed to use the given ext

        >>> fred = "/path/to/fred.fred"
        >>> assert makepath("/path/to/fred").extend_by("fred") == fred
        >>> assert makepath("/path/to/fred.txt").extend_by(".fred") == fred
        >>> assert makepath("/path/to/fred.txt").extend_by("..fred") == fred
        """
        copy = self[:]
        filename, _ = os.path.splitext(copy)
        ext_ = ext.lstrip(".")
        return makepath(f"{filename}.{ext_}")
