"""Paths that hold source code"""

from pysyte.types.trees import (
    files,
    paths,
)


class SourcePath(files.FilePath):
    pass


SourcePath.__file_class__ = SourcePath


def find_sources(args: list[str]) -> list[paths.Path]:
    """Find all the source files in those args

    args might include paths to files/dirs
        all files in the args (or in the dirs) should be returned
    """
    ignores = ["__pycache__", ".tox", ".git", ".venv"]
    result = []
    for arg in args:
        path_to_arg = paths.path(arg)
        if path_to_arg.isfile():
            result.append(path_to_arg)
        elif path_to_arg.isdir():
            for path_to_file in path_to_arg.walkfiles(pattern="*.py", ignores=ignores):
                result.append(path_to_file)
        else:
            raise TypeError(f"Unknown path type {path_to_arg}")
    return result
