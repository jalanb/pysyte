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
from dataclasses import field
from typing import Any


@dataclass
class OTMLData:
    i: int = 0


@total_ordering
class OTML(OTMLData):
    """A number in the "1, 2, many, lots" number system

    """
    def check_args(self):
        try:
            if self.limit and self.i > self.limit:
                 raise IndexError(f"{self.__class__.__name__}: {self.i=} > {self.limit}")
        except IndexError:
            args = self.i
            raise ValueError(f"{self.__class__.__name__}({args=!r}): Too many args")

    def __postinit__(self):
        """Set some 'is_...' booleans"""
        self.too_many = 10
        self.is_lots = len(self.i) >= self.too_many_digits
        self.is_one = len(self.i) == 1
        self.is_two = len(self.i) == 2
        self.is_many = len(self.i) > 2 and not self.is_lots

    def __str__(self):
        return str(int(self))

    def __repr__(self):
        return f"<{self.__class__.__name__} {int(self)} {self.i}>"

    def __add__(self, other):
        return lots(self.i + other.i)

    def __sub__(self, other):
        return lots(self.i[-len(other.i) :])

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def __lt__(self, other):
        return int(self) < int(other)



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
        self.limit = self.too_many - 1
        self.check_args()


class Lots(Many):
    def __post_init__(self):
        self.limit = None
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
