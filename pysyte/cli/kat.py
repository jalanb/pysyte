import sys

from pysyte.cli import streams
from pysyte.cli.main import run
from pysyte.cli.functions import parser
from pysyte.types import lines


def add_args(_):
    """Parse out command line arguments"""
    p = parser()
    p.positional('files', help='files to edit')
    p.inty('-a', '--at', default="", help='Show line at the line number')
    p.inty('-f', '--first', default="1",
               help='number/regexp of first line to show')
    p.inty('-l', '--last', default="0",
               help='number/regexp of last line to show')
    p.boolean('-p', '--paste', help='Paste text from clipboard')
    p.boolean('-i', '--stdin', help='Wait for text from stdin')
    p.lines()
    p.version()
    return p


def kat_main(args):
    """Run the script"""
    at = args.at
    first = args.first or 1
    last = args.last or -1
    for stream in streams.args(args, 'files'):
        start, lines_in = lines.first_and_rest(
            stream,
            at,
            first,
            last
        )
        lines_out = args.sed(lines_in, start)
        print(lines.text(lines_out))
    return True


def main():
    run(kat_main, add_args)

