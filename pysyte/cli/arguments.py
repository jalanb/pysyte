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
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=description,
            usage=usage,
            epilog=epilog)
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
        same = lambda x: x
        parsed_args = ArgumentsNamespace(self.parser.parse_args(arguments))
        my_args = getattr(self, 'post_parser', same)(parsed_args)
        program_args = (post_parser if post_parser else same)(my_args)
        self.args = program_args
        program_args .prog = self.parser.prog
        return program_args


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
    lines = (description or "").splitlines()
    regexp = re.compile('^[uU]sage:')
    usages = [l for l in lines if regexp.match(l)]
    if usages:
        usage_line = usages.pop()
        usage = usage_line.split(':', 1)[1]
        description = '\n'.join([l for l in lines if l != usage_line])
    elif len(lines) > 1 and not lines[1]:
        usage, description = lines[0], '\n'.join(lines[2:])
    return ArgumentsParser(description, usage, epilog)
