from pysyte.types.trees.errors import MissingPath
from pysyte.types.trees.errors import PathError


class PathAssertions:
    """Assertions that can be made about paths"""

    def assertExists(self):
        if not self.exists():
            raise MissingPath(self)
        return self

    def assert_isdir(self):
        """Raise a PathError if this path is not a directory on disk"""
        if not self.isdir():
            raise PathError(f"{self} is not a directory")
        return self

    def assert_isfile(self):
        """Raise a PathError if this path is not a file on disk"""
        if not self.isfile():
            raise PathError(f"{self} is not a file")
        return self
