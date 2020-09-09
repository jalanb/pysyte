import os
import linecache
import ast
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from dataclasses import field
from typing import Dict

from pysyte.types import dictionaries


class ImportVisitor(ast.NodeVisitor):

    def __init__(self):
        super().__init__()
        self.imports = defaultdict(list)
        self.froms = defaultdict(list)

    def imported(self, name, line):
        raise NotImplementedError(f"imported({name}, {line}")

    def collect_names(self, node):
        names = [(_.name, getattr(_, 'asname', None)) for _ in node.names]
        for name, alias in names:
            self.imports[alias if alias else name].append(node.lineno)
        return names

    def find_value_id(self, node, attr=None):
        if not node:
            return None
        value = getattr(node, 'value', None)
        if not value:
            if attr:
                value = getattr(getattr(node, attr, None), 'value', None)
                if not value:
                    name = getattr(getattr(node, attr, None), 'id', None)
                    if name:
                        return name
        if not value:
            return None
        result = getattr(value, 'id', None)
        if result:
            return result
        return self.find_value_id(value, attr)

    def find_name(self, node, *args):
        name = getattr(node, 'id', None)
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
        if node.module != '__future__':
            names = self.collect_names(node)
            self.froms[node.module].extend(names)
        self.generic_visit(node)

    def visit_Import(self, node):
        self.collect_names(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        breakpoint()
        for decorator in node.decorator_list:
            name = self.find_name(decorator, 'func', 'value')
            self.imported(name, decorator.lineno)
        self.generic_visit(node)

    def visit_Subscript(self, node):
        name = self.find_value_id(node)
        name2 = self.find_name(node, 'value')
        assert name == name2
        self.imported(name, node.lineno)
        subname = self.find_value_id(node.slice)
        assert subname == self.find_name(node.slice, 'value')
        self.imported(subname, node.lineno)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        try:
            self.imported(node.value.id, node.lineno)
            full_name = f'{node.value.id}.{node.attr}'
            self.imported(full_name, node.lineno)
        except AttributeError:
            pass
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        for base in node.bases:
            name = self.find_name(base, 'value')
            self.imported(name, node.lineno)
        self.generic_visit(node)

    def visit_Call(self, node):
        func = node.func
        try:
            name = func.id
        except AttributeError:
            name = self.find_value_id(func, 'func')
            name2 = self.find_name(node, 'value', 'func')
            assert name == name2
        self.imported(name, node.lineno)
        self.generic_visit(node)

    def visit_Name(self, node):
        name = self.find_name(node)
        self.imported(name, node.lineno)
        self.generic_visit(node)


@dataclass
class ImportUserData(ImportVisitor):
    used: Dict = field(default_factory=defaultdict(list))


class ImportUser(ImportUserData):

    def imported(self, name, line):
        if not name: return
        if name in self.imports:
            self.used[name].append(line)

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
        return f'{line_number:4d}: {line}'


@contextmanager
def find_imports(tree):
    return ImportUser().visit(tree)


@contextmanager
def parse_python(script):
    with open(script) as stream:
        as3 = ast.parse(stream.read(), script)
        as3.path = script
        yield as3


def extract_imports(script):
    """Extract all imports from a python script"""
    if not os.path.isfile(script):
        raise ValueError(f'Not a file: {script}')
    with parse_python(script) as as3:
        result = find_imports(as3)
        result.path = script
        return result


@contextmanager
def importer(*args):
    """Provide a context with those modules

        >>> with importer(os, ('pysyte.imports')) as (os_, methods_)
        ...     assert os_.path is os.path
        ...     assert importer == methods.importer
    """
    result = []
    for module in args:
        if isinstance(module, type(inspect)):
            result.append(module)
        elif isinstance(module, str):
            result.append(importlib.import_module(module))
    yield result
