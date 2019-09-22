"""Handle different OS platforms"""
import platform as python_platform
import importlib

from pysyte import oss
from pysyte.bash import cmnds

name = python_platform.system().lower()
platform = importlib.import_module(f'pysyte.oss.{name}', oss)


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
