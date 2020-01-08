"""This module handles lists"""

import itertools


class Uniques(list):
    """A list of unique items"""
    def __init__(self, items=None):
        super().__init__([])
        self.extend(items or [])

    def predicate(self, _):
        """Subclasses can exclude items which return False"""
        # pylint: disable=no-self-use
        return True

    def append(self, item):
        if item in self:
            return False
        if not self.predicate(item):
            return False
        super().append(item)
        return True

    def extend(self, items):
        result = False
        for item in items or []:
            if self.append(item):
                result = True
        return result


class UniquelyTrues(Uniques):
    """A unique list of items all being true-ish"""
    def predicate(self, item):
        return bool(item)


def de_duplicate(items):
    """Remove any duplicate item, preserving order

    >>> assert de_duplicate([1, 9, 2, 8, 1, 7, 2]) == [1, 9, 2, 8, 7]
    """
    return list(Uniques(items))


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
