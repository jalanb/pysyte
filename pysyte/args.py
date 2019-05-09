"""Handle arguments from the command line"""

import argparse
import os
import sys
from functools import partial
from itertools import chain

_exit_ok = os.EX_OK
_exit_fail = not _exit_ok

import stackprinter

from pysyte.debuggers import DebugExit


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
    """Parse out command line arguments"""

    class ArgNamespace(object):
        def __init__(self, result):
            self._result = result

        def __getattr__(self, name):
            try:
                super(ArgNamespace, self).__getattr__(name)
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

    class ArgParser(object):
        def __init__(self, argument_parser):
            self.parser = argument_parser
            self.parse = self.parse_args
            self._parsed = None

            self.arg = self.parser.add_argument
            self.opt = self.true = partial(self.arg, action='store_true')
            self.int = partial(self.arg, type=int)

        def __repr__(self):
            return f'<{self.__class__.__name__}>'

        def parse_args(self, args=None):
            return ArgNamespace(self.parser.parse_args(args))

        def sub(self, name, help=''):
            return self.arg(name, metavar=name, help=help, type=str)

        def args(self, name, help='', many='*'):
            return self.arg(name, metavar=name, help=help, type=str, nargs=many)

    lines = description.splitlines()
    if not usage:
        if len(lines) > 1 and not lines[1]:
            usage, epilog = lines[0], '\n\n'.join(lines[2:])
    else:
        usage = description = lines[0]
        epilog = None
    return ArgParser(
        argparse.ArgumentParser(usage=description))


def call_main(main):

    try:
        return _exit_ok if main() else _exit_fail
    except SystemExit as e:
        return e.code
    except KeyboardInterrupt as e:
        ctrl_c = 3
        return ctrl_c
    except DebugExit:
        return _exit_fail
    except Exception as e:  # pylint: disable=broad-except
        stackprinter.show(e, style='darkbg')


def run_main(main, add_args):
    def inner_main():
        args = parser_.parse_args()
        return main(args)

    parser_ = parser(add_args.__module__.__doc__)
    add_args(parser_)
    sys.exit(call_main(inner_main))
