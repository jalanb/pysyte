"""Handle bash commands for the tools package"""

import logging
import os
from contextlib import contextmanager

from pysyte.bash.cmnds import getstatusoutput

logger = logging.getLogger(__name__)


class BashError(ValueError):
    pass


_working_dirs = ['']
_displays = [False]
_path = []


def cd(path):
    if _working_dirs[0] == path:
        return
    logger.info('$ PWD=%s', path)
    _working_dirs[0] = path


@contextmanager
def pushd(path):
    _working_dirs.insert(0, path)
    yield
    del _working_dirs[0]


def _get_path():
    """Guarantee that /usr/local/bin and /usr/bin are in PATH"""
    if _path:
        return _path[0]
    environ_paths = set(os.environ['PATH'].split(':'))
    environ_paths.add('/usr/local/bin')
    environ_paths.add('/usr/bin')
    _path.append(':'.join(environ_paths))
    logger.debug('PATH = %s', _path[-1])
    return _path[0]


def run(command):
    path_command = f'PATH={_get_path()} {command}'
    if _working_dirs[0]:
        run_command = f'(cd {_working_dirs[0]}; {path_command}'
        logger.info('$ (cd %s; %s)', _working_dirs[0], path_command)
    else:
        run_command = path_command
        logger.info('$ %s', command)
    status, output = getstatusoutput(run_command)
    if status:
        logger.error('\n%s', output)
        raise BashError(output)
    elif output:
        logger.info('\n%s', output)
    return output


def set_verbosity(display):
    _displays[0] = display


def full_path(path):
    """Get the real path, expanding links and bashisms"""
    return os.path.realpath(os.path.expanduser(os.path.expandvars(path)))
