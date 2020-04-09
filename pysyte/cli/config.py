"""Handle configs from program name"""

from pysyte.unix import root

from pysyte.config import xdg

def user(name):
    return xdg.home_config(name)


def machine(name):
    return xdg.etc_config(name)


def all(name):
    return {**machine(name), **user(name)}
