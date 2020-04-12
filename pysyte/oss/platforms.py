"""Handle different OS platforms"""
import platform as python_platform
import importlib

from pysyte import oss
from pysyte.bash import shell

name = python_platform.system().lower()
platform = importlib.import_module(f'pysyte.oss.{name}', oss)


def put_clipboard_data(data):
    try:
        shell.run(platform.bash_copy, input=data)
    except shell.BashError:
        pass


def get_clipboard_data():
    try:
        return shell.run(platform.bash_paste)
    except shell.BashError:
        return ''
