from dataclasses import dataclass
from functools import partial
from typing import Callable
from typing import List

"""
>>> faxed, fixed = applied((fax, fix), (+7, -999))
>>> assert faxed == (7, 0)
>>> assert fixed == (0, -999)

"""

fax = lambda x: max(0, x)
fix = lambda x: min(0, x)
applied = lambda a, b: tuple(tuple(x(y) for x in a) for y in b)


def upper_choice(a, b) -> int:
    """Compare the args into 2 choices"""
    try:
        return fax(a - b)
    except TypeError:
        return +1 if a > b else 0


def lower_choice(a, b) -> int:
    """Compare the args into 2 choices"""
    try:
        return fix(a - b)
    except TypeError:
        return -1 if a < b else 0


def binary_choice(a, b) -> int:
    """Constrain the args' values into 3 choices"""
    try:
        return a - b
    except TypeError:
        return +1 if a > b else -1 if a < b else 0


def binary_chooser(a, b) -> int:
    """Compare the args into 3 choices"""
    return +1 if a > b else -1 if a < b else 0


def average(lo: int, hi: int) -> int:
    """Calculate the average of two integers, floor dividing by 2."""
    return (lo + hi) // 2


@dataclass
class Chooser:
    """A context manager for choosers"""

    chooser: Callable

    def choose(self, a, b):
        return self.chooser(a, b)


@dataclass
class Picker:
    """A context manager for pickers"""

    picker: Callable

    def __post_init__(self):
        pass

    def __enter__(self):
        return self.picker

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __call__(self, *args, **kwargs):
        return self.pick(*args, **kwargs)

    def pick(self, *args, **kwargs):
        return self.picker(*args, **kwargs)


def directed_search(average: Picker, arr: List[int], sought: int) -> int:
    """
    Perform a directed search on a sorted array to find the index of a sought element.

    Parameters:
        average (Picker): Function to calculate mid-point.
        arr (List[int]): The sorted array.
        sought (int): The element to find.

    Returns:
        int: The index of the sought element, or -1 if not found.

    Example:
        >>> binary_search([1, 2, 3, 4, 5], 3)
        2
        >>> binary_search([1, 2, 3, 4, 5], 6)
        -1
        >>> i = 1024
        >>> items = list(range(i))
        >>> import random
        >>> j = random.randint(0, i)
        >>> random.shuffle(items)
        >>> assert binary_search(items, j) < i
    """
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        i = average.pick(lo, hi)
        item = arr[i]
        if item == sought:
            return i
        elif item < sought:
            lo = i + 1
        else:
            hi = i - 1

    return -1


binary_search = partial(directed_search, Picker(average))

# Doctest
if __name__ == "__main__":
    import doctest

    doctest.testmod()
