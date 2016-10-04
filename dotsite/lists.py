"""This module handles lists"""


def de_duplicate(items):
    """Remove any duplicate item, preserving order

    >>> de_duplicate([1, 2, 1, 2])
    [1, 2]
    """
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result
