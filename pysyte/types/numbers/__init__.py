"""This module handles numbers for pysyte

>>> from pysyte.types import numbers

integers and strings work like int() for both
>>> assert numbers.as_int(5) == 5 == numbers.as_int(" 5  ")
>>> assert numbers.inty(5) == 5 == numbers.inty("5   ")

inty() does extra computation is done for things with a length

>>> assert numbers.inty("lll") == 3
>>> assert (
...     numbers.inty(
...         [
...             3,
...         ]
...     )
...     == 1
... )

as_int() does not
>>> try:
...     numbers.as_int("lll")
...     assert False
... except numbers.NAN:
...     pass
...
>>> try:
...     numbers.as_int(
...         [
...             3,
...         ]
...     )
...     assert False
... except numbers.NAN:
...     pass
...
"""


class NAN(ValueError):
    def __init__(self, value):
        super().__init__(f"NAN: {value}")


def _to_number(value, kind, default):
    """Convert the value to that kind of int, using that default

    >>> assert _to_number(3, int, 7) == 3
    >>> assert _to_number(3, float, 7) == 3.0
    >>> assert _to_number(None, int, 7) == 7
    >>> assert _to_number(None, float, 7) == 7.0
    >>> assert _to_number(3, int, None) == 3
    >>> assert _to_number(3, float, None) == 3.0
    """
    try:
        return kind(value)
    except (ValueError, TypeError):
        if default is None:
            raise NAN(value)
        if isinstance(value, (type(None),)):
            return kind(default)
        try:
            return len(value)
        except TypeError:
            raise ValueError(value)


as_int = lambda x: _to_number(x, int, None)
as_float = lambda x: _to_number(x, float, None)

inty = lambda x: _to_number(x, int, x)
floaty = lambda x: _to_number(x, float, x)
