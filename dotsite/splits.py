"""Generic methods for splitting strings"""


import re


from dotsite.literals import Empty
from dotsite.literals import Punctuation


def _default_separator():
    """The default separator used by all methods is a comma

    Monkey-patching this method can change that default
    """
    return Punctuation.comma


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
    return join(items, Empty.string)


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
    joiner = spaced and '%s ' % separator_regexp or separator_regexp
    return joiner.join(strings)
