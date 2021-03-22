"""Handle config files"""

import yaml

from pysyte.types.dictionaries import NameSpaces


class Config(NameSpaces):
    def __init__(self, data):
        super().__init__(data)


def load(path_to_config):
    with path_to_config.open() as stream:
        data = yaml.safe_load(stream)
        return Config(data)


def dump(data, path_to_config):
    with path_to_config.open("w") as stream:
        yaml.safe_dump(data, stream, explicit_start=True)
