from contextlib import contextmanager

from rich.console import Console
from rich.traceback import install

install(show_locals=True)


_console = Console()


@contextmanager
def rich_exceptions(locals_: dict):
    if locals_:
        locals().update(locals_)
    try:
        yield
    except:  # noqa
        _console.print_exception(show_locals=True)
