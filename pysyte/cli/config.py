"""Handle configs from program name"""

from typing import Optional
from typing import List

from pysyte import __file__ as path_to_pysyte
from pysyte.oss import linux
from pysyte.config.types import ConfigPaths
from pysyte.types.dictionaries import NameSpaces
from pysyte.types.paths import DirectPath
from pysyte.types.paths import path


def _common_config_dirs(extras: List[DirectPath]) -> List[DirectPath]:
    """Build a list of common config dirs

    Try each of the following directories
        include them if they exist on this machine
        exclude any duplicates
    And in the following order

    /etc/, $XDG_CONFIG_DIRS, ~/.config, $XDG_CONFIG_HOME
        then any extras specified as args
    """

    def add_dir(value: str):
        path_ = path(value)
        if not path_:
            return
        expanded = path_.expand()
        if expanded in configs:
            return
        if expanded.isdir():
            configs.append(expanded)
        elif expanded.isfile():
            configs.append(expanded.parent)

    configs: List[DirectPath] = []
    add_dir("/etc")
    for path_ in linux.xdg_dirs():
        add_dir(path_)
    add_dir("~/.config")
    add_dir(linux.xdg_home())
    for path_ in extras or []:
        add_dir(path_)
    return configs


def load_configs(name: str, extras: Optional[list] = None) -> NameSpaces:
    """Load all config files with that name from common config dirs"""
    config_paths = ConfigPaths(_common_config_dirs(extras or []))
    return config_paths.load(name)


pysyte = load_configs("pysyte", [path(path_to_pysyte)])
