"""Generic methods for splitting strings"""

import re
from typing import Any, List, Optional, Tuple

from pysyte.types.literals import nones


# Available to mockers and monkey-patchers
splits_separator = ","


def join(items: list, separator: str = splits_separator) -> str:
    """Join the items into a string using the separator

    Converts items to strings if needed

    >>> assert join([1, 2, 3]) == '1,2,3'
    """
    if not items:
        return ""
    if separator is None:
        separator = splits_separator
    return separator.join([str(item) for item in items])


def seamless_join(items: list) -> str:
    """A seamless join does not show where the joins are

    >>> assert seamless_join(['fred', 'was', 'here']) == 'fredwashere'
    """
    return join(items, nones.string)


def split(string: str, separator_regexp: str = splits_separator, maxsplit=0) -> List[str]:
    """Split a string to a list

    >>> assert split('fred, was, here') == ['fred', ' was', ' here']
    """
    if not string:
        return []
    if not separator_regexp:
        return string.split()
    return re.split(separator_regexp, string, maxsplit)


def split_and_strip(
    string: str, separator_regexp: str = splits_separator, maxsplit=0
) -> List[str]:
    """Split a string into items and trim any excess spaces from the items

    >>> assert split_and_strip('fred, was, here  ') == ['fred', 'was', 'here']
    """
    if not string:
        return [""]
    if not separator_regexp:
        return string.split()
    return [item.strip() for item in re.split(separator_regexp, string, maxsplit)]


def split_and_strip_without(
    string: str, exclude, separator_regexp: str = splits_separator
) -> List[str]:
    """Split a string into items, and trim any excess spaces

    Any items in exclude are not in the returned list

    >>> assert split_and_strip_without('fred, was, here  ', ['was']) == ['fred', 'here']
    """
    result = split_and_strip(string, separator_regexp)
    if not exclude:
        return result
    return [x for x in result if x not in exclude]


def split_and_strip_whole(
    string: str, separator_regexp: str = splits_separator
) -> List[str]:
    """Split a string into items and trim any excess spaces from the items

    Exclude any empty items

    >>> assert split_and_strip_whole('fred, , was,here,') == ['fred', 'was', 'here']
    """
    return split_and_strip_without(string, [""], separator_regexp)


def split_by_count(items: list, count, filler: Optional[Any] = splits_separator) -> List[Tuple]:
    """Split the items into tuples of count items each

    >>> assert split_by_count([0, 1, 2, 3], 2) == [(0, 1), (2, 3)]

    If there are a mutiple of count items then filler makes no difference
    >>> fred = [0, 1, 2, 7, 8, 9]
    >>> assert split_by_count(fred, 3, 0) == split_by_count(fred, 3)

    If there are not a multiple of count items, then any extras are discarded
    >>> assert split_by_count([0, 1, 2, 7, 8, 9, 6], 3) == [(0, 1, 2), (7, 8, 9)]

    Specifying a filler expands the "lost" group
    >>> assert split_by_count([0, 1, 2, 7, 8, 9, 6], 3, 0) == [(0, 1, 2), (7, 8, 9), (6, 0, 0)]
    """
    if filler is not None:
        items = items[:]
        while len(items) % count:
            items.append(filler)
    iterator = iter(items)
    iterators = [iterator] * count
    return list(zip(*iterators))


def pairs(items: list, filler: Optional[Any] = splits_separator) -> List[Tuple]:
    """Split the items into pairs

    >>> assert pairs([0, 1, 2, 7, 8, 9, 10]) == [(0, 1), (2, 7), (8, 9)]

    If a filler is used any unpaired items are retained
    >>> assert pairs([0, 1, 2, 7, 8, 9, 10], 99) == [(0, 1), (2, 7), (8, 9), (10, 99)]
    """
    return split_by_count(items, 2, filler)


def threes(items: list, filler: Optional[Any] = splits_separator) -> List[Tuple]:
    """Split the items into groups of 3

    >>> threes([0, 1, 2, 6, 7, 8, 9])
    [(0, 1, 2), (6, 7, 8)]

    If a filler is used any discarded items are retained
    >>> threes([0, 1, 2, 6, 7, 8, 9], 5)
    [(0, 1, 2), (6, 7, 8), (9, 5, 5)]
    """
    return split_by_count(items, 3, filler)


def despaced(string: str) -> List[str]:
    """Split a string into spaceless items

    Split on spaces, trim excess space, exclude any empty strings

    >>> despaced('fred, , was,here today')
    ['fred,', ',', 'was,here', 'today']
    """
    return split_and_strip_without(string, [""], " ")


def words(string: str) -> List[str]:
    """Split a string into words

    Split on (English) punctuaution, trim space, exclude any empty strings

    >>> words('fred, , was,here today')
    ['fred', 'was', 'here', 'today']
    """
    return split_and_strip_without(string, [""], "[,;. ]")


def rejoin(string: str, separator_regexp: str = splits_separator, spaced=False) -> str:
    """Split a string and then rejoin it

    Spaces are interspersed between items only if spaced is True

    >>> assert rejoin('fred, was, here  ') == 'fred,was,here'
    """
    strings = split_and_strip(string)
    joiner = spaced and f"{separator_regexp} " or separator_regexp
    return joiner.join(strings)
