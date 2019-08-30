"""Handle scripts from the command_line

This module is a simplifying proxy to stdlib's sys.exit()
"""

import inspect
import os
import sys

import stackprinter

from pysyte.cli import arguments
from pysyte.debuggers import DebugExit
from pysyte.cli.config import user


def try_main(main):
    """Handle expected exceptions"""
    try:
        return os.EX_OK if main() else os.X_OK
    except KeyboardInterrupt as e:
        sys.stderr.write('^c ^C ^c    ^C ^c ^C    ^c ^C ^c\n')
        ctrl_c = 3
        return ctrl_c
    except DebugExit:
        return os.X_OK
    except SystemExit as e:
        return e.code
    except Exception as e:  # pylint: disable=broad-except
        stackprinter.show(e, style='darkbg')


def run(main_method, add_args=None, post_parse=None, config=None, usage=None, epilog=None):
    """Run a main_method from command line, parsing arguments

    if add_args(parser) is given it should add arguments to the parser
    if post_parse(args) is given then it is called with parsed args
        if it returns the args they will be used
    if config is true then
        is config is not a name then set config to program name
        read ~/.config/name.yml to data
        call main_method(args, data)
    Else
        call main_method(args)
    """

    module = inspect.getmodule(main_method)
    if not main_method.__code__.co_argcount:
        main = main_method
    else:
        def main():
            args = parser.parse_args(post_parser=post_parse)
            if config:
                config_name = config if isinstance(config, str) else args.prog
                try:
                    configuration = user(config_name)
                    return main_method(args, configuration)
                except FileNotFoundError:
                    pass
            return main_method(args)

        parser = arguments.parser(module.__doc__, usage, epilog)
        if add_args:
            added_parser = add_args(parser)
            parser = added_parser if added_parser else parser
        else:
            if main_method.__code__.co_argcount == 1:
                def main():
                    return main_method(sys.argv)
            else:
                raise ValueError('Too many arguments to main')

    if module.__name__ == '__main__':
        sys.exit(try_main(main))
