"""Linux-specific code"""

import os

from pysyte.types import paths

class XDG:
    class Config:
        @property
        def HOME(self):
            return paths.path(
                os.environ.get(
                    'XDG_CONFIG_HOME',
                    str(paths.home() / '.config')
                )
            )

    CONFIG = Config()


def xdg_home():
    """path to $XDG_CONFIG_HOME

    >>> assert xdg_home_config() == os.path.expanduser('~/.config')
    """
    return paths.path(XDG.CONFIG.HOME)

def xdg_home_config(filename):
    """path to that file in $XDG_CONFIG_HOME

    >>> assert xdg_home_config('fred') == os.path.expanduser('~/.config/fred')
    """
    return xdg_home() / filename


bash_paste = 'xclip -selection clipboard'
bash_copy = 'xclip -selection clipboard -o'
