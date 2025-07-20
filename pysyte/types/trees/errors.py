class PathError(Exception):
    """Something went wrong with a path"""

    prefix = "Path Error"


class MissingPath(PathError):
    def __init__(self, path, desc=""):
        self.path = path
        description = desc or "path"
        super().__init__(f"Missing {description}{path}")


class MissingImport(MissingPath, ModuleNotFoundError):
    def __init__(self, module):
        self.module = module
        try:
            key = module.__file__
        except AttributeError:
            try:
                key = module.__name__
            except AttributeError:
                key = str(module)
        MissingPath.__init__(self, key, desc="module")
        ModuleNotFoundError.__init__(self, f"No module named '{key=}'")
