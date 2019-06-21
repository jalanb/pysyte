
from .arguments import Arguments

def add(args):
    arguments = Arguments(args)
    if '-m' not in arguments:
        arguments.add(False, ('-m', '--man'))
