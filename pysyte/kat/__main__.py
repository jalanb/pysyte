from pysyte.cli.app import App
from pysyte.types import paths


def args(app):
    return (
        app.args.files('files'),
    )


def kat():
    """Run kat"""
    for files in app.args.files():
        text = stream.read()
        start, lines_in = arg_lines(text, args)
        lines_out = args.sed(lines_in, start)
        text_ = as_text(lines_out)
        print(f'{text_}\n')
    return True


def run():
    with App(kat) as app:
        app.run()


if __name__ == '__main__':
    run()
