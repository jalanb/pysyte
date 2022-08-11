"""Show some lines from files

Usage: python3 -m pysyte.kat [options] [files]

"""

from pysyte.cli.app import App
from pysyte.cli.lines import arg_lines


def args(app):
    return (app.args.files("files"),)


def kat(app):
    """Run kat"""
    for file in app.args.files():
        text = file.read()
        start, lines_in = arg_lines(text, args)
        lines_out = args.sed(lines_in, start)
        text_ = "\n".join(lines_out)
        print(f"{text_}\n")
    return True


def main():
    with App(kat) as app:
        app.run()


if __name__ == "__main__":
    main()
