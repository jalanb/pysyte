"""Handle methods for pysyte

>>> from pysyte.types import methods

>>> def fred(i: int = 0, s: str = "") -> str:
...     '''If in doubt, call it Fred'''
...     return "fred"

>>> foo = methods.method(fred)
>>> assert "def fred" in foo.code
"""

import ast
from dataclasses import dataclass

from lazy import lazy
from pym.ast import parse

from pysyte.types import functions

@dataclass
class Method(functions.Function):
    """A callable method from a selfie"""

    selfie: object | None = None

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.callable, MethodType):
            self.selfie = self.callable.__self__

    def run(self, *args, **kwargs):
        return self.callable(self.selfie, *args, **kwargs)

    def about_that_egg(self, arg_name: str) -> list[str]:
        """Duck type that arg in this method"""
        requirements = [f"{self.name}()"]
        return about_that_egg(self.ast, arg_name, requirements)



def about_that_egg(ast: ast.AST, arg_name: str, requirements : list[str]) -> list[str]:
    """Duck type that arg in this method

    About the name:
        Comes from a cartoon, where the bad guy threatens Daffy with
        > Alright Duck. About that egg!

        But Daffy is not that type of duck
    """
    from pym.ast.visitors import DuckVisitor
    visitor = DuckVisitor(ast, arg_name, requirements)
    visitor.visit(ast)
    return visitor.usages


def method(bound_method: MethodType) -> Method:
    """Convenience method to avoid importing capitals

    >>> class Fred:
    ...     def fred(self):
    ...         pass
    >>> fred = Fred().fred
    >>> assert method(fred) == Method(fred)

    >>> m = method(fred)
    >>> assert m.callable == fred
    >>> assert m.name == "fred"
    """
    return Method(bound_method)
