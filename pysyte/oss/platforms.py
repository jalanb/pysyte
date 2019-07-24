"""Handle different OS platforms"""
import platform as python_platform

from pysyte import imports
from pysyte import oss
from pysyte.bash import cmnds

_platform_name = python_platform.system().lower()
platform = imports.load_module(oss, _platform_name)


def put_clipboard_data(data):
    try:
        cmnds.run(platform.bash_copy, input=data)
    except cmnds.CommandError:
        pass


def get_clipboard_data():
    try:
        return cmnds.run(platform.bash_paste)
    except cmnds.CommandError:
        return ''
