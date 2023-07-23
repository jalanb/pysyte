"""Show some lines from files

Usage: python3 -m pysyte.kat [options] [files]

"""

from pysyte.cli import arguments
from pysyte.cli import lines
from pysyte.cli.app import App


def parse_args():
    parser = arguments.parser(__doc__)
    line_parser = lines.add_args(parser)
    return line_parser.parse_args()


def kat(app):
    """Run kat"""
    for file in app.args.files():
        text = file.read()
        start, lines_in = arg_lines(text, app.args)
        lines_out = args.sed(lines_in, start)
        text_ = "\n".join(lines_out)
        print(f"{text_}\n")
    return True


def main():
    args = parse_args()
    with App(kat, args) as app:
        app.run(app.args)


if __name__ == "__main__":
    main()
