from dataclasses import dataclass
from fnmatch import fnmatch

from pysyte.types.trees.strings import StringPath


@dataclass
class PathGlobber:
    pattern: str

    def match(self, path: StringPath) -> bool:
        """Match the entire path against the pattern."""
        return fnmatch(str(path), self.pattern)

    def basename(self, path: StringPath) -> bool:
        """Match the basename of the path against the pattern."""
        basename = path.basename()
        return fnmatch(basename, self.pattern)

    def directory(self, path: StringPath) -> bool:
        """Match the directory name of the path against the pattern."""
        directory = path.parent.basename()
        return fnmatch(directory, self.pattern)

    def directories(self, path: StringPath) -> bool:
        """Match any directory in the path against the pattern."""
        directories = path.parent_directories()
        return any(fnmatch(d.basename(), self.pattern) for d in directories)
