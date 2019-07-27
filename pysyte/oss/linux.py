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
                    str(paths.home('.config'))
                )
            )

    CONFIG = Config()


def xdg_config_file(filename):
    """path to that file in $XDG_CONFIG_HOME

    >>> assert xdg_config_file('fred') == os.path.expanduser('~/.config/fred')
    """
    return paths.path(os.path.join(XDG.CONFIG.HOME, filename))


bash_paste = 'xclip -selection clipboard'
bash_copy = 'xclip -selection clipboard -o'
