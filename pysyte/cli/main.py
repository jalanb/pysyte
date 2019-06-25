import os

import stackprinter

import .arguments
from ..debuggers import DebugExit

_exit_ok = os.EX_OK
_exit_fail = not _exit_ok

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


def run_main(main, args):
    def inner_main():
        args = parser.parse_args()
        return main(args)

    parser = arguments.parser(args.__module__.__doc__)
    args(parser)
    sys.exit(call_main(inner_main))

