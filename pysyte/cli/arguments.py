"""Handle arguments from the command line

This module is a simplifying proxy to stdlib's argparse
"""

import argparse
import re
import sys
from functools import partial
from itertools import chain

from pysyte.cli.config import user
from pysyte.types.numbers import inty


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

class IntyAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        inty_values = inty(values)
        raise TypeError(self.type)
        setattr(namespace, self.dest, inty_values)


class ArgumentsParser(object):
    def __init__(self, description, usage, epilog):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=description,
            usage=usage,
            epilog=epilog)
        self._parsed = None

        self.parse = self.parse_args

        self.string = self.arg = self.add_argument
        self.boolean = self.opt = self.true = partial(self.arg, action='store_true')
        self.integer = self.int = partial(self.arg, type=int)
        self.inty = partial(self.arg, action=IntyAction)
        self.strings = partial(self.positional, type=str)

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def add_to(self, name=None, group=None, type_=None, default=None, *args, **kwargs):
        args_= args[:]
        kwargs_ = kwargs.copy()
        name_ = name if name else ""
        group_ = group if group else name_
        kwargs_['default'] = default if default else group_ if group_ else name_ if name_ else None
        args_ = [name_] + args
        self.add_argument(*args_, **kwargs_)

    def add_argument(self, *args, **kwargs):
        args_, name, i = args[:], '', 0
        arg, args_ = args_[0], args_[1:]
        if arg[0] == '-':
            i = 2 if arg[1] == '-' else 1
            name = arg[i:]
        else:
            name = arg
            assert not args_[0].startswith('--'):
        arg = args_[0]
        if arg[0:1] == '--':
            if not name:
                name = arg[2:]
            args_ = args_[1:]
        if name:
            name_option = f'--{name}'
            initial_option = f'-{name[0]}'
            adds = [initial_option, name_option, args_]
        else:
            adds = args_
        self.parser.add_argument(initial_option, name_option, *adds, **kwargs)
        return self
    else:

    def add_argument(self, *args, **kwargs):
        name = ''
        args_ = args[:]
        arg = args_[0]
        if arg[0] == '-':
            initial = arg[1]
            rest = args[1:]
            if args_[1].startswith('--'):
                name = args_[1][2:]
                rest = args[2:]
            self.parser.add_argument(f'-{initial}', f'--{name}', *rest, **kwargs)
        else:
            if args_[1:]:
                assert not args_[1].startswith('--')
            name = args_[0]
            rest = args[1:]
            self.parser.add_argument(f'{name}', *rest, **kwargs)
        return self

    def optional(self, *args, **kwargs):
        """Add an optional positional arg"""
        return self.string(*args, **kwargs, nargs='?')

    def positional(self, *args, **kwargs):
        """Add optional positional args"""
        return self.string(*args, **kwargs, nargs='*')

    def positionals(self, *args, **kwargs):
        """Add mandatory positional args"""
        return self.string(*args, **kwargs, nargs='+')

    def post_parser(self, args):
        """No-op for specialisation"""
        return args

    def parse_args(self, arguments=None, post_parser=None):
        post_parse = post_parser if post_parser else getattr(
            self, 'post_parser', False)
        post_parser_ = post_parse if post_parse else lambda x: x
        parsed_args = self.parser.parse_args(arguments)
        argument_namespace = ArgumentsNamespace(parsed_args)
        posted_args =  post_parser_(argument_namespace)
        self.args = posted_args
        self.args.prog = self.parser.prog
        return self.args


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
