"""Any option mentioning "a line" means either a number or a regexp"""

import sys
from collections import defaultdict
from functools import partial

from pysyte import __version__
from pysyte.cli.arguments import ArgumentsParser
from pysyte.types import lines as pylines
from pysyte.bash.screen import alt_screen


class LinesParser(ArgumentsParser):
    """Add option sets to the parser"""

    def __init__(self, parser_):
        super().__init__(parser_)
        self.version = __version__
        self.groups = defaultdict(list)

    def add_files(self, name=None, action=None):
        name_ = name if name else "files"
        action_ = action if action else "show"
        self.positional(name_, help=f"{name_} to {action_}")
        return self

    def add_to(self, letter, name, group, type_, help_, default=None):
        letter_ = f'-{letter.lstrip("-")}'
        name_ = f'--{name.lstrip("-")}'
        safe_default = default if default else 0 if str(type_).startswith("int") else ""
        method = getattr(self, type_, f"not a method for {letter},{name}")
        assert callable(method), f"self.{type_}() is {method}"
        if type_ == "boolean":
            arg = method(letter_, name_, help=help_)
        else:
            arg = method(letter_, name_, help=help_, default=safe_default)
        self.groups[group].append(arg)

    def add_lines(self):
        args = {
            "a": ["at", "lines", "inty", "show that line"],
            "c": ["copy", "clipboard", "boolean", "copy text to clipboard"],
            # 'd': ['delete', 'lines', 'string', 'lines to be deleted'],
            "e": ["expression", "ed", "string", "sed expression"],
            "f": ["first", "lines", "inty", "the first line to show", "1"],
            "i": [
                "stdin",
                "stdin",
                "boolean",
                "(aka -) wait for text from stdin",
            ],
            "l": ["last", "lines", "inty", "the last line to show", "0"],
            "n": ["numbers", "lines", "boolean", "show line numbers"],
            "p": [
                "paste",
                "clipboard",
                "boolean",
                "paste text from clipboard",
            ],
            "s": ["substitute", "ed", "string", "sed s-expression"],
            "v": ["remove", "lines", "inty", "remove that line"],
            "V": ["version", "version", "boolean", "show version"],
            "w": ["width", "lines", "integer", "max width of lines", "80"],
        }
        [self.add_to(letter, *args) for letter, args in args.items()]
        return self

    def post_parser(self, args):
        if args.version and self.version:
            sys.stdout.write(f"{sys.argv[0]} version: {self.version}")
            raise SystemExit
        args.sed = partial(pylines.sed, args=args)
        args.alt_screen = alt_screen()
        return args


def add_args(old_parser):
    """Create a new parser to handle some lines from given parser"""
    result = LinesParser(old_parser.parser)
    result.add_lines()
    return result


def arg_lines(a, b):
    raise NotImplementedError
