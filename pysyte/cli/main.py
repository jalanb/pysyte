"""Handle scripts from the command_line

This module is a simplifying proxy to stdlib's sys.exit()
"""

import inspect
import os
import sys

import stackprinter

from pysyte.cli import arguments
from pysyte.debuggers import DebugExit


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


def run(main_method, add_args=None, post_parse=None):
    """Run a main_method from command line, parsing arguments

    if add_args(parser) is given it should add arguments to the parser
    if post_parse(args) is given then it is called with parsed args
        if it returns the args they will be used
    Then call:
        main_method(args)
    """

    module = inspect.getmodule(main_method)
    if not add_args:
        main = main_method
        assert not main_method.__code__.co_argcount
    else:
        def main():
            args = parser.parse_args()
            if post_parse:
                parsed = post_parse(args)
                if parsed:
                    args = parsed
            return main_method(args)

        parser = arguments.parser(module.__doc__)
        add_args(parser)

    if module.__name__ == '__main__':
        sys.exit(try_main(main))
