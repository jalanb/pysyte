"""Handle nothing for pysyte

>>> from pysyte.types import nothing
>>> assert not nothing.NoThing()

"""

from functools import total_ordering
from typing import Any


@total_ordering
class NoThing:
    def __hash__(self) -> int:
        return hash(None)

    def __bool__(self) -> bool:
        return False

    def __int__(self) -> int:
        return 0

    def __float__(self) -> float:
        return 0.0

    def __str__(self) -> str:
        return ""

    def __eq__(self, fred: Any) -> bool:
        return not fred

    def __lt__(self, fred: Any) -> bool:
        return True


def no_thing(class_: type) -> type:
    """Converts the given class to a NoThing

    A No... class creates instances which act like None

    >>> class Fred:
    ...     def __str__(self):
    ...         return "fred"
    >>> assert str(Fred()) == "fred"
    >>> NoFred = no_thing(Fred)
    >>> assert issubclass(NoFred, Fred)
    >>> no_fred = NoFred()
    >>> assert str(no_fred) == "", f"{str(no_fred)}"
    >>> assert isinstance(no_fred, NoFred)
    >>> assert isinstance(no_fred, Fred)
    """
    no_name = f'No{class_.__name__}'
    return type(no_name, (NoThing, class_), {})
