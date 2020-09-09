"""Handle sources for pysyte"""

from dataclasses import dataclass
from functools import singledispatch

from pym.ast.parse import parse
from pysyte.types import paths

class SourceError(NotImplementedError):
    def __init__(*args, **kwargs):
        breakpoint()


@dataclass
class SourceTextData:
    source: str = ""


class SourceText(SourceTextData):
    def __init__(self, source_):
        super().__init__(source_)
        self.ast = parse(source_)
        breakpoint()

    def grep(self, type_, name):
        breakpoint()


@dataclass
class SourcePathData:
    path: paths.FilePath

class SourcePath(SourcePathData):
    def __init__(self, path_):
        super().__init__(path_)
        self.text = SourceText(self.path.text)


@singledispatch
def source(arg: type(None)):
    breakpoint()
    return SourceText()


@source.register(str)
def _(arg):
    return source('')


@dataclass
class Language:
    name: str


@source.register(type(paths.FilePath))
def _(arg):
    return Source(arg)


def sources(strings_: list):
    return (source(_) for _ in strings_)
