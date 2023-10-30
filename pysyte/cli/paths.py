from pysyte.cli.arguments import ArgumentsParser
from pysyte.types.paths import path


class PathParser(ArgumentsParser):
    """Handle positional args as paths"""

    def __init__(self, argparser, paths="paths"):
        super().__init__(argparser)
        self.paths = paths
        super().positionals(self.paths)

    def post_parser(self, arguments):
        strings = arguments.get_arg(self.paths)
        paths = [path(_) for _ in strings]
        arguments.set_arg(self.paths, [_ for _ in paths if _])
        arguments.set_arg(f"not_{self.paths}", [_ for _ in paths if not _])
        return arguments


def add_args(parser: ArgumentsParser, paths="paths") -> ArgumentsParser:
    return PathParser(parser.parser, paths)
