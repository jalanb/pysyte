"""Classes for configuration"""
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from rich import inspect
from yamlreader import yaml_load

from pysyte.types.trees import paths
from pysyte.types.trees.files import FilePath
from pysyte.types.dictionaries import NameSpaces
from pysyte.types.file_types import FileTypes


class Configuration(NameSpaces):
    """We'll use a new name now"""


class ConfigFile(ABC):
    """An abstract base class for configuration files.

    E.g.
    >>> this = ConfigFile(Configuration)
    >>> assert "ConfigFile" in file.classes
    """

    try:
        file: paths.path = ""
    except AttributeError as e:
        values = f"""
             File: {paths.__file__}
             dir: {dir(paths)}
             vars: {vars(paths)}
             inspect: {inspect(paths, all=True)}
        """
        raise ValueError(values) from e

    def __init__(self, path: paths.StringPath):
        super().__init__(self.load())

    def load(self):
        raise NotImplementedError


class ConfigFileType(Configuration):
    types: List[str] = []

    def __init__(self, stem: str):
        self.path = self.path(stem)
        if self.path:
            super().__init__(self.path)

    def path(self, stem: str):
        path, *paths = self.paths(stem)
        if paths:
            raise NotImplementedError
        return path

    def paths(self, stem_: str) -> List[paths.StringPath]:
        stem = paths.path(stem_)
        files = [stem.extend_by(_) for _ in self.types]
        return [_ for _ in files if _ and _.isfile()]


class YamlConfiguration(ConfigFileType):
    """Read a yaml config file and parse it to attributes"""

    types = ["yml", "yaml"]

    def __init__(self, module):
        super().__init__(paths.path(module))

    def load(self, path):
        return yaml_load(path)

    def extensions(self):
        return ("yml", "yaml")


class ModuleConfiguration(YamlConfiguration):
    def __init__(self, module):
        super().__init__(paths.path(module))


@dataclass
class ConfigPathsData:
    paths: list


class ConfigPaths(ConfigPathsData):
    def __init__(self, paths_):
        super().__init__([_ for _ in paths_ if _])
        self.file_types = FileTypes(
            [
                (YamlConfiguration, "yml"),
                (YamlConfiguration, "yaml"),
            ]
        )

    def configs(self, name):
        for path_ in self.paths:
            stem = path_ / name
            for typed in list(self.file_types.typed(stem)):
                if typed:
                    yield typed

    def files(self, name):
        for path_ in self.paths:
            stem = path_ / name
            for file in list(self.file_types.extend(stem)):
                if file:
                    yield file

    def load(self, name):
        result = {}
        for config in self.configs(name):
            result.update(config)
        return Configuration(result)
