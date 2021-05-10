"""Handle iterators for pysyte"""

from typing import Sequence
from typing import TypeVar

T = TypeVar("T")  # Declare Type variable


def first(sequence: Sequence[T], message=None) -> T:  # Generic function
    """The first item in that sequence

    If there aren't any, raise a ValueError with that message

    >>> assert first([1, 2, 3]) == 1
    """
    try:
        return next(iter(sequence))
    except StopIteration:
        raise ValueError(message or (f"Sequence is empty: {sequence}"))


def last(sequence: Sequence[T], message=None) -> T:
    """The last item in that sequence

    If there aren't any, raise a ValueError with that message

    >>> assert last([1, 2, 3]) == 3
    """
    return first(list(reversed(sequence)), message)


def first_or(sequence: Sequence[T], value) -> T:
    """First item in that sequence, or that value

    >>> assert first_or([1, 2, 3], 4) == 1
    >>> assert first_or([], 4) == 4
    """
    try:
        return first(sequence)
    except ValueError:
        return value


def first_that(predicate, sequence: Sequence[T], message=None) -> T:
    """The first item in that sequence that matches that predicate

    If none matches raise a KeyError with that message

    >>> assert first_that(lambda x: x > 1, [1, 2, 3]) == 2
    """
    try:
        return first([_ for _ in sequence if predicate(_)])
    except (ValueError, StopIteration):
        raise KeyError(message or "Not Found")
