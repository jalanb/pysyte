import sys
from functools import partial

from pysyte import __version__
from pysyte.cli.arguments import ArgumentsParser
from pysyte.types import lines as pylines
from pysyte.bash.screen import alt_screen

class FunctionsParser(ArgumentsParser):
    """Add option sets to the parser"""
    def __init__(self, parser_):
        super().__init__(parser_)
        self.version = __version__
        self.groups = dict(args=[])

    def add_version(self, version_=None):
        if version_:
            self.version = version_
        self.boolean('-v', '--version', help='Show version',)
        return self

    def add_files(self, name=None):
        name_ = name if name else 'files'
        self.positional(name_, help=f'{name_} to show')
        return self

    def add_to(self, letter, name, group, help, default=None, type_=None):
        def add_group(group_):
            def add_arg(self):
                setattr(self, f'add_{group}', add_group(group))
                return self

            return method

        letter_ = f'-{letter.lstrip("-")}'
        name_ = f'--{name.lstrip("-")}'
        default_ = default if default else ''
        type_name = type_ if type_ else 'string'
        method = getattr(self, type_, "not a method")
        assert callable(method), f'self.{type_}() is {method}'
        self.groups[group].append(self.add_argument(letter, name, default=default_, help=help))

    def add_functions(self):
        args = {
            'a': ['at', 'lines', 'inty' 'Show line at the line number'],
            'b': ['numbers', 'lines', 'boolean' 'Show line numbers'],
            'c': ['copy', 'clipboard', 'boolean' 'Copy text to clipboard'],
           #'d': ['delete', 'lines', 'string', 'lines to be deleted'],
            'e': ['expression', 'ed', 'string' 'sed expression to be executed'],
            'f': ['first', 'lines', 'inty' 'number/regexp of first line to show', '1'],
            'i': ['stdin', 'stdin', 'boolean' '(aka -) Wait for text from stdin'],
            'l': ['last', 'lines', 'inty' 'number/regexp of last line to show', '0'],
            'p': ['paste', 'clipboard', 'boolean' 'Paste text from clipboard'],
            't': ['editor', 'ed', 'string' 'edit with, e.g., vim'],
            'v': ['version', 'version', 'boolean' 'Show version'],
            'w': ['width', 'lines', 'intger' 'Max width of shown line'],
        }
        [ self.add_to(letter, *args) for letter, args in args.items()]
        return self

    def post_parser(self, args):
        if args.version and self.version:
            sys.stdout.write(f'{sys.argv[0]} version: {self.version}')
            raise SystemExit
        args.sed = partial(
            pylines.reformat_lines, numbers=args.numbers, width=args.width)
        args.alt_screen = alt_screen()
        return args


def parser(parser_):
    """Create a new parser to handle some functions from given parser"""
    return FunctionsParser(parser_.parser)
