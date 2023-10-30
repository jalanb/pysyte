"""Miscellaneous string handlers

"""

from functools import total_ordering


def pp(name, value):
    """
    >>> assert pp("x", 0) == 'x: int == 0'
    """
    named = name
    valued = f'{value.__class__.__name__} == {value!r}'
    return f'{named}: {valued}'


class Repper:
    """Add a repr() to anything that can do str(self)"""
    def __str(self):
        raise NotImplementedError

    def __repr__(self) -> str:
        string = str(self)
        return f'<{self.__class__.__name__} "{string}">'


@total_ordering
class Stringer:
    """A Mixin to provide more ops to a class that can str()"""

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


def pp(name, value):
    """
    >>> assert pp("x", 0) == 'x: int == 0'
    """
    named = name
    valued = f'{value.__class__.__name__} == {value!r}'
    return f'{named}: {valued}'
