"""This module provides methods to handle some features of English words"""

import inflect

_inlection = inflect.engine()


def pluralize(string):
    """Returns the plural of string.

    >>> pluralize('Cow')  == 'Cows'
    True
    """
    return _inlection.plural_noun(string)


def singularize(string):
    """Returns the singular of string.

    >>> singularize('Cows') == 'Cow'
    True
    """
    return _inlection.singular_noun(string)


def number_name(item):
    """The English name for that number

    >>> assert number_name(5) == 'five'
    """
    return _inlection.number_to_words(item)
