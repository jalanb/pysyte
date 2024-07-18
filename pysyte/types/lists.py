"""This module handles lists"""

import itertools

from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Tuple
from typing import TypeVar

Unique = TypeVar("Unique")  # Generic type


class Nones(list):
    limit: int = 0

    def __init__(self, limit: int, *args):
        self.limit = limit
        self.check(len(args))
        self.args = args
        super().__init__(*args)

    def check(self, i) -> bool:
        if self.limit < 0:
            return True
        if len(self.args) <= self.limit:
            return True
        raise TypeError(f"{self.__class__.__name__} has nothing at {i=}")

    def __getitem__(self, i) -> Any:
        self.check(i)
        return super().__getitem__(i)


class One(Nones):
    def __init__(self, *args):
        self.one, *_ = args
        super().__init__(1, [self.one])


class Two(Nones):
    def __init__(self, *args):
        self.one, self.two, *_ = args
        super().__init__(2, args)


class Many(Two):
    def __init__(self, *args):
        super().__init__(8, args)


class Lots(Many):
    def __init__(self, *args):
        self.limit = -1
        super().__init__(-1, args)


# https://stackoverflow.com/a/25464724/500942
class Uniques(list):
    """A list of unique items

    Uniqueness is checked when appending to the list
    """

    def __init__(self, items=None):
        super().__init__([])
        self.extend(items or [])

    def predicate(self, _: Unique) -> bool:
        """Subclasses can exclude items which return False"""
        return True

    def convert(self, item: Unique) -> Unique:
        return item

    def append(self, item: Unique) -> None:
        if item in self:
            return
        if not self.predicate(item):
            return
        super().append(self.convert(item))

    def extend(self, items: Iterable[Unique]) -> None:
        for item in items or []:
            self.append(item)


class UniquelyTrues(Uniques):
    """A unique list of items all being true-ish"""

    def predicate(self, item: Unique) -> bool:
        return bool(item)


def de_duplicate(items: List) -> List:
    """Remove any duplicate item, preserving order

    >>> assert de_duplicate([1, 9, 2, 8, 1, 7, 2]) == [1, 9, 2, 8, 7]
    """
    return list(Uniques(items))


def flatten(list_of_lists: List[List]) -> List:
    """Reduce a lists of lists to a list, comprehensively

    >>> assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    Thanks to Alex Martelli at
        https://stackoverflow.com/a/952952/500942
    """
    return [item for list_ in list_of_lists for item in list_]


def flatten_(list_of_lists: List[List]) -> List:
    """Reduce a lists of lists to a list, functionally

    >>> assert flatten_([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    Thanks to CTT at
        https://stackoverflow.com/a/716482/500942
    """
    return list(itertools.chain.from_iterable(list_of_lists))


def as_list(item):
    """Make item a list from types which can index, have items, or can pop"""
    try:
        item.index
        return list(item)
    except AttributeError:
        try:
            return list(item.items())
        except AttributeError:
            try:
                item.pop
                return list(item)
            except AttributeError:
                raise TypeError(f"Cannot make a list from {item!r}")


def splits(predicate: Callable, items: List) -> Tuple[List[Any], List[Any]]:
    """Split a list into 2 lists based one the predicate

    >>> is_odd = lambda x: bool(x % 2)
    >>> odds, evens = splits(is_odd, [0, 1, 2, 3, 4, 5, 6])
    >>> assert odds == [1, 3, 5]
    >>> assert evens == [0, 2, 4, 6]
    """
    one: List[Any] = []
    two: List[Any] = []
    for item in items:
        destination = one if predicate(item) else two
        destination.append(item)
    return one, two
