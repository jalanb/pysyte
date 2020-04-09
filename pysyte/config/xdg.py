"""Handle XDG config files as yaml"""

from functools import partial

from pysyte.config.types import YamlConfiguration
from pysyte.config.types import YamlyConfiguration
from pysyte.config.types import IniConfiguration
from pysyte.iteration import first
from pysyte.oss.linux import xdg_home
from pysyte.types.paths import path


def home_config(string):
    return first_config(string, [xdg_home()])


def any_config_type(string):
    for path_, type_ in config_types(string):
        if path_.isfile():
            return type_(path_)
    return {}


def first_config(string, paths):
    return first(any_config_type(_ / string) for _ in paths)


def any_config(string):
    return first_config(string, (xdg_home(), path('/etc')))


def all_configs(string):
    return (any_config_type(_ / string) for _ in (path('/etc'), xdg_home()) if _)


def etc_config(string):
    return any_config_type(path('/etc') / string)


def config_types(stem):
    config_exts = (
        ('yml', YamlConfiguration),
        ('yaml', YamlConfiguration),
        ('yamly', YamlyConfiguration),
        ('ini', IniConfiguration),
    )
    return [(stem.add_missing_ext(e), t) for e, t in config_exts]
