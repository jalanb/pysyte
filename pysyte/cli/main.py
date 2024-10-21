"""Run scripts from the command_line

This module was a simplifying proxy to stdlib's sys.exit()
    but it's grown since then
"""

import sys
from dataclasses import dataclass
from typing import Optional

from pysyte.cli import app
from pysyte.cli import arguments
from pysyte.cli.config import load_configs
from pysyte.types.methods import Callable
from pysyte.types.methods import Method
from pysyte.types.paths import makepath


class MainMethod(Method):
    """A method that can be called from the command line"""
    def __init__(self, method):
        super().__init__(method)
        self.in_main_module = self.module.__name__ == "__main__"
        self.needs_args = self.argcount > 0
        self.needs_one_arg = self.argcount == 1

    @property
    def doc(self) -> str:
        for doc in (super().doc, self.module.__doc__):
            if doc:
                return doc
        return ""


ArgumentsParsers = Callable[[arguments.ArgumentsParser], arguments.ArgumentsParser]


@dataclass
class CallerData:
    method: MainMethod
    add_args: Optional[ArgumentsParsers]


def exit(main: Callable):
    """Exit to shell with error"""
    app.exit(main)


def run(
    main_method: Callable,
    add_args: Optional[ArgumentsParsers] = None,
    post_parse: Optional[Callable] = None,
    usage: Optional[str] = None,
    epilog: Optional[str] = None,
    config_name: Optional[str] = None,
):
    """Run a main_method from command line, parsing arguments

    if add_args(parser) is given it should call parser.add_arg()
        See ArgumentsParser.add_arg(), etc
    if pre_parse() is given then call it instead of sys.argv
    if post_parse(args) is given then it is called with parsed args
        and should return them after any adjustments
        if config_name is given:
            if it is a string then find configs for that
            otherwise use the main_method's script's name
        read config_name, as yaml, to data
        call main_method(args, data)
    else
        call main_method(args)
    """

    class Caller(CallerData):
        def arg_parser(self):
            try:
                parser_ = arguments.parser()
                return self.add_args(parser_)
            except TypeError:
                raise NotImplementedError("Unknown signature for add_args()")

        def parse_args(self):
            if self.add_args:
                parser = self.arg_parser()
                assert parser  # Dont trust callers' coder to return the parser
                return parser.parse_args(post_parser=post_parse)
            assert self.method.needs_one_arg
            return sys.argv[1:]

        def config_name(self, name):
            if not isinstance(name, str):
                return makepath(self.method).name
            p = makepath(name)
            return p.name if p else name

        def config(self):
            return load_configs(self.config_name(config_name))

        def main(self, argument_handler):
            if self.method.needs_args:
                self.args = self.parse_args()
            if config_name:
                return self.method(self.args, self.config())
            if self.method.needs_args:
                return self.method(self.args)
            return self.method()

    caller = Caller(MainMethod(main_method), add_args)
    if caller.method.in_main_module:
        handler = arguments.ArgumentHandler()
        app.exit(lambda: handler.run(caller))
