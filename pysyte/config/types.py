"""Classes for configuration"""

from dataclasses import dataclass

from pysyte.types import paths
from pysyte.types.dictionaries import NameSpaces
from pysyte.types.paths import FileTypes


class Configuration(NameSpaces):
    """We'll use a new name now"""


class PysyteConfiguration(Configuration):
    def __init__(self, stem):
        self.exts = []
        self.path = self.as_path(stem)
        self.data = self.load(self.path) if self.path else {}
        super().__init__(self.data)

    def as_path(self, stem):
        stem_ = paths.path(stem)
        paths_ = [stem_.extend_by(_) for _ in self.exts]
        for path in paths_:
            for ext in self.exts:
                path = path.extend_by(ext)
                if path.isfile():
                    return path
        return paths.path(None)


class YamlConfiguration(PysyteConfiguration):
    """Read a yaml config file and parse it to attributes"""

    def __init__(self, module):
        self.exts = ["yml", "yaml"]
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
            for file in list(self.file_types.files(stem)):
                if file:
                    yield file

    def load(self, name):
        result = {}
        for config in self.configs(name):
            result.update(config)
        return Configuration(result)
