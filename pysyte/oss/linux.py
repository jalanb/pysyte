"""Linux-specific code"""

import os

from pysyte.types import paths


def xdg_config_home():
    """Find $XDG_CONFIG_HOME from environment

    If not set in enviroment use $HOME/.config
    """
    if 'XDG_CONFIG_HOME' in os.environ:
        return paths.path(os.environ['XDG_CONFIG_HOME'])
    return paths.home('.config')


def xdg_config_file(filename):
    """path to that file in $XDG_CONFIG_HOME

    >>> assert xdg_config_file('fred') == os.path.expanduser('~/.config/fred')
    """
    return paths.path(os.path.join(xdg_config_home(), filename))


bash_paste = None
bash_copy = None
