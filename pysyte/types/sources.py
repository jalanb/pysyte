"""Handle source files for pysyte"""

from dataclasses import dataclass
from functools import singledispatch

from pysyte.types import paths


@singledispatch
def source(str_: str):
    breakpoint()
    return source(paths.path(str_))


@source.register(type(None))
def _(arg):
    return source('')

@dataclass
class Source:
    path: paths.FilePath

@source.register(type(paths.FilePath))
def _(arg):
    return Source(arg)


def sources(strings_: list):
    return (source(_) for _ in strings_)
