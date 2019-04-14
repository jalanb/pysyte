#! /usr/bin/env python

import argparse
from functools import partial


def parser(help_text):
    """Parse out command line arguments"""

    class ArgParser(object):

        def __init__(self, argument_parser):
            self.parser = argument_parser
            self.parse = self.parse_args = self.parser.parse_args

            self.arg = self.parser.add_argument
            self.true = partial(self.arg, action='store_true')
            self.int = partial(self.arg, type=int)

        def strings(self, name, help, many='*'):
            self.arg(name, metavar=name, help=help, type=str, nargs=many)

        args = strings

        def answer(self, answers=None):
            yes_no = {
                'n': ('-n', '--no', 'Answer no'),
                'y': ('-y', '--yes', 'Answer yes'),
            }
            options = yes_no
            options.update(answers)
            [self.true(options[o]) for o in options]

    return ArgParser(
        argparse.ArgumentParser(description=help_text.splitlines()[0]))
