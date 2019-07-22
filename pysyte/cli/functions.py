import sys

from pysyte import __version__
from pysyte.cli.arguments import ArgumentsParser
from pysyte.types import lines as pylines

class FunctionsParser(ArgumentsParser):
    """Add option sets to the parser"""
    def version(self, version_=None):
        self.version = version_ if version_ else __version__
        self.boolean('-v', '--version', help='Show version')

    def lines(self):
        self.boolean('-n', '--numbers', help='Show line numbers')
        self.int('-w', '--width', help='Max width of shown line')

    def post_parser(args):
        if args.version and self.version:
            sys.stdout.write(self.version)
            sys.exit()

    def sed(self, lines, first):
        return pylines.reformat_lines(lines, first, self.numbers, self.width)

def parser(description=None, usage=None):
    return FunctionsParser(usage, epilog)
