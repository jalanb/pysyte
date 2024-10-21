class PathError(Exception):
    """Something went wrong with a path"""

    prefix = "Path Error"


class MissingPath(PathError):
    def __init__(self, path, desc=""):
        self.path = path
        description = desc or "path"
        super().__init__(f"Missing {description}{path}")


class MissingImport(MissingPath):
    def __init__(self, module):
        self.module = module
        try:
            path_ = module.__file__
        except AttributeError:
            path_ = module.__name__
        super().__init__(path_, desc="module")
