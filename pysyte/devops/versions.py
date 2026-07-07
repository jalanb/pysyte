"""Handle version numbers for pysyte


Make versions from strings or lists

>>> assert Version("2.3.5") == Version((2, 3, 5)) == Version((2, "3", 5))

>>> version = Version("2.6.m")
>>> assert version.major == "2"
>>> assert version.minor == "6"
>>> assert version.patch == "m"

Can compare versions

>>> Ver = Version
>>> assert Ver("3.9.9") < Ver("3.9.10") < Ver((7, 3)) < Ver("10.0.0")

Numbers are compared, not strings

>>> assert Ver([9]) == Ver("9") < Ver("10") == Ver([10])

Letters are always lower than digits

    >>> assert Ver("2.3.z") < Ver("2.3.0")

"""

from functools import total_ordering
from itertools import zip_longest
from typing import Sequence

from lazy import lazy

from pysyte.types.strings import Stringer

version_zeroes = "0.0.0"


def _as_int(string: str) -> int | None:
    """Convert various patch string parts to integers

    Numeric strings are converted strightforwardly
    Letters are converted to negative values
    Others give 'None'

    >>> assert _as_int("") is None and _as_int(";;;") is None
    >>> assert _as_int("A") == _as_int("a") < 0
    >>> assert _as_int("888") == 888
    """
    try:
        c = string[0]
    except IndexError:
        return None
    if c.isalpha():
        return ord(c.lower()) - (ord("z") + 1)
    try:
        return int(string)
    except (TypeError, ValueError):
        return None


def _zip_to_ints(version: Version, other: str):
    """zip parts of version and parts of other for comparisons"""
    strings = other.split(version.sep, 2)
    return zip_longest(
        [_as_int(_) for _ in version.split()],
        [_as_int(str(_)) for _ in strings],
        fillvalue=None,
    )


