"""Handle arguments from the command line

This module is a simplifying proxy to stdlib's argparse
"""

import argparse
import os
import re
import shlex
import sys
from bdb import BdbQuit
from pprint import pformat
from functools import partial
from typing import Any
from typing import List

import stackprinter

from pysyte.cli.config import load_configs
from pysyte.types.numbers import inty

from pysyte.cli.config import pysyte


def config(arguments):
    return load_configs(arguments.prog)


def extract_strings(names: dict, name: str) -> List[str]:
    try:
        value = names[name]
    except KeyError:
        return []
    if isinstance(value, str):
        return [value]
    try:
        return [_ for _ in value if isinstance(_, str)]
    except TypeError:
        return []


class IntyAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        setattr(namespace, self.dest, inty(value))


class ArgumentsParser(object):
    """Add more attriubtes and methods to an argparse.ArgumentParser"""

    def __init__(self, argparser):
        self.parser = argparser
        self._parsed = None

        self.parse = self.parse_args

        self.string = self.arg = self.add_option
        self.boolean = self.opt = self.true = partial(self.arg, action="store_true")
        self.integer = self.int = partial(self.arg, type=int)
        self.inty = partial(self.arg, action=IntyAction)
        self.strings = partial(self.positional, type=str)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def add_to(self, name=None, group=None, type_=None, default=None, *args, **kwargs):
        args_ = args[:]
        kwargs_ = kwargs.copy()
        name_ = name if name else ""
        group_ = group if group else name_
        kwargs_["default"] = (
            default if default else group_ if group_ else name_ if name_ else None
        )
        args_ = [name_[0], name_] + args
        self.add_option(*args_, **kwargs_)

    def add_option(self, initial, name, *args, **kwargs):
        n = name.lstrip("-")
        i = initial.lstrip("-") or n[0]
        return self.parser.add_argument(f"-{i}", f"--{n}", *args, **kwargs)

        if not initial:
            initial = name[0]
        return self.parser.add_argument(
            f'-{initial.lstrip("-")}', f'--{name.lstrip("-")}', *args, **kwargs
        )

    def optional(self, *args, **kwargs):
        """Add an optional positional arg"""
        return self.parser.add_argument(*args, **kwargs, nargs="?")

    def positional(self, *args, **kwargs):
        """Add optional positional args"""
        return self.parser.add_argument(*args, **kwargs, nargs="*")

    def positionals(self, *args, **kwargs):
        """Add mandatory positional args"""
        return self.parser.add_argument(*args, **kwargs, nargs="+")

    def post_parser(self, args):
        """No-op for specialisation"""
        return args

    def parse_args(self, arguments=None, post_parser=None):
        post_parse = post_parser if post_parser else getattr(self, "post_parser", False)
        parsed_args = self.parser.parse_args(arguments)
        argument_namespace = ArgumentsNamespace(parsed_args)
        post_parser_ = post_parse if post_parse else lambda x: x
        posted_args = post_parser_(argument_namespace)
        self.args = posted_args
        self.args.prog = self.parser.prog
        return self.args

    def parse_string(self, string):
        return self.parse_args(shlex.split(string))


class DescribedParser(ArgumentsParser):
    """An argparse.ArgumentParser with a description, usage and epilog"""

    def __init__(self, description, usage, epilog):
        super().__init__(
            argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description=description,
                usage=usage,
                epilog=epilog,
            )
        )


class ArgumentsNamespace(object):
    def __init__(self, result):
        self._result = result

    def __repr__(self):
        """Show args nicely in cli and debuggers"""
        klass = self.__class__.__qualname__
        cmd = " ".join(sys.argv)
        cmd_ = f"$ {cmd}"
        args = pformat(self.get_args())
        repr_ = "\n".join((klass, cmd_, args))
        return f"<{repr_}>"

    def __getattr__(self, name) -> Any:
        return getattr(self._result, name)

    def get_args(self) -> dict:
        attributes = [a for a in dir(self._result) if a[0] != "_"]
        return {a: getattr(self._result, a) for a in attributes}

    def get_arg(self, name: str) -> Any:
        return getattr(self._result, name, None)

    def get_strings(self, name: str) -> List[str]:
        if not self._result:
            return []
        return extract_strings(self._result.__dict__, name)

    def set_arg(self, name: str, value: Any) -> None:
        setattr(self._result, name, value)


class ArgumentHandler:
    def run(self, caller):
        """Handle expected exceptions"""
        try:
            return caller.main(self)
        except KeyboardInterrupt:
            sys.stderr.write("^c ^C ^c    ^C ^c ^C    ^c ^C ^c\n")
            ctrl_c = 3
            return ctrl_c
        except BdbQuit:
            return os.X_OK
        except SystemExit as e:
            return e.code
        except Exception as e:
            stackprinter.show(e, style=pysyte.stackprinter.style)


def parser(description=None, usage=None, epilog=None):
    """Make a command line argument parser"""

    if usage:
        return DescribedParser(description, usage, epilog)
    lines = (description or "").splitlines()
    regexp = re.compile("^[uU]sage:")
    usages = [_ for _ in lines if regexp.match(_)]
    if usages:
        usage_line = usages.pop()
        usage = usage_line.split(":", 1)[1]
        description = "\n".join([_ for _ in lines if _ != usage_line])
    elif len(lines) > 1 and not lines[1]:
        usage, description = lines[0], "\n".join(lines[2:])
    return DescribedParser(description, usage, epilog)


def test_parser():
    """A parser for testing convenience"""
    return parser("Testing", "Use this from a test", "")


def in_debugger():
    """Whether script is being traced

    A debugger will often set a system trace
    So this functions returns whether one has been set

    Debuggers known to give True
        * pudb
        * PyCharm

    Test runners known to give True
        * nose
        * py.test
        * coverage

    Test runners known to give False
        * doctest
        * unittest
    """
    return bool(sys.gettrace())
