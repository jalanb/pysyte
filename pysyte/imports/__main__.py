#! /usr/bin/env python3
"""Find imports in python files"""

import linecache

from pysyte import importers
from pysyte.cli.arguments import ArgumentsParser
from pysyte.cli.main import run
from pysyte.types import paths


def add_args(parser: ArgumentsParser) -> ArgumentsParser:
    """Parse out command line arguments"""
    parser.positional("source", help="path to source(s) to be checked")
    parser.boolean("", "edit", help="Show a command for editing")
    parser.boolean("", "multiple", help="Show multiple imports")
    parser.boolean("", "unused", help="Show unused imports")
    return parser


def texter(path):
    def text(line):
        string = "% 4d: %s" % (line, linecache.getline(path, line))
        return string.rstrip()

    return text


def show_unused(visitor):
    unused_lines = visitor.unused_lines()
    if not unused_lines:
        return []
    text = texter(visitor.path)
    print("Unused:")
    for line in sorted(unused_lines):
        names = unused_lines[line]
        print(",".join(names))
        print(text(line))
    return visitor.unused().keys()


def show_multiples(visitor):
    multiples = visitor.multiples()
    if multiples:
        print("Multiples:")
    for name, lines in multiples.items():
        instances = [visitor.line(_, True) for _ in lines]
        lines = [name] + instances
        print("\n".join(lines))
    return multiples.keys()


def find_sources(args):
    ignores = ["__pycache__", ".tox", ".git", ".venv"]
    result = []
    for arg in args:
        path_to_arg = paths.path(arg)
        if path_to_arg.isfile():
            result.append(path_to_arg)
        elif path_to_arg.isdir():
            for path_to_file in path_to_arg.walkfiles(pattern="*.py", ignores=ignores):
                result.append(path_to_file)
        else:
            raise TypeError(f"Unknown path type {path_to_arg}")
    return result


def show_imports(args, source):
    visitor = importers.parse(source)
    modules = []
    if args.multiple:
        modules.extend(show_multiples(visitor))
    if args.unused:
        modules.extend(show_unused(visitor))
    if args.edit and modules:
        sought = r"\|".join((rf"\<{_}\>" for _ in modules))
        print(f'\nvim {visitor.path} +/"{sought}"')
    return bool(modules)


def main(args) -> bool:
    result = False
    sources = find_sources(args.source)
    for source in sources:
        if show_imports(args, source):
            result = True
    return result


run(main, add_args)
