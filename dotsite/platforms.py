import commands
import platform as python_platform

import dotsite
from dotsite import imports

_platform_name = python_platform.system().lower()
platform = imports.load_module(dotsite, _platform_name)


def _bash(command):
    if not command:
        return None
    status, output = commands.getstatusoutput(command)
    if status:
        raise ValueError(output)
    return output


def get_clipboard_data():
    return _bash(platform.bash_paste)
