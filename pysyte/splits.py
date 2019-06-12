"""Generic methods for splitting strings"""


import re

from pysyte import literals


def _default_separator():
    """The default separator used by all methods is a comma

    Monkey-patching this method can change that default
    """
    return literals.Punctuation.comma


def join(items, separator=None):
    """Join the items into a string using the separator

    Converts items to strings if needed

    >>> join([1, 2, 3])
    '1,2,3'
    """
    if not items:
        return ''
    if separator is None:
        separator = _default_separator()
    return separator.join([str(item) for item in items])


def seamless_join(items):
    """A seamless join does not show where the joins are

    >>> seamless_join(['fred', 'was', 'here'])
    'fredwashere'
    """
    return join(items, literals.Empty.string)


def split(string, separator_regexp=None, maxsplit=0):
    """Split a string to a list

    >>> split('fred, was, here')
    ['fred', ' was', ' here']
    """
    if not string:
        return []
    if separator_regexp is None:
        separator_regexp = _default_separator()
    if not separator_regexp:
        return string.split()
    return re.split(separator_regexp, string, maxsplit)


def split_and_strip(string, separator_regexp=None, maxsplit=0):
    """Split a string into items and trim any excess spaces from the items

    >>> split_and_strip('fred, was, here  ')
    ['fred', 'was', 'here']
    """
    if not string:
        return ['']
    if separator_regexp is None:
        separator_regexp = _default_separator()
    if not separator_regexp:
        return string.split()
    return [item.strip()
            for item in re.split(separator_regexp, string, maxsplit)]


def split_and_strip_without(string, exclude, separator_regexp=None):
    """Split a string into items, and trim any excess spaces

    Any items in exclude are not in the returned list

    >>> split_and_strip_without('fred, was, here  ', ['was'])
    ['fred', 'here']
    """
    result = split_and_strip(string, separator_regexp)
    if not exclude:
        return result
    return [x for x in result if x not in exclude]


def split_and_strip_whole(string, separator_regexp=None):
    """Split a string into items and trim any excess spaces from the items

    Exclude any empty items

    >>> split_and_strip_whole('fred, , was,here,')
    ['fred', 'was', 'here']
    """
    return split_and_strip_without(string, [''], separator_regexp)


def split_by_count(items, count, filler=None):
    """Split the items into tuples of count items each

    >>> split_by_count([0,1,2,3], 2)
    [(0, 1), (2, 3)]

    If there are a mutiple of count items then filler makes no difference
    >>> split_by_count([0,1,2,7,8,9], 3, 0) == split_by_count([0,1,2,7,8,9], 3)
    True

    If there are not a multiple of count items, then any extras are discarded
    >>> split_by_count([0,1,2,7,8,9,6], 3)
    [(0, 1, 2), (7, 8, 9)]

    Specifying a filler expands the "lost" group
    >>> split_by_count([0,1,2,7,8,9,6], 3, 0)
    [(0, 1, 2), (7, 8, 9), (6, 0, 0)]
    """
    if filler is not None:
        items = items[:]
        while len(items) % count:
            items.append(filler)
    iterator = iter(items)
    iterators = [iterator] * count
    return list(zip(*iterators))


def pairs(items, filler=None):
    """Split the items into pairs

    >>> pairs([0,1,2,7,8,9,10])
    [(0, 1), (2, 7), (8, 9)]

    If a filler is used any unpaired items are retained
    >>> pairs([0,1,2,7,8,9,10], 99)
    [(0, 1), (2, 7), (8, 9), (10, 99)]
    """
    return split_by_count(items, 2, filler)


def threes(items, filler=None):
    """Split the items into groups of 3

    >>> threes([0,1,2,6,7,8,9])
    [(0, 1, 2), (6, 7, 8)]

    If a filler is used any discarded items are retained
    >>> threes([0,1,2,6,7,8,9], 5)
    [(0, 1, 2), (6, 7, 8), (9, 5, 5)]
    """
    return split_by_count(items, 3, filler)


def despaced(string):
    """Split a string into spaceless items

    Split on spaces, trim excess space, exclude any empty strings

    >>> despaced('fred, , was,here today')
    ['fred,', ',', 'was,here', 'today']
    """
    return split_and_strip_without(string, [''], ' ')


def words(string):
    """Split a string into words

    Split on (English) punctuaution, trim space, exclude any empty strings

    >>> words('fred, , was,here today')
    ['fred', 'was', 'here', 'today']
    """
    return split_and_strip_without(string, [''], '[,;. ]')


def rejoin(string, separator_regexp=None, spaced=False):
    """Split a string and then rejoin it

    Spaces are interspersed between items only if spaced is True

    >>> rejoin('fred, was, here  ')
    'fred,was,here'
    """
    strings = split_and_strip(string)
    if separator_regexp is None:
        separator_regexp = _default_separator()
    joiner = spaced and f'{separator_regexp} ' or separator_regexp
    return joiner.join(strings)
