#! /usr/bin/env python

import argparse
from functools import partial


def parser(text):
    """Parse out command line arguments"""
    arg_parser = argparse.ArgumentParser(description=text.splitlines()[0])

    class ArgParser(object):
        add = arg_parser.add_argument
        true = partial(add, action='store_true')
        num = partial(add, type=int)
        parse_args = arg_parser.parse_args
        parse = parse_args

        def strings(self, name, help, many='*'):
            self.add(name, metavar=name, help=help, type=str, nargs=many)

    return ArgParser()
