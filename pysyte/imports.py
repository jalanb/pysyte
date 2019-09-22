import os
import linecache
import ast
from collections import defaultdict


from pysyte.types import dictionaries


class ImportVisitor(ast.NodeVisitor):

    def __init__(self):
        super().__init__()
        self.imports = defaultdict(list)
        self.froms = defaultdict(list)

    def check_usage(self, name, line):
        if not name:
            return
        found = name in self.imports
        if found:
            self.used[name].append(line)

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
        for decorator in node.decorator_list:
            name = self.find_name(decorator, 'func', 'value')
            self.check_usage(name, decorator.lineno)
        self.generic_visit(node)

    def visit_Subscript(self, node):
        name = self.find_value_id(node)
        name2 = self.find_name(node, 'value')
        assert name == name2
        self.check_usage(name, node.lineno)
        subscript = self.find_value_id(node.slice)
        name2 = self.find_name(node.slice, 'value')
        assert subscript == name2
        self.check_usage(subscript, node.lineno)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        try:
            self.check_usage(node.value.id, node.lineno)
        except AttributeError:
            pass
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        for base in node.bases:
            name = self.find_name(base, 'value')
            self.check_usage(name, node.lineno)
        self.generic_visit(node)

    def visit_Call(self, node):
        func = node.func
        try:
            name = func.id
        except AttributeError:
            name = self.find_value_id(func, 'func')
            name2 = self.find_name(node, 'value', 'func')
            assert name == name2
        self.check_usage(name, node.lineno)
        self.generic_visit(node)

    def visit_Name(self, node):
        name = self.find_name(node)
        self.check_usage(name, node.lineno)
        self.generic_visit(node)


class ImportAnalyser(ImportVisitor):
    def __init__(self):
        dd = defaultdict
        super().__init__()
        self.used = defaultdict(list)

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


def find_imports(tree):
    visitor = ImportAnalyser()
    visitor.visit(tree)
    return visitor


def parse_python(path):
    with open(path) as stream:
        return ast.parse(stream.read(), path)


def extract_imports(script):
    """Extract all imports from a python script"""
    if not os.path.isfile(script):
        raise ValueError(f'Not a file: {script}')
    parse_tree = parse_python(script)
    result = find_imports(parse_tree)
    result.path = script
    return result
