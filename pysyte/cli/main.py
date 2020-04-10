"""Handle scripts from the command_line

This module is a simplifying proxy to stdlib's sys.exit()
"""

import os
import sys
import inspect

import stackprinter

from pysyte.cli import arguments
from pysyte.debuggers import DebugExit
from pysyte.cli import config as configuration
from pysyte.types.paths import makepath


def run(
        main_method, add_args=None, post_parse=None,
        usage=None, epilog=None, config=None):
    """Run a main_method from command line, parsing arguments

    if add_args(parser) is given it should add arguments to the parser
    if add_args(make_parser, description, epilog, usage) is given
        it can adjust help texts before making the parser
    if pre_parse() is given then call it instead of sys.argv
    if post_parse(args) is given then it is called with parsed args
        and should return them after any adjustments
    if config is true then configure that, else configure(args.prog)
        read config, as yaml, to data
        call main_method(args, data)
    else
        call main_method(args)
    """
    class Caller:
        def __init__(self):
            self.sys_args = sys.argv
            self.method = main_method
            self.add_args = add_args
            self.module = inspect.getmodule(main_method)
            self.doc = self.module.__doc__
            self.in_main_module = self.module.__name__ == '__main__'
            self.argcount = bool(self.method.__code__.co_argcount)
            self.needs_one_arg = self.argcount == 1
            self.needs_args = bool(self.argcount)
            self.adds_args = bool(self.add_args)

        def arg_parser(self):
            try:
                return self.add_args(
                    arguments.parser, self.doc, usage, epilog)
            except TypeError:
                try:
                    return self.add_args(
                        arguments.parser(self.doc, usage, epilog))
                except TypeError:
                    raise NotImplementedError(
                        'Unknown signature for add_args()')

        @property
        def config_name(self):
            if isinstance(config, str):
                return config
            name = makepath(self.method).name
            return name

        def main(self, argument_handler):
            if config:
                if self.needs_args:
                    argument_handler.add_args()
                config_ = configuration.all(self.config_name)
                return caller.method(self.args, config_)
            if self.needs_args:
                argument_handler.add_args()
                return self.method(self.args)
            return self.method()

    caller = Caller()

    class ArgumentHandler:

        if caller.adds_args:
            def add_args(self):
                parser = caller.arg_parser()
                assert parser  # Dont trust callers' coder to return the parser
                global args  # leave parsed args available from this module
                caller.args = args = parser.parse_args(post_parser=post_parse)
        else:
            def add_args(self):
                assert caller.needs_one_arg
                assert len(caller.args) == 1

        def run(self):
            """Handle expected exceptions"""
            try:
                return caller.main(self)
            except KeyboardInterrupt:
                sys.stderr.write('^c ^C ^c    ^C ^c ^C    ^c ^C ^c\n')
                ctrl_c = 3
                return ctrl_c
            except DebugExit:
                return os.X_OK
            except SystemExit as e:
                return e.code
            except Exception as e:  # pylint: disable=broad-except
                stackprinter.show(e, style='darkbg')

    if caller.in_main_module:
        handler = ArgumentHandler()
        sys.exit(handler.run())


args = {}
