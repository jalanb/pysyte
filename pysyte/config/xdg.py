"""Handle XDG config files as yaml"""

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
        path = paths.path(string)
        return path.add_missing_ext('yml')

class XdgConfiguration(YamlConfiguration):
    def as_path(self, string):
        path = xdg_config_file(string)
        return super().as_path(path)


class ModuleConfiguration(YamlConfiguration):
    def as_path(self, string):
        path = paths.path(string)
        stem, ext = path.split_ext()
        return string(stem)
