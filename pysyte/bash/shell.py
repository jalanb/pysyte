"""Handle bash commands for pysyte"""

import os
import psutil

from contextlib import contextmanager
from subprocess import getstatusoutput
from typing import List

from boltons.setutils import IndexedSet


class BashError(ValueError):
    pass


_working_dirs: List[str] = [""]
_paths: List[str] = []


def cd(path: str):
    if _working_dirs[0] == path:
        return
    assert os.path.isdir(path)
    _working_dirs[0] = path


@contextmanager
def pushd(path):
    assert os.path.isdir(path)
    _working_dirs.insert(0, path)
    yield
    del _working_dirs[0]


def _get_path() -> str:
    """Guarantee that /usr/local/bin, /usr/bin, /bin are in PATH"""
    if _paths:
        return _paths[0]
    environ_paths = IndexedSet(os.environ["PATH"].split(":"))
    minimal_paths = IndexedSet(["/usr/local/bin", "/usr/bin", "/bin"])
    all_paths = environ_paths | minimal_paths
    _paths.append(":".join(all_paths))
    return _paths[0]


def run(command: str) -> str:
    path_command = f"PATH={_get_path()} {command}"
    if _working_dirs[0]:
        run_command = f"(cd {_working_dirs[0]}; {path_command})"
    else:
        run_command = path_command
    status, output = getstatusoutput(run_command)
    if status:
        raise BashError(f"{run_command}\n{output}")
    return output


def parent_command() -> str:
    """Find the parent of this process

    Returns: the command line of the parent process
    """
    parent_pid = os.getppid()
    parent = psutil.Process(parent_pid)
    return parent.cmdline()
