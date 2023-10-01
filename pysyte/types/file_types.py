"""This module handles files whose type is known from their extension

.e.g.
    the "type" of "fred.py" is "Python"
    the "type" of "fred.yaml" is "Yaml config"
    the "type" of "fred.ini" is "INI config"
"""

from typing import Any
from typing import List
from dataclasses import dataclass

from pysyte.types.trees import files


@dataclass
class FileType:
    """A file extension and associated type

    >>> class Python:
    >>>     path: files.FilePath

    >>> ft = FileType(Python, "py")
    >>> typed = ft.typed(__file__)
    >>> assert isinstance(typed, Python)
    """

    type_: type
    ext: str

    def extend(self, file_stem: files.FilePath) -> files.FilePath:
        """Returns file stem with missing extension added."""
        return file_stem.add_missing_ext(self.ext)

    def typed(
        self, file_stem: files.FilePath
    ) -> Any:  # actually returns instance of self.type_, but mypy is hard
        """Adds extension to stem and attempts to cast it to the associated type."""
        file = self.extend(file_stem)
        if file:
            return self.type_(file)
        return None


@dataclass
class FileTypes:
    """A collection of FileTypes

    Assuming "fred.yml", or "fred.yaml" exist, then
    >>> class YamlConfig:
    >>>     pass
    >>> configs = FileTypes((YamlConfig, "yaml"), (YamlConfig, "yml"))
    >>> fred = configs.typed("fred")
    >>> assert isinstance(fred, YamlConfig)
    """

    file_types: List[FileType]

    def __init__(self, file_types: List[FileType]):
        """Convert all elements in file_types to FileType instances."""
        self.file_types = [
            _ if isinstance(_, FileType) else FileType(*_) for _ in file_types
        ]

    def extend(self, file_stem: FilePath) -> List[FilePath]:
        """The first real file matching the stem with one of our extensions"""
        for file_type in self.file_types:
            file = file_type.extend(file_stem)
            if file:
                yield file

    def typed(
        self, file_stem: FilePath
    ) -> Any:  # actually yields instances of self.file_types, but mypy is hard
        """An iterator of all possible extensions of that stem which are real files"""
        for file_type in self.file_types:
            typed = file_type.typed(file_stem)
            if typed:
                yield typed
