"""Handle config files for pysyte

Some prep work
>>> from pysyte.types.paths import path
>>> pysyte_package = path(__file__).parent.parent
>>> pysyte_config = pysyte_package / 'pysyte.yaml'

Now we can load the yaml config file
>>> pysyte = load(pysyte_config)
>>> assert pysyte.stackprinter.style == 'darkbg'

Or we could load the git global config file
>>> git = load(path('~/.gitconfig'))
>>> assert git.user.name == "J Alan Brogan"

Also handles ini, json, toml

Special function for git, which reads both global and local configs

>>> git = load_git()
>>> assert git.user.name == "J Alan Brogan"
>>> assert 'git' in git.remote.url or 'local' in git.remote.url

Later on you may need to dump your data back to the file

>>> assert dump(pysyte, pysyte_config)
"""
import json
import tomllib
from configparser import ConfigParser

import yaml

from pysyte.types.dictionaries import NameSpaces
from pysyte.types.paths import FilePath
from pysyte.types.paths import path


class Config(NameSpaces):
    def __init__(self, data):
        super().__init__(data)


home_gitconfig = path('~/.gitconfig')

def load_git() -> Config:
    """load gloabl and local git config

    >>> git = load_git()

    Has global values
    >>> assert git.user.name == 'J Alan Brogan'

    And local ones (if '.git/config' is present)
    >>> assert 'git' in git.remote.url
    """
    home = load(home_gitconfig)
    here = load(path('.git/config'))
    here['remote'] = here.get('remote "origin"', NameSpaces({}))
    if here:
        home.update(here)
    return home


def load(path_to_config: FilePath) -> Config:
    """load config data from that path

    >>> pysyte_package = path(__file__).parent.parent
    >>> pysyte_config = pysyte_package / 'pysyte.yaml'
    >>> pysyte = load(pysyte_config)
    >>> assert pysyte.stackprinter.style == 'darkbg'
    """
    def path_to_git_config() -> bool:
        if path_to_config.same_path(home_gitconfig):
            return True
        if path_to_config.name == 'config':
            if path_to_config.parent.name == '.git':
                return True
        return False

    def parse_ini_format() -> Config:
        config = ConfigParser(interpolation=None)
        config.read(path_to_config)
        data = {_: dict(config[_]) for _ in config.sections()}
        return Config(data)

    def parse_loader(loader: Callable, mode:str = "") -> Config:
        with path_to_config.open(mode or 'r') as stream:
            data = loader(stream)
            return Config(data)

    if path_to_config.ext in ('.yml', '.yaml'):
        return parse_loader(yaml.safe_load)
    if path_to_config.ext in ('.ini', '.conf') or path_to_git_config():
        return parse_ini_format()
    if path_to_config.ext == '.json':
        return parse_loader(json.load)
    if path_to_config.ext == '.toml':
        return parse_loader(tomlib.load, 'rb')
    return Config({})


def dump(data: Config, path_to_config: FilePath):
    with path_to_config.open("w") as stream:
        yaml.safe_dump(dict(data), stream, explicit_start=True)
