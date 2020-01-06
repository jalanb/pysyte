"""This module handles numbers"""

from functools import partial


def _as_number(value, type_, default, strict):
    """Try to use that value as that type

    >>> assert _as_number(2, int, 0, False) == _as_number('2', int, 0, False)
    """
    if not value:
        return default
    try:
        return type_(value)
    except (ValueError, TypeError):
        return None if strict else value


inty = partial(_as_number, type_=int, default=0, strict=False)
floaty = partial(_as_number, type_=float, default=0.0, strict=False)
to_int = partial(_as_number, type_=int, default=0, strict=True)
to_float = partial(_as_number, type_=float, default=0.0, strict=True)
