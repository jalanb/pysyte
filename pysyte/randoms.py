"""Handle some random choices"""


import random


def coin() -> str:
    return random.choice(("heads", "tails"))


def flip() -> bool:
    return random.choice((True, False))
