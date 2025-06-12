#! /usr/bin/env python3
"""Find imports in python files

Show any imports which are unused, or mutiple
"""

import linecache

from pysyte import importers
from pysyte.cli.main import run
from pysyte.types import paths


def add_args(parser):
    """Parse out command line arguments"""
    parser.positional("source", help="path to source(s) to be checked")
    parser.boolean("", "edit", help="Show a command for editing")
    parser.boolean("", "multiple", help="Show multiple imports")
    parser.boolean("", "unused", help="Show unused imports")
    return parser


def texter(path):
    """Make a function to get a line form that file"""

    def text(line_number: int) -> str:
        """Get the line at that number

        Return a string showing the line number and the line
        """
        string = "% 4d: %s" % (line_number, linecache.getline(path, line_number))
        return string.rstrip()

    return text


def show_unused(visitor):
    """Show the unused lines that visitor found"""
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
    """Show the multiple imports that visitor found"""
    multiples = visitor.multiples()
    if multiples:
        print("Multiples:")
    for name, lines in multiples.items():
        instances = [visitor.line(_, True) for _ in lines]
        lines = [name] + instances
        print("\n".join(lines))
    return multiples.keys()


def find_sources(args):
    """Find all the source files in those args

    args might include paths to files/dirs
        all files in the args (or in the dirs) should be returned
    """
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
