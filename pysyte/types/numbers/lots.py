"""handle numbers for pysyte

>>> zero = otml(0)
>>> one = otml(1)
>>> two = otml(2)
>>> many = otml(random.randint(3,9))
>>> lots = otml(random.randint(10,9_999_999_999))

>>> assert not zero
>>> assert one.is_one and not any(_.is_one for _ in (zero, two, many, lots))
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass
class OTMLData:
    i : int = 0

@total_ordering
class OTML(OTMLData):
    """A number in the "1, 2, many, lots" number system

    >>> i = OTML(7)
    >>> assert i.is_many and not (i.is_one or i.is_two or i.is_lots)
    """

    def __postinit__(self):
        """Set some 'is_...' booleans

        >>> i = OTML(7)
        >>> assert i.is_many
        >>> assert not (i.is_one or i.is_two or i.is_lots)
        """
        rules = {
            "one": self.i == 1,
            "two": self.i == 2,
            "many":  2 < self.i <= 9,
            "lots": self.i > 9,
        }
        [setattr(f'is_{k}', v) for k, v in rules.items()]


def otml(i: int) -> OTML:
    try:
        j = int(i)
        return OTML(j)
    except (ValueError, TypeError):
        raise TypeError(f'Cannot use {i!r} in "1, 2, many, lots"')
