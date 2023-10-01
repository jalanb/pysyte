from __future__ import annotations

from typing import Any
from typing import Sequence
from typing import Tuple
from typing import Union
from path import Path as JasonOrrendorfPath
from deprecated import deprecated

StrPath = Union["StringPath", str]  # many args can be either string or path


class StringPath(JasonOrrendorfPath):
    """This class handles the path as if it were just a string

    Sub-classes know about paths qua paths

    >>> fred = StringPath("Hello World")
    >>> try:
    ...     assert fred.directory()
    ...     print("in a dir")
    ... except AttributeError:
    ...     print("Not in a dir")
    Not in a dir
    """

    # pylint: disable=abstract-method
    # pylint: disable=too-many-public-methods

    def __hash__(self):
        return hash(str(self))

    def __repr__(self) -> str:
        string = repr(f"{self}")
        return f"<{self.__class__.__name__} {string}>"

    @deprecated(version="0.7.5", reason="Embrace python3")
    def __div__(self, other) -> StringPath:
        """Handle the / operator

        >>> assert sys.version_info.major < 3

        >>> p = StringPath("/path/to")
        >>> assert p / "fred" == "/path/to/fred" == p.__div__("fred") == p // "fred"
        """
        return self.__truediv__(other)

    def __truediv__(self, substring: str) -> StringPath:
        """Handle the / operator

        Add substring to self

        >>> assert sys.version_info.major >= 3

        >>> p = StringPath("/path/to")
        >>> assert p / None is p
        >>> assert p / "fred" == "/path/to/fred" == p.__truediv__("fred") == p // "fred"
        """
        if not substring:
            return self
        full_string = os.path.join(str(self), substring)
        return makepath(full_string)

    def __floordiv__(self, substrings: Sequence[str]) -> StringPath:
        """Handle the // operator

        Add substrings to self like a path in local os

        >>> p = StringPath("/path/to")
        >>> assert p.__floordiv__("fred") == p // "fred"
        >>> assert p // ["module", "fred.py"] == "/path/to/module/fred.py"
        >>> assert p // None is p
        """
        if not substrings:
            return self
        string = str(self)
        strings = [string] + list(substrings)
        return makepath(os.path.join(*strings))

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __lt__(self, other) -> bool:
        return str(self) < str(other)

    # functools.total_ordering does not work properly cos we inherit from str
    # Hence: we do need to define next 3
    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __contains__(self, other) -> bool:
        """The other is in self if self.contains(other)

        this method should be specialised in sub-classes
        """
        return self.contains(other)

    def contains(self, other: StrPath) -> bool:
        """If other is also a path then this path should start with other

        E.g. /path/to/file is "in" /path

        Otherwise, just use the sub-string sense of "in"
        """
        if isinstance(other, StringPath):
            return str(other).startswith(str(self))
        return str(other) in str(self)

    def basename(self) -> str:
        return str(super().basename())

    @property
    def basename_(self) -> str:
        return self.basename()

    @property
    def name(self) -> str:
        return str(super().name)

    @property
    def stem(self) -> StringPath:
        stem, *_ = self.splitexts()
        return stem

    @property
    def stem_name(self) -> str:
        return self.stem.name

    def splitexts(self) -> Tuple[StringPath, str]:
        """Split all extensions from the path

        >>> p = FilePath('here/fred.tar.gz')
        >>> assert p.splitexts() == ('here/fred', '.tar.gz')
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

        >>> source = makepath(__file__)
        >>> new = source.add_ext('txt', '.new')
        >>> assert new.name.endswith('.py.txt.new')
        """
        exts = [(a[1:] if a[0] == "." else a) for a in args]
        string = ".".join([self] + list(exts))
        return makepath(string)

    def add_missing_ext(self, ext: str) -> StringPath:
        """Add that extension, if it is missing

        >>> fred = makepath("fred")
        >>> assert fred.add_missing_ext("") == fred
        >>> fred_py = makepath("fred.py")
        >>> assert fred.add_missing_ext(".py") == fred_py
        >>> assert fred_py.add_missing_ext(".txt") == "fred.py.txt"
        """
        dot_ext = f'.{ext.lstrip(".")}'
        copy = self[:]
        _, self_ext = os.path.splitext(copy)
        return makepath(self) if self_ext == dot_ext else self.add_ext(dot_ext)

    def extend_by(self, ext: str) -> StringPath:
        """The path to the file changed to use the given ext

        >>> fred = "/path/to/fred.fred"
        >>> assert makepath("/path/to/fred").extend_by("fred")       == fred
        >>> assert makepath("/path/to/fred.txt").extend_by(".fred")  == fred
        >>> assert makepath("/path/to/fred.txt").extend_by("..fred") == fred
        """
        copy = self[:]
        filename, _ = os.path.splitext(copy)
        ext_ = ext.lstrip(".")
        return makepath(f"{filename}.{ext_}")

    def has_vcs_dir(self):
        for vcs_dir in (".git", ".svn", ".hg"):
            if self.fnmatch_part(vcs_dir):
                return True
        return False


class NoPath(StringPath):
    """An empty path

    >>> np = NoPath()
    >>> assert not np
    >>> assert np == NoPath(None) == NoPath(0) == NoPath(False)
    """

    def __init__(self, string: Any = ""):
        self.string = string or ""
        self.fake_path = FilePath(self.string) or DirectPath(self.string)

    def __str__(self):
        return self.string

    def __repr__(self):
        string = self.string
        if self.fake_path:
            string = str(self.fake_path)
        return f'<{self.__class__.__name__} "{string}">'

    def __bool__(self):
        return False

    def __eq__(self, other):
        if self.string:
            return str(self) == str(other)
        return not other

    def __lt__(self, other):
        if self.string and other:
            return str(self) < str(other)
        return bool(other)

    def contains(self, other: StrPath) -> bool:
        """As this is not a real path, just use the substring sense"""
        return str(other) in str(self)

    def __truediv__(self, child):
        result = os.path.join(self.string, child) if child else self.string
        return makepath(result)

    @property
    def parent(self):
        if "/" not in self.string:
            return None
        parent_string = "/".join(self.string.split("/")[:-1])
        return makepath(parent_string)

    def exists(self):
        return False

    isdir = isfile = isexec = isroot = exists

    def __getattr__(self, name):
        return getattr(self.fake_path, name, None)

    def makedirs(self):
        os.makedirs(str(self))
