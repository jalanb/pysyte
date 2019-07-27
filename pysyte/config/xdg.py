"""Handle XDG config files as yaml"""

from functools import partial

import yaml

from pysyte.types import paths
from pysyte.types.dictionaries import RecursiveDictionaryAttributes
from pysyte.oss.linux import xdg_config_file


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

class ModuleConfiguration(YamlConfiguration):
    def as_path(self, string):
        path = paths.path(string)
        stem, ext = path.split_ext()
        return string(stem)


class IniConfiguration(object):
    pass


def xdg_config(string):
    stem = xdg_config_file(string)
    known_types = {
        'yml': YamlConfiguration,
        'yaml': YamlConfiguration,
        'ini': IniConfiguration,
    }
    for ext, type_ in known_types.items():
        extended = stem.add_missing_ext(ext)
        if extended.isfile():
            return type_(stem)
