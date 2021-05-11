"""Handle different OS platforms"""
import platform as python_platform
import importlib
from subprocess import run

name = python_platform.system().lower()
platform = importlib.import_module(f"pysyte.oss.{name}", "pysyte.oss")


def put_clipboard_data(data):
    run(platform.bash_copy, encoding="utf-8", input=data)


def get_clipboard_data():
    result = run(platform.bash_paste, capture_output=True, encoding="utf-8")
    return result.stdout
