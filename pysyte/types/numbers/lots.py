"""handle numbers for pysyte

>>> one = lots([''])
>>> assert one.limit == 1
>>> two = lots(["", ""])
>>> assert two.limit == 2
>>> three = lots([1, "7", 9])
>>> assert three.limit == 3
>>> four = lots([9, 5, 3, 0])
>>> assert four.limit == 4

>>> assert two + one == three

"""
from typing import Any

from dataclasses import dataclass
from dataclasses import field


@dataclass
class Nones(list):
    args: list = field(default_factory=list)

    def __post_init__(self):
        breakpoint()
        self.limit = 0
        self.check_args()

    def check_args(self):
        try:
            self.check(len(self.args))
        except IndexError as e:
            args = self.args
            raise ValueError(f"{self.__class__.__name__}({args=!r}): Too many args")

    def __int__(self):
        return len(self.args)

    def __str__(self):
        return str(int(self))

    def __repr__(self):
        return f'<{self.__class__.__name__} {int(self)} {self.args}>'

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
