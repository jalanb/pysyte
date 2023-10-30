"""Some methods to help with the handling of dictionaries"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from yamlreader import data_merge


def get_caselessly(dictionary, sought):
    """Find the sought key in the given dictionary regardless of case

    >>> things = {'Fred': 9}
    >>> print(get_caselessly(things, 'fred'))
    9
    """
    try:
        return dictionary[sought]
    except KeyError:
        caseless_keys = {k.lower(): k for k in dictionary.keys()}
        real_key = caseless_keys[sought.lower()]  # allow any KeyError here
        return dictionary[real_key]


def swap_dictionary(dictionary):
    """Swap keys for values in the given dictionary

    >>> swap_dictionary({'one': 1})[1] == 'one'
    True
    """
    if dictionary is None:
        return None
    return {v: k for k, v in dictionary.items()}


def append_value(dictionary, key, item):
    """Append those items to the values for that key"""
    items = dictionary.get(key, [])
    items.append(item)
    dictionary[key] = items


def extend_values(dictionary, key, items):
    """Extend the values for that key with the items"""
    values = dictionary.get(key, [])
    try:
        values.extend(items)
    except TypeError:
        raise TypeError("Expected a list, got: %r" % items)
    dictionary[key] = values


def group_list(items):
    """Items in the list are grouped into a dictionary

    Items should be a list of (key, value) pairs

    >>> grouped = group_list([(1, 0), (2, 0), (1, 1)])
    >>> grouped[1] == [0, 1]
    True
    """
    groups = defaultdict(list)
    for key, value in items:
        groups[key].append(value)
    return groups


def group_list_by(items, key_from_item):
    """Items in the list are grouped into a dictionary

    key_from_item is a method to get the key from the item

    >>> items = [(1, 9), (2, 8), (1, 7)]
    >>> key_from_item = lambda x: 'a' if x[0] == 1 else 'b'
    >>> grouped = group_list_by(items, key_from_item)
    >>> grouped['a'] == [(1, 9), (1, 7)]
    True
    """
    groups = defaultdict(list)
    for item in items:
        key = key_from_item(item)
        groups[key].append(item)
    return groups


class DefaultDict(defaultdict):
    """A default dict with improved repr"""

    def __repr__(self):
        from pprint import pformat

        name = self.__class__.__name__
        value = pformat(dict(self), indent=4)
        return f"<{name}\n    {value}\n>"


@dataclass
class LazyDefaultDict(DefaultDict):
    """A defaultdict which waits for key access to provide default

    Same as a defaultdict, but the initiasing method takes a key
        and provides a value
    """

    method: Any = None

    def __init__(self, method: Any):
        self.method = method
        super().__init__(None)

    def __missing__(self, key):
        result = self.method(key)
        self[key] = result
        return result


class NameSpace(dict):
    """Convert dictionary keys to attributes of self

    >>> assert NameSpace({'fred': 1}).fred == 1
    """

    def __init__(self, *args, **kwargs):
        """>>> assert NameSpace({'fred': 1}).fred == 1"""
        super(NameSpace, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def update(self, other):
        self.__dict__ = data_merge(self.__dict__, other)


class NameSpaces(NameSpace):
    """Convert dictionary keys to attributes of self, recursively

    >>> spaces = NameSpaces({'fred': {'mary': 1}})
    >>> assert spaces.fred.mary == 1
    """

    def __init__(self, thing):
        data = {}
        for key, value in (thing or {}).items():
            data[key] = NameSpaces(value) if isinstance(value, dict) else value
        super(NameSpaces, self).__init__(data)


@dataclass
class SpaceName:
    """Access attributes of a thing like a dict

    >>> class Fred:
    ...     foo = "Hello"
    ...     bar = "World"
    >>> dic = SpaceName(Fred())
    >>> assert f'{dic["foo"]} {dic["bar"]}' == "Hello World"
    """

    proxy: Any

    def __getitem__(self, name):
        return self.getitem(name)

    def getitem(self, name: str):
        try:
            return getattr(self.proxy, name)
        except AttributeError:
            raise KeyError(name)


class SpaceNames(SpaceName):
    """Access attributes of a thing like a dict, recursively

    >>> class Fred:
    ...     foo = "Hello"
    ...     bar = "World"
    >>> fred = Fred()
    >>> fred.fred = Fred()
    >>> dic = SpaceNames(fred)
    >>> assert f'{dic["foo"]} {dic["bar"]}' == "Hello World"
    >>> assert dic['fred']['foo'] == "Hello" == dic['foo']
    """

    def getitem(self, string: str):
        name, *names = string.split(".")
        value = super().getitem(name)
        try:
            return SpaceNames(value).getitem(names)
        except IndexError:
            return value
