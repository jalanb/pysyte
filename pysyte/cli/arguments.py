"""Handle arguments from the command line

This module is a simplifying proxy to stdlib's argparse
"""

import argparse
import re
import sys
from functools import partial
from itertools import chain

from pysyte.cli.config import user


def config(arguments):
    return user(arguments.prog)

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


class ArgumentsParser(object):
    def __init__(self, description, usage, epilog):
        self.parser = argparse.ArgumentParser(
            description=description, usage=usage, epilog=epilog)
        self._parsed = None

        self.parse = self.parse_args

        self.string = self.arg = self.parser.add_argument
        self.boolean = self.opt = self.true = partial(self.arg, action='store_true')
        self.integer = self.int = partial(self.arg, type=int)
        self.strings = partial(self.arg, type=str, nargs='*')

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def optional(self, *args, **kwargs):
        """Add an optional positional arg"""
        return self.string(*args, **kwargs, nargs='?')

    def positional(self, *args, **kwargs):
        """Add optional positional args"""
        return self.string(*args, **kwargs, nargs='*')

    def positionals(self, *args, **kwargs):
        """Add mandatory positional args"""
        return self.string(*args, **kwargs, nargs='+')

    def parse_args(self, arguments=None, post_parser=None):
        post_parse = post_parser if post_parser else getattr(
            self, 'post_parser', False)
        poster = post_parse if post_parse else lambda x: x
        return poster(ArgumentsNamespace(self.parser.parse_args(arguments)))


class ArgumentsNamespace(object):
    def __init__(self, result):
        self._result = result

    def __getattr__(self, name):
        try:
            super(ArgumentsNamespace, self).__getattr__(name)
        except AttributeError:
            return getattr(self._result, name)

    def get_args(self):
        attributes = [a for a in dir(self._result) if a[0] != '_']
        return {a: getattr(self._result, a) for a in attributes}

    def get_arg(self, name):
        if not self._result:
            return None
        return getattr(self._result, name)

    def get_strings(self, name):
        if not self._result:
            return None
        return extract_strings(self._result.__dict__, name)


def parser(description=None, usage=None, epilog=None):
    """Make a command line argument parser"""

    if usage:
        return ArgumentsParser(description, usage, epilog)
    match = lambda x: re.match('^[uU]sage:', x)
    lines = (description or "").splitlines()
    usages = [l for l in lines if match(l)]
    if usages:
        usage = usages.pop()
        epilog = '\n\n'.join([l for l in lines if l != usage])
    elif len(lines) > 1 and not lines[1]:
        usage, description = lines[0], '\n\n'.join(lines[2:])
    return ArgumentsParser(description, usage, epilog)