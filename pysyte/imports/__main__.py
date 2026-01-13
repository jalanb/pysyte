#! /usr/bin/env python3
"""Find imports in python files

Show any imports which are unused, or multiple
"""

from pysyte import importers
from pysyte.cli.arguments import ArgumentsParser
from pysyte.cli.main import run
from pysyte.types import paths
from pysyte.types.trees.sources import find_sources


def add_args(parser: ArgumentsParser) -> ArgumentsParser:
    """Parse out command line arguments"""
    parser.positional("source", help="path to source(s) to be checked")
    parser.boolean("", "edit", help="Show a command for editing")
    parser.boolean("", "multiple", help="Show multiple imports")
    parser.boolean("", "unused", help="Show unused imports")
    return parser


def show_unused(visitor: importers.ImportVisitor) -> list[str]:
    """Show the unused lines that visitor found"""

    unused_lines = visitor.unused_lines()
    if not unused_lines:
        return []
    print("Unused:")
    for line_number in sorted(unused_lines):
        names = unused_lines[line_number]
        print(",".join(names))
        print(visitor.numbered_line(line_number))
    return visitor.unused().keys()


def show_multiples(visitor: importers.ImportVisitor) -> list[str]:
    """Show the multiple imports that visitor found"""
    multiples = visitor.multiples()
    if multiples:
        print("Multiples:")
    for name, lines in multiples.items():
        instances = [visitor.line(_) for _ in lines]
        lines = [name] + instances
        print("\n".join(lines))
    return multiples.keys()


def show_imports(args: ArgumentsParser, source: paths.StringPath) -> bool:
    """Parse any source files from the args, showing imports"""
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
    """Find some sources, show imports in them"""
    result = False
    sources = find_sources(args.source)
    for source in sources:
        if show_imports(args, source):
            result = True
    return result


run(main, add_args)
