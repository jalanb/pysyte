"""handle numbers for pysyte

>>> one = lots([""])
>>> assert one.limit == 1
>>> two = lots(["", ""])
>>> assert two.limit == 2
>>> three = lots([1, "7", 9])
>>> assert three.limit == 3
>>> four = lots([9, 5, 3, 0])
>>> assert four.limit == 4

>>> assert two + one == three

>>> assert not zero
>>> assert one.is_one and not any(_.is_one for _ in (zero, two, many, lots))
"""

from dataclasses import dataclass
from functools import total_ordering



@dataclass
class OTMLData:
    i: int = 0


@total_ordering
class OTML(OTMLData):
    """A number in the "1, 2, many, lots" number system

    >>> i = OTML(7)
    >>> assert i.is_many and not (i.is_one or i.is_two or i.is_lots)
    """

    def __postinit__(self):
        """Set some 'is_...' booleans

    def __str__(self):
        return str(int(self))

    def __repr__(self):
        return f"<{self.__class__.__name__} {int(self)} {self.args}>"

    def __add__(self, other):
        return lots(self.args + other.args)

    def __sub__(self, other):
        return lots(self.args[-len(other.args) :])  # + other.args)

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def __lt__(self, other):
        return int(self) < int(other)

    def __getitem__(self, i) -> Any:
        self.check(i)
        return super().__getitem__(i)

    @property
    def max(self):
        return 5

    def check(self, i) -> bool:
        if self.limit >= self.max:
            return True
        if len(self.args) > self.limit:
            raise IndexError(f"{self.__class__.__name__} has nothing at {i=}")
        return True
        raise TypeError(f"{self.__class__.__name__} has nothing at {i=}")


class One(Nones):
    def __post_init__(self):
        self.limit = 1
        self.check_args()


class Two(Nones):
    def __post_init__(self):
        self.limit = 2
        self.check_args()


class Many(Two):
    def __post_init__(self):
        self.limit = 4
        self.check_args()


class Lots(Many):
    def __post_init__(self):
        self.limit = self.max + 1
        self.check_args()


def lots(args: list, many=3):
    a = len(args)
    match a:
        case 0:
            return None
        case 1:
            return One(args)
        case 2:
            return Two(args)
    if a <= many:
        return Many(args)
    return Lots(args)
