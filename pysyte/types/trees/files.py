import os

from pysyte.types.trees import dirs
from pysyte.types.trees import errors
from pysyte.types.trees import paths
from pysyte.types.trees import strings
from pysyte.types.trees.asserts import PathAssertions


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
        self.chmod(paths.ChmodValues.readonly_file)

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

    def write(self, string:str):
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

    def __init__(self, string: str):
        self.file = files.FilePath()
        self.file.write(string)
        super().__init__(*args)
