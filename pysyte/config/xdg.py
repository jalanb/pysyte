"""Handle XDG config files as yaml"""

from pysyte.oss import linux


user = [_.expand() for _ in linux.xdg_homes() if _]
machine = [_.expand() for _ in linux.xdg_dirs() if _]
