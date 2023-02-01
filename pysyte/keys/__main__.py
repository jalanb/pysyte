#! /usr/bin/env python3
"""Script to get a key from the keyboard"""

from __future__ import print_function


from pysyte.oss import getch
from pysyte.cli.main import run


__version__ = "0.1.1"


class ScriptError(NotImplementedError):
    pass


def add_args(parser):
    parser.boolean("", "codes", help="Show raw codes")
    parser.boolean(
        "",
        "prompt",
        default="",
        help="Prompt to show before getting keys " "(default: none)",
    )
    parser.boolean("", "string", help="Show string")
    return parser


def main(args):
    if args.codes:
        print(", ".join(getch.get_codes()))
    elif args.string:
        print(getch.get_string())
    else:
        print(getch.get_key())
    return True


run(main, add_args)
