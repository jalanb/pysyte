"""Classes for configuration"""

import yaml

from pysyte.types import paths
from pysyte.types.dictionaries import NameSpaces


class YamlConfiguration(NameSpaces):
    """Read a yaml config file and parse it to attributes"""
    def __init__(self, string):
        if not string:
            super().__init__({})
        else:
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
        return str(path.extend_by('yaml'))


class IniConfiguration(object):
    pass
