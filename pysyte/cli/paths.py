from pysyte.cli.arguments import ArgumentsParser
from pysyte.types.paths import path


class PathParser(ArgumentsParser):
    """Handle positional args as paths"""

    def __init__(self, argparser, paths_arg=None):
        super().__init__(argparser)
        self.paths_arg = paths_arg if paths_arg else "paths"
        super().positionals(self.paths_arg)

    def post_parser(self, arguments):
        strings = arguments.get_arg(self.paths_arg)
        paths = [path(_) for _ in strings]
        arguments.set_arg(self.paths_arg, [_ for _ in paths if _])
        arguments.set_arg(f"not_{self.paths_arg}", [_ for _ in paths if not _])
        return arguments


def add_args(old_parser, name=None):
    parser = PathParser(old_parser.parser, name)
    return parser
