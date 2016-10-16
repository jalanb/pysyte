from __future__ import print_function
import os
import sys
import argparse

from dotsite import __version__

_versions = [__version__]
_exit_ok = os.EX_OK


def latest_version():
    return _versions[-1]


def version(args):
    print('%s %s' % (args, latest_version()))
    raise SystemExit


def parse_args(add_args):
    """Parse out command line arguments"""

    def run_args(args):
        """Run any global methods eponymous with args"""
        valuable_args = {k for k, v in args.__dict__.items() if v}
        arg_methods = {globals()[a] for a in valuable_args if a in globals()}
        if not arg_methods:
            return
        for method in arg_methods:
            method(args)
        raise SystemExit(_exit_ok)

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser = add_args(parser)
    parser.add_argument('-v', '--version', action='store_true',
                        help='Show version [default: %s]' % __version__)
    # parser.add_argument('-q', '--quiet', action='store_true',
    # help='Do not show stdout')
    # parser.add_argument('-Q', '--quiet_errors', action='store_true',
    # help='Do not show stderr')
    args = parser.parse_args()
    run_args(args)
    return args


# pylint: disable=redefined-outer-name
def main(method, add_args, version=None, error_stream=sys.stderr):
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
        args = parse_args(add_args)
        return _exit_ok if method(args) else not _exit_ok
    except KeyboardInterrupt as e:
        ctrl_c = 3
        return ctrl_c
    except SystemExit as e:
        return e.code
    except Exception, e:  # pylint: disable=broad-except
        if int(latest_version().split('.')[0]) < 1:
            raise
        if error_stream:
            print(e, file=error_stream)
        return not _exit_ok
    return _exit_ok
