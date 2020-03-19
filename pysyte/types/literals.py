"""Literal values generally useful"""

# pylint: disable=no-init


class Literals(object):
    pass


class Empty(Literals):
    string = ''
    integer = 0
    real = 0.0


class Python(Literals):
    name = directory = command = package = inline = 'python'
    extension = 'py'
    ext = '.py'
