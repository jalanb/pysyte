from pysyte.cli.arguments import ArgumentsParser
from pysyte.types.paths import path


class PathParser(ArgumentsParser):
    """Handle positional args as paths"""

    def post_parser(self, args):
        for arg in args:
            arg_path = path(arg)
            if not arg_path.exists():
                continue
            args.set(arg, arg_path)
        return args
