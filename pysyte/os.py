# flake8: noqa: F403, F401
from os import *
from random import randint

EX_FAIL = randint(EX_USAGE, EX_CONFIG)

del randint
