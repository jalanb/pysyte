"""This module handles lists"""

import itertools


def de_duplicate(items):
    """Remove any duplicate item, preserving order

    >>> assert de_duplicate([1, 9, 2, 8, 1, 7, 2]) == [1, 9, 2, 8, 7]
    """
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def flatten(list_of_lists):
    """Reduce a lists of lists to a list, comprehensively

    >>> assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    Thanks to Alex Martelli at
        https://stackoverflow.com/a/952952/500942
    """
    return [item for list_ in list_of_lists for item in list_]


def flatten_(list_of_lists):
    """Reduce a lists of lists to a list, functionally

    >>> assert flatten_([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    Thanks to CTT at
        https://stackoverflow.com/a/716482/500942
    """
    return list(itertools.chain.from_iterable(list_of_lists))



