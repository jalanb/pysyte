"""Handle XDG config files as yaml"""

from pysyte.config.types import ConfigPaths
from pysyte.oss import linux 


user = ConfigPaths(linux.xdg_homes())
machine = ConfigPaths(linux.xdg_dirs())


def homes(name):
    return user.configs(name)


def machines(name):
    return machine.configs(name)


def all(name):
    return machines(name) + homes(name)
