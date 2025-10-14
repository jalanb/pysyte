#! /usr/bin/env python3
"""Script to show a key from the keyboard"""

from pysyte.cli.main import run
from pysyte.oss import getch


def add_args(parser):
    parser.boolean("-c", "--codes", help="Show raw codes")
    parser.boolean(
        "-p",
        "--prompt",
        default="",
        help="Prompt to show before getting keys " "(default: none)",
    )
    parser.boolean("-s", "--string", help="Show string")
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
