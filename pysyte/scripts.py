"""Framework for a script to be run from a shell"""

import argparse
import os
import sys

from pysyte import __version__
from pysyte.debuggers import DebugExit


_versions = [__version__]
_exit_ok = os.EX_OK
_exit_fail = not _exit_ok

args = None


def latest_version():
    return _versions[-1]


def version():
    print(f'{args} {latest_version()}')
    raise SystemExit


def parse_args(add_args, docstring):
    """Parse out command line arguments"""

    def run_args():
        """Run any global methods eponymous with args"""
        valuable_args = {k for k, v in args.__dict__.items() if v}
        arg_methods = {globals()[a] for a in valuable_args if a in globals()}
        if not arg_methods:
            return
        for method in arg_methods:
            method()
        raise SystemExit(_exit_ok)

    parser = argparse.ArgumentParser(
        description=docstring and docstring.splitlines()[0] or "No docstring")
    result = add_args(parser)
    parser = result if result else parser
    parser.add_argument('-v', '--version', action='store_true',
                        help=f'Show version [default: {__version__}]')
    # parser.add_argument('-q', '--quiet', action='store_true',
    # help='Do not show stdout')
    # parser.add_argument('-Q', '--quiet_errors', action='store_true',
    # help='Do not show stderr')
    global args  # pylint: disable=global-statement
    args = parser.parse_args()
    run_args()
    return args


# pylint: disable=redefined-outer-name
def main(method, add_args, version=None,
         docstring=None, error_stream=sys.stderr):
    """Run the method as a script

    Add a '--version' argument
    Call add_args(parser) to add any more

    Parse sys.argv
    call method(args)
    Catch any exceptions
        exit on SystemExit or KeyboardError
        Others:
            If version is less then 1, reraise them
            Else print them to the error stream
    """
    if version:
        _versions.append(version)
    try:
        args = parse_args(
            add_args,
            docstring and docstring or f'{method.__name__}()')
        return _exit_ok if method(args) else _exit_fail
    except KeyboardInterrupt as e:
        ctrl_c = 3
        return ctrl_c
    except SystemExit as e:
        return e.code
    except DebugExit:
        return _exit_fail
    except Exception as e:  # pylint: disable=broad-except
        if int(latest_version().split('.')[0]) < 1:
            raise
        if error_stream:
            print(e, file=error_stream)
        return _exit_fail
    return _exit_ok
