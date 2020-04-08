"""Linux-specific code"""

import os

from pysyte.types import paths


def xdg_home():
    """path to $XDG_CONFIG_HOME

    >>> assert xdg_home() == os.path.expanduser('~/.config')
    """
    path_to_xdg = os.getenv('XDG_CONFIG_HOME', str(paths.home() / '.config'))
    return paths.path(path_to_xdg)


def xdg_home_config(filename):
    """path to that file in $XDG_CONFIG_HOME

    >>> assert xdg_home_config('fred') == os.path.expanduser('~/.config/fred')
    """
    return xdg_home() / filename


bash_paste = 'xclip -selection clipboard'
bash_copy = 'xclip -selection clipboard -o'
