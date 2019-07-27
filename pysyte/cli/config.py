"""Handle configs from program name"""

from pysyte.config.xdg import xdg_config

def user(name):
    return xdg_config(name)
