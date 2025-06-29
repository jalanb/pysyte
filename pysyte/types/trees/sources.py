"""Paths that hold source code"""

from pysyte.types.trees import files


class SourcePath(files.FilePath):
    pass


SourcePath.__file_class__ = SourcePath

