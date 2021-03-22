"""This module handles numbers"""


class NAN(ValueError):
    def __init__(self, value):
        super().__init__(f"NAN: {value}")


def _eval(value, kind, default=None):
    try:
        return kind(value)
    except (ValueError, TypeError):
        # if default is None:
        # raise NAN(value)
        if isinstance(value, (str, type(None))):
            return default
        try:
            return len(value)
        except TypeError:
            raise NAN(value)


as_int = lambda x: _eval(x, int)
as_float = lambda x: _eval(x, float)

inty = lambda x: _eval(x, int, x)
floaty = lambda x: _eval(x, float, x)
