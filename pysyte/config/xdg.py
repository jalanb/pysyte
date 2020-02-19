"""Handle XDG config files as yaml"""

from functools import partial

import yaml

from pysyte.iteration import first
from pysyte.types import paths
from pysyte.types.dictionaries import RecursiveDictionaryAttributes
from pysyte.oss.linux import xdg_home


class YamlConfiguration(RecursiveDictionaryAttributes):
    """Read a yaml config file and parse it to attributes"""
    def __init__(self, string):
        path = self.as_path(string)
        with open(path) as stream:
            data = yaml.safe_load(stream)
            super(YamlConfiguration, self).__init__(data)

    def as_path(self, string):
        stem = paths.path(string)
        yml = stem.add_missing_ext('yml')
        if yml.isfile():
            return yml
        yaml = stem.add_missing_ext('yaml')
        if yaml.isfile():
            return yaml

class YamlyConfiguration(YamlConfiguration):
    pass


class ModuleConfiguration(YamlConfiguration):
    def as_path(self, string):
        path = paths.path(string)
        stem, ext = path.split_ext()
        return string(stem)


class IniConfiguration(object):
    pass


def home_config(string):
    return first_config((xdg_home / string))


def any_config_type(string):
    for path_, type_ in config_types(string):
        if path_.isfile():
            return type_(path_)
    return None


def first_config(string, paths):
    return first(any_config_type(_ / string) for _ in paths)


def any_config(string):
    return first_config(string, (xdg_home(), root.etc))


def all_configs(string):
    return (any_config_type(_ / string) for _ in (root.etc, xdg_home()) if _)


def etc_config(string):
    return any_config_type(root.etc / string)


def config_types(string):
    config_exts = (
        ('yml', YamlConfiguration),
        ('yaml', YamlConfiguration),
        ('yamly', YamlyConfiguration),
        ('ini', IniConfiguration),
    )
    return [(stem.add_missing_ext(e), t) for e, t in config_exts]


