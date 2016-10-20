# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
import commands
import platform as python_platform

import dotsite

_platform_name = python_platform.system().lower()
platform = dotsite.imports.load_module(dotsite, _platform_name)


def _bash(command):
    status, output = commands.getstatusoutput(command)
    if status:
        raise ValueError(output)
    return output


def get_clipboard_data():
    return _bash(platform.bash_paste)
