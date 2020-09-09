"""Linux-specific code"""

import os

from pysyte.types import paths


def xdg_home():
    """path to $XDG_CONFIG_HOME

    >>> assert xdg_home() == os.path.expanduser('~/.config')
    """
    return paths.environ_path('XDG_CONFIG_HOME', '~/.config')


def xdg_home_config(filename):
    """path to that file in $XDG_CONFIG_HOME

    >>> assert xdg_home_config('fred') == os.path.expanduser('~/.config/fred')
    """
    return xdg_home() / filename


def xdg_dirs():
    """paths in $XDG_CONFIG_DIRS"""
    return paths.environ_paths('XDG_CONFIG_DIRS')


def xdg_homes():
    return [xdg_home()]


bash_paste = 'xclip -selection clipboard'
bash_copy = 'xclip -selection clipboard -o'
