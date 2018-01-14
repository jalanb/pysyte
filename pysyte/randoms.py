import random


def coin():
    return random.choice(('heads', 'tails'))


def flip():
    return random.choice((True, False))
