"""Miscellaneous string handlers"""

from functools import total_ordering


class Repper:
    """Make a nice repr(x) for any x that can do str(x)"""

    def __repr__(self) -> str:
        string = str(self)
        return f'<{self.__class__.__name__} "{string}">'


@total_ordering
class Stringer(Repper):
    """A Mixin to provide more ops to a class that can str()"""

    def __str__(self):
        raise NotImplementedError

    def __hash__(self):
        """Derive a hash value from the string"""
        return hash(str(self))

    def __eq__(self, other):
        """Whether this equals other, compared as strings"""
        return str(self) == str(other)

    def __ne__(self, other):
        """Whether this differs from other, compared as strings"""
        return str(self) != str(other)

    def __lt__(self, other):
        """Whether this is less than other, compared as strings"""
        return str(self) < str(other)
