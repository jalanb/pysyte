"""Import imports for pysyte"""
import abc
import os
import importlib
import linecache
import ast
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator

from pym.ast.visit import visitors


class ImportVisitor(visitors.PymVisitor):
    def __init__(self):
        super().__init__()
        self.imports = defaultdict(list)
        self.froms = defaultdict(list)

    @abc.abstractmethod
    def imported(self, name, line):
        pass

    def collect_names(self, node):
        names = [(_.name, getattr(_, "asname", "")) for _ in node.names]
        for name, alias in names:
            self.imports[alias if alias else name].append(node.lineno)
        return names

    def find_value_id(self, node, attr=None):
        if not node:
            return None
        value = getattr(node, "value", None)
        if not value:
            if attr:
                value = getattr(getattr(node, attr, None), "value", None)
                if not value:
                    name = getattr(getattr(node, attr, None), "id", None)
                    if name:
                        return name
        if not value:
            return getattr(node, "id", None)
        result = getattr(value, "id", None)
        if result:
            return result
        return self.find_value_id(value, attr)

    def find_name(self, node, *args):
        name = getattr(node, "id", None)
        if name is not None:
            return name
        for attribute in args:
            attr = getattr(node, attribute, None)
            if attr:
                name = self.find_name(attr, *args)
                if name:
                    return name
        return None

    def visit_ImportFrom(self, node):
        if node.module != "__future__":
            names = self.collect_names(node)
            self.froms[node.module].extend(names)
        self.generic_visit(node)

    def visit_Import(self, node):
        _ = self.collect_names(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        for decorator in node.decorator_list:
            name = self.find_name(decorator, "func", "value")
            self.imported(name, decorator)
        self.generic_visit(node)

    def visit_Subscript(self, node):
        name = self.find_value_id(node)
        name2 = self.find_name(node, "value")
        assert name == name2
        self.imported(name, node)
        subname = self.find_value_id(node.slice)
        assert subname == self.find_name(node.slice, "value")
        self.imported(subname, node)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        try:
            self.imported(node.value.id, node.lineno)
            full_name = f"{node.value.id}.{node.attr}"
            self.imported(full_name, node.lineno)
        except AttributeError:
            pass
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        for base in node.bases:
            name = self.find_name(base, "value")
            self.imported(name, node)
        self.generic_visit(node)

    def visit_Call(self, node):
        func = node.func
        try:
            name = func.id
        except AttributeError:
            name = self.find_value_id(func, "func")
            name2 = self.find_name(node, "value", "func")
            assert name == name2
        self.imported(name, node)
        self.generic_visit(node)

    def visit_Name(self, node):
        name = self.find_name(node)
        self.imported(name, node)
        self.generic_visit(node)


class UsedImportVistor(ImportVisitor):
    def __init__(self):
        super().__init__()
        self.used = defaultdict(list)

    def imported(self, name, node):
        if not name:
            return
        if name in self.imports:
            self.used[name].append(node.lineno)

    def unused(self):
        return {k: v for k, v in self.imports.items() if k not in self.used}

    def unused_lines(self):
        result = defaultdict(set)
        for name, lines in self.unused().items():
            for line in lines:
                result[line].add(name)
        return result

    def multiples(self):
        return {k: v for k, v in self.imports.items() if len(v) > 1}

    def line(self, line_number, with_number=True):
        line = linecache.getline(self.path, line_number).rstrip()
        if not with_number:
            return line
        return f"{line_number:4d}: {line}"


@dataclass
class AS3:
    path: str
    tree: ast.Module


def find_imports(as3: AS3) -> UsedImportVistor:
    import_user = UsedImportVistor()
    import_user.visit(as3.tree)
    return import_user


@contextmanager
def parse_python(script) -> Iterator[AS3]:
    with open(script) as stream:
        as3 = ast.parse(stream.read(), script)
        yield AS3(script, as3)


def parse(script) -> UsedImportVistor:
    """Extract all imports from a python script"""
    if not os.path.isfile(script):
        raise FileNotFoundError(f"Not a file: {script}")
    with parse_python(script) as as3:
        importer = find_imports(as3)
        importer.path = script  # type: ignore [attr-defined]
        return importer


@contextmanager
def importer(module):
    """Provide a context with that module

    >>> with importer(os) as os_, importer('pysyte.importers') as importers:
    ...     assert os_.path is os.path
    ...     assert importer.__code__ == importers.importer.__code__
    ...
    """
    if isinstance(module, type(os)):
        yield module
    elif isinstance(module, str):
        yield importlib.import_module(module)
