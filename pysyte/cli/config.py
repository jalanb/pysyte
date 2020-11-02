"""Handle configs from program name"""

from pysyte.config import xdg
from pysyte.config.types import ConfigPaths
from pysyte.types.paths import home
from pysyte.types.paths import path


user = xdg.user.append(home())
machine = xdg.machine.append(path('/etc'))

config_paths = ConfigPaths(machine.paths + user.paths)

pysyte = config_paths.config('pysyte')
