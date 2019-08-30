import sys
import atexit
from functools import partial

from pysyte import __version__
from pysyte.cli.arguments import ArgumentsParser
from pysyte.types import lines as pylines
from pysyte.bash.shell import run

class FunctionsParser(ArgumentsParser):
    """Add option sets to the parser"""
    def version(self, version_=None):
        self.version = version_ if version_ else __version__
        self.boolean('-v', '--version', help='Show version')

    def lines(self):
        self.boolean('-n', '--numbers', help='Show line numbers')
        self.int('-w', '--width', help='Max width of shown line')

    def post_parser(self, args):
        if args.version and self.version:
            sys.stdout.write(f'{sys.argv[0]} version: {self.version}')
            raise SystemExit
        args.sed = partial(
            pylines.reformat_lines, numbers=args.numbers, width=args.width)
        args.alt_screen = get_alt_screen()
        return args


def parser(description=None, usage=None, epilog=None):
    """Create a new parser with those texts

    If description is a parser
        then take all texts from that
    """
    if usage is None and epilog is None:
        try:
            parser_ = description.parser
            description = parser_.description
            usage = parser_.usage
            epilog = parser_.epilog
        except AttributeError:
            pass
    return FunctionsParser(description, usage, epilog)


def get_alt_screen():

    def stop_alt_screen():
        run('tput rmcup')

    def start_alt_screen():
        atexit.register(stop_alt_screen)
        run('tput smcup')

    return start_alt_screen