@total_ordering
class Version(Stringer):
    """A version number, with major, minor and patch parts"""

    def __init__(self, data: str | Sequence | Version):
        """Make a version from those data

        data can be a string or a sequence of parts, e.g.
        >>> assert Version("1.0.2") == Version([1, 0, 2])

        or it could be another version, e.g.
        >>> v1 = Version("1.0.2")
        >>> v2 = Version(v1)
        >>> assert v1 == v2
        """
        self.sep = "."
        if not data:
            self.string = version_zeroes
        elif isinstance(data, (str, Version)):
            self.string = str(data)
        else:
            self.string = self._join([str(_) for _ in data])
        for part in self.string.split("."):
            if part and not part.isalnum():
                raise ValueError(f"{data} is not a version")

    def __bool__(self):
        """Whether the version has a non-zero value"""
        return self.started()

    def __str__(self):
        """The version as a string

        >>> assert str(Version((3, 2, 1))) == "3.2.1"
        """
        return self.string

    def _comparable(self, other: object):
        """Raise an exception if other is not a type comparable to a Version"""
        if not isinstance(other, (str, int, float, Version)):
            raise NotImplementedError(
                f"Cannot compare {self.__class__.__name__} to {type(other)}"
            )

    def __eq__(self, other: object) -> bool:
        """Whether other is same as self

        Parts are compared individually:
            major to major, minor to minor, patch to patch

        >>> assert Version((3, 2, 1)) == Version("3.2.1")
        >>> assert Version((3, 2, 1)) == "3.2.1"
        >>> assert Version((3, 5)) == 3.5
        """
        self._comparable(other)
        for i, j in _zip_to_ints(self, str(other)):
            if not i and not j:
                continue
            if i != j:
                return False
        return True

    def __lt__(self, other: object) -> bool:
        """Whether self is less than other

        Parts are compared, as numbers, not strings

        >>> assert Version("3.9.0") < Version("3.10.0")
        """
        self._comparable(other)
        for i, j in _zip_to_ints(self, str(other)):
            if i is None and j is None:
                continue
            elif i is None:
                return True
            elif j is None:
                return False
            elif i > j:
                return False
            elif i < j:
                return True
        return False

    @property
    def string(self) -> str:
        """The string representation of the version"""
        return self._string

    @string.setter
    def string(self, value: str):
        """Set the string representation of the version"""
        self._string = value

    def started(self) -> bool:
        """Whether the version number has started

        i.e. the version should have some value
            and the value should be > 0.0.0

        >>> assert not Version("0.0.0").started()
        >>> assert Version("0.0.1").started()
        """
        return bool(self.string) and self.string != version_zeroes

    def split(self) -> tuple[str, ...]:
        """Split the version into major, minor, patch parts, as strings

        >>> assert Version("3.9.0").split() == ('3', '9', '0')
        """
        return tuple(self.string.split(self.sep, 2))

    def _join(self, *args: Sequence) -> str:
        """Join the parts to a string

        >>> assert Version("")._join(('3', '9', 'z')) == "3.9.z"
        """
        return self.sep.join(*args)

    def part(self, i: int) -> str:
        """The i'th part of the version

        >>> assert Version("8.4.ff").part(1) == '4'
        """
        try:
            return self.split()[i]
        except IndexError:
            return ""

    @lazy
    def major(self) -> Version:
        """The major version in this version

        >>> assert Version("4.7.2").major == Version("4") == Version("4.0.0")
        """
        return Version(self.part(0))

    @lazy
    def minor(self) -> str:
        """The minor part of this version

        >>> assert Version("4.7.2").minor == '7'
        """
        return self.part(1)

    def next_minor(self) -> Version:
        """The next minor version after this

        >>> assert Version("4.7.2").next_minor() == Version("4.8.0")
        """
        return self._change_minor("+")

    def prev_minor(self) -> Version:
        """The previous minor version before this version

        >>> assert Version("4.7.2").prev_minor() == Version("4.6.0")
        """
        return self._change_minor("-")

    def _change_minor(self, sign: str) -> Version:
        """The next or previous minor version from this version

        Choose the next minor with a '+' sign
            Or the previous one with '-'

        >>> assert Version("4.7.2")._change_minor('+') == Version("4.8.0")
        >>> assert Version("4.7.2")._change_minor('-') == Version("4.6.0")
        """
        major = self.part(0)
        minor = eval(f"int({self.minor}) {sign} 1")
        return self.__class__(f"{major}.{minor}")

    @property
    def patch(self) -> str:
        """The patch part of this version

        >>> assert Version("4.7.2").patch == '2'
        """
        return self.part(2)

    @patch.setter
    def patch(self, value: str | int):
        """Change the patch value in this version

        >>> v1 = Version("4.7.2")
        >>> v1.patch = 99
        >>> assert v1 == Version("4.7.99")
        """
        str_value = str(value)
        parts = list(self.split())
        if len(parts) < 3:
            assert len(parts) > 1
            parts.append(str_value)
        else:
            parts[2] = str_value
        self.string = self._join(parts)

    @lazy
    def production(self) -> Version:
        """A version which discards the patch value of this version

        We drop the patch when releasing to production
            So, if we are testing version "5.6.88"
            and decide to release that to production server
            then we change the version to "5.6" (aka "5.6.0")

        >>> assert Version("5.6.88").production == Version("5.6")
        """
        return self.__class__((self.major, self.minor))

    @lazy
    def tag(self) -> str:
        """A string of this version, suitable to use in a git tag

        >>> assert Version("5.6.88").tag == "v5.6.88"
        """
        return f"v{self}"


class VersionZero(Version):
    """This class allows mypy to recognise empty versions"""

    def __init__(self):
        """Initialise with a zero verion string

        >>> assert VersionZero() == Version("0.0.0")
        """
        super().__init__(version_zeroes)

    def __bool__(self):
        """This is always false"""
        return False

    def __str__(self):
        """The string of a VersionZero should always be '0.0.0'

        >>> assert str(VersionZero()) == "0.0.0"
        """
        return version_zeroes

    def __eq__(self, other: object) -> bool:
        """Equal to the other only if that is not true-ish

        >>> assert VersionZero() == None
        >>> assert VersionZero() == 0
        >>> assert VersionZero() != 1
        """
        return not other

    def __lt__(self, other: object) -> bool:
        """If the other is true-ish then this is less than it

        >>> assert VersionZero() < 1.1
        >>> assert VersionZero() >= 0.0
        """
        return bool(other)

    @lazy
    def is_hotfix(self) -> bool:
        """A VersionZero is not for a Hotfix Release"""
        return False
