"""Handle arguments from the command line

This module is a simplifying proxy to stdlib's argparse
"""

import argparse
import sys
from functools import partial
from itertools import chain


def extract_strings(names, name):
    result = {}
    try:
        value = names[name]
    except KeyError:
        return []
    if isinstance(value, str):
        return [value]
    try:
        return [v for v in value if isinstance(v, str)]
    except TypeError:
        return []


def parser(description=None, usage=None):
    """Make a command line argument parser"""

    class ArgumentsNamespace(object):
        def __init__(self, result):
            self._result = result

        def __getattr__(self, name):
            try:
                super(ArgumentsNamespace, self).__getattr__(name)
            except AttributeError:
                return getattr(self._result, name)

        def get_arg(self, name):
            if not self._result:
                return None
            return getattr(self._result, name)

        def get_strings(self, name):
            if not self._result:
                return None
            return extract_strings(self._result.__dict__, name)

    class ArgumentsParser(object):
        def __init__(self, usage, epilog):
            self.parser = argparse.ArgumentParser(usage=usage, epilog=epilog)
            self._parsed = None

            self.parse = self.parse_args

            self.string = self.arg = self.parser.add_argument
            self.boolean = self.opt = self.true = partial(self.arg, action='store_true')
            self.integer = self.int = partial(self.arg, type=int)
            self.strings = partial(self.arg, type=str, nargs='*')

        def __repr__(self):
            return f'<{self.__class__.__name__}>'

        def positional(self, *args, **kwargs):
            """Add optional positional args"""
            return self.string(*args, **kwargs, nargs='*')

        def positionals(self, *args, **kwargs):
            """Add mandatory positional args"""
            return self.string(*args, **kwargs, nargs='+')

        def parse_args(self, args=None):
            return ArgumentsNamespace(self.parser.parse_args(args))


    lines = description.splitlines()
    epilog = None
    if not usage:
        if len(lines) > 1 and not lines[1]:
            usage, epilog = lines[0], '\n\n'.join(lines[2:])
    else:
        usage = description = lines[0]
    return ArgumentsParser(usage, epilog)
