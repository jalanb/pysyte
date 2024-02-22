"""Handle requirements for pysyte"""

from dataclasses import dataclass

from pysyte.types import versions
from pysyte.types.paths import dirs
from pysyte.types.paths import files
from pysyte.types.python import packages


@dataclass
class Requirement(packages.Package):
    """A python package required by something or other"""

    min_: versions.version = versions.NoVersion()
    max_: versions.version = versions.NoVersion()

    def __postinit__(self):
        import re

        breakpoint()
        if re.search('[<=>]', self.name):
            pass


@dataclass
class Requirements:
    """A collection of requirements"""

    required: list = [Requirement]

    def extend(self, items: list[Requirement]):
        self.required.extend(items)

    def append(self, item: Requirement):
        self.required.append(item)

    def pop(self) -> Requirement:
        return self.required.pop()

    def __iter__(self):
        yield from self.required


class RequirementDir(dirs.DirPath):
    """A directory, with requirements files as *.txt"""

    def requirement_files(self):
        """The requirements files in here"""
        return self.files('*.txt')


def parse(file: files.FilePath) -> Requirements:
    breakpoint()
