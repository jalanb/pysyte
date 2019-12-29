from functools import partial

def _as_number(value, type_, default=None):
    """Try to use that value as that type"""
    if not value:
        return default
    try:
        return type_(value)
    except TypeError:
        return value

inty = partial(_as_number, type_=int, default=0)
floaty = partial(_as_number, type_=float, default=0.0)
