"""Handle iterators for pysyte"""

from typing import Sequence
from typing import TypeVar

T = TypeVar("T")  # Declare Type variable


def first(sequence: Sequence[T], message=None) -> T:  # Generic function
    """The first item in that sequence

    If there aren't any, raise a ValueError with that message

    >>> assert first("fred") == "f"
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
        raise KeyError(f":-(\n{message}\n{e}" if message else f":-(\n{e}")


def take_until(predicate, iterable):
    """All items in iterable (inclusive) until predicate is truish

    >>> list(take_until(lambda x: x == 6, [1, 4, 6, 4, 1])) == [1, 4, 6]
    True
    """
    for item in iterable:
        yield item
        if predicate(item):
            break


def drop_from_end(predicate, iterable):
    """Drop items from end as long as predicate is True

    >>> drop_from_end(lambda x: not x, [0, 1, 2, 3, None, 3, 0, None])
    [0, 1, 2, 3, None, 3]
    """
    type_ = type(iterable)
    return type_(reversed(type_(dropwhile(lambda x: predicate(x), reversed(iterable)))))


def drop_falsies_from_end(iterable):
    return drop_from_end(lambda x: not x, iterable)
