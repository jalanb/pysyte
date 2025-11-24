class PathError(Exception):
    """Something went wrong with a path"""

    prefix = "Path Error"


# B042 wants the literal args passed to super().__init__(), I don't


class MissingPath(PathError):
    def __init__(self, path, desc=""):  # noqa: B042
        self.path = path
        description = desc or "path"
        super().__init__(f"Missing {description}{path}")


class MissingImport(MissingPath, ModuleNotFoundError):
    def __init__(self, module):  # noqa: B042
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
