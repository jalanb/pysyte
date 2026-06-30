from __future__ import annotations

from dataclasses import dataclass
import os
from typing import (
    Any,
    Callable,
    Iterable,
    Sequence,
    TypeAlias,
)

from deprecated import deprecated
from path import Path as JasonOrrendorfPath

StrPath: TypeAlias = "StringPath | str"  # many args can be either string or path


@dataclass
class StringPath(JasonOrrendorfPath):
    """This class handles the path as if it were just a string

    Sub-classes know about paths qua paths

    >>> fred = StringPath("Hello World")
    >>> try:
    ...     assert fred.directory()
    ...     print("in a dir")
    ... except AttributeError:
    ...     print("Not in a dir")
    ...
    Not in a dir
    """

    from pysyte.types.trees.dirs import DirectPath

    sep: str = "/"

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
        from pysyte.types.trees.makes import makepath

        return makepath(full_string)

    def __floordiv__(self, substrings: Sequence[str]) -> StringPath:
        """Handle the // operator

        Add substrings to self like a path in local os

        >>> p = StringPath("/path/to")
        >>> assert p.__floordiv__("fred") == p // "fred"
        >>> assert p // ["module", "fred.py"] == "/path/to/module/fred.py"
        >>> assert p // None is p
        """
        from pysyte.types.trees.makes import makepath

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

    def __add__(self, other: StringPath) -> StringPath:
        """Concatenate the other

        >>> assert StringPath("/usr/loc") + "al" == "/usr/local"
        """
        return self.__class__(f"{self}{other}")

    def __sub__(self, other: int) -> DirectPath:
        """Subtract dirs from end of path

        >>> assert StringPath("/usr/local/bin/conf.d/fred.toml") - 3 == "/usr/local"
        """
        parts = self.split(str(self))
        i = int(other)
        fewer = parts[:-i]
        return self.join(fewer)

    def split(self, string: str = "", maxsplit: int = -1) -> list[str]:
        """Split a path into root and strings

        >>> StringPath("/1/2/3/4/5").split(2)
        StringPath('/'), 'one', 'two'
        """
        data = string if string else str(self)
        return data.split(self.sep, maxsplit)

    def rsplit(self, string: str = "", maxsplit: int = -1) -> list[str]:
        """Split a path into root and strings, from the right

        >>> StringPath("/1/2/3/4/5").rsplit(2)
        StringPath('/1/2/3'), '4', '5'
        """
        data = string if string else str(self)
        return data.rsplit(self.sep, maxsplit)

    def join(self, other: list) -> str:
        """Join a list into a path

        >>> assert StringPath("").join(["one", "two"]) == "/one/two"
        """
        return self.sep.join(other or [])

    def contains(self, other: StrPath) -> bool:
        """If other is also a path then this path should start with other

        E.g. /path/to/file is "in" /path

        Otherwise, just use the sub-string sense of "in"
        """
        if isinstance(other, StringPath):
            return str(other).startswith(str(self))
        return str(other) in str(self)

    @property
    def name(self) -> str:
        return str(super().name)


StringPaths = list[StringPath]


class NoPath(StringPath):
    """An empty path

    >>> np = NoPath()
    >>> assert not np
    >>> assert np == NoPath(None) == NoPath(0) == NoPath(False)
    """

    def __init__(self, string: Any = ""):
        from pysyte.types.trees.dirs import DirectPath
        from pysyte.types.trees.files import FilePath

        self.string = string or ""
        self.fake_path = FilePath(self.string) or DirectPath(self.string)

    def __str__(self) -> str:
        """>>> assert NoPath('not a path') == 'not a path'"""
        return self.string

    def __repr__(self) -> str:
        """>>> assert repr(NoPath("not a path")) == "<NoPath 'not a path'>"""
        string = self.string
        if self.fake_path:
            string = str(self.fake_path)
        return f'<{self.__class__.__name__} "{string}">'

    def __bool__(self) -> bool:
        """>>> assert not NoPath('not a path')"""
        return False

    def __eq__(self, other: Any) -> bool:
        """
        >>> assert NoPath('') == NoPath() == NoPath(None)
        >>> assert NoPath('not a path') == 'not a path'
        """
        if self.string:
            return str(self) == str(other)
        return not other

    def __lt__(self, other: Any) -> bool:
        if self.string and other:
            return str(self) < str(other)
        return bool(other)

    def __truediv__(self, child: str) -> StringPath:
        """
        >>> bin = NoPath("/") / "bin"
        >>> assert bin and bin.isdir()
        >>> bin = NoPath("not a path") / "bin"
        >>> assert not bin and not bin.isdir()
        """
        result = os.path.join(self.string, child) if child else self.string
        from pysyte.types.trees.makes import makepath

        return makepath(result)

    def contains(self, other: StrPath) -> bool:
        """As this is not a real path, just use the substring sense

        >>> assert NoPath("not a path").contains(" a ")
        """
        return str(other) in str(self)

    @property
    def parent(self) -> StringPath:
        if "/" not in self.string:
            return self
        parent_string = "/".join(self.string.split("/")[:-1])
        from pysyte.types.trees.makes import makepath

        return makepath(parent_string)

    def exists(self) -> bool:
        return False

    isdir = isfile = isexec = isroot = exists

    def __getattr__(self, name: str) -> Any:
        return getattr(self.fake_path, name, None)

    def makedirs(self) -> None:
        os.makedirs(str(self))


def string_to_paths(string: str) -> StringPaths:
    """Split the string into paths

    >>> assert string_to_paths("/bin:/usr/bin") == [
    ...     StringPath("/bin"),
    ...     StringPath("/usr/bin"),
    ... ]
    """
    for c in ":,;":
        if c in string:
            return paths(string.split(c))
    return paths([string])


def _choose_paths(*strings, chooser: Callable) -> StringPaths:
    from pysyte.types.trees.makes import path

    paths_ = [path(_) for _ in strings]
    return [_ for _ in paths_ if chooser(_)]


def paths(*strings: Iterable) -> StringPaths:
    return _choose_paths(*strings, chooser=os.path.exists)


def directories(*strings: Iterable) -> StringPaths:
    return _choose_paths(*strings, chooser=os.path.isdir)


def files(*strings: Iterable) -> StringPaths:
    return _choose_paths(*strings, chooser=os.path.isfile)
