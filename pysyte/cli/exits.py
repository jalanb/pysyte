"""Help pysyte handle exit codes

>>> x = ExitCode(os.EX_USAGE)
>>> assert x.code == os.EX_USAGE
>>> assert x.NAME == "EX_USAGE"

"""
from dataclasses import dataclass

from pysyte import os
from pysyte.types.methods import memoized
from pysyte.types.strings import Repper


@dataclass
class ExitCode(Repper):
    """ Has an exit code and a name

    >>> x = ExitCode(os.EX_USAGE)
    >>> assert x == os.EX_USAGE
    >>> assert x.code == os.EX_USAGE
    >>> assert x.NAME == "EX_USAGE"
    >>> assert x.name == "usage"
    """
    code: int

    def __bool__(self) -> bool:
        return self.code == EX_OK

    def __int__(self) -> int:
        return self.code

    def __str__(self) -> str:
        return self.NAME

    def __eq__(self, other) -> bool:
        try:
            return self.code == other.code
        except AttributeError:
            try:
                return self.code == int(other)
            except (ValueError, TypeError):
                return False

    def repr_value(self) -> str:
        try:
            name = self.NAME
        except KeyError:
            name = "EX_???"
        return f"{name} == {self.code}"

    def exit(self, message: str = "") -> None:
        raise SystemExit(self.code, message)

    @property
    def name(self) -> str:
        return ex_low_name(self.NAME)

    @property
    def NAME(self) -> str:
        try:
            return EX_CODES()[self.code]
        except KeyError:
            code = self.code
            raise KeyError(f"{code=}")


@memoized
def ex_low_name(ex_str: str) -> str:
    """
    >>> assert ex_low_name("EX_USAGE") == "usage"
    """
    return ex_str.replace("EX_", "").lower()


@memoized
def EX_NAMES() -> dict[str, int]:
    """a dict of exit names, from os module

    >>> assert EX_NAMES()["EX_USAGE"] == 64 == os.EX_USAGE
    """
    return {_:getattr(os, _) for _ in dir(os) if _.startswith("EX_")}


@memoized
def names() -> dict[str]:
    """a dict of exit names, with the "EX_" removed, and lowercased

    >>> assert names()["usage"] == 64 == os.EX_USAGE
    """
    return {ex_low_name(k):v for k, v in EX_NAMES().items()}


@memoized
def EX_CODES() -> dict[int, str]:
    """a dict of exit codes

    >>> assert EX_CODES()[os.EX_USAGE] == "EX_USAGE"
    """
    return {v:k for k, v in EX_NAMES().items()}


@memoized
def exit_codes() -> dict[str, ExitCode]:
    """a dict of exit codes

    >>> assert exit_codes()["usage"] == ExitCode(os.EX_USAGE)
    """
    return {k:ExitCode(v) for k, v in names().items()}


globals().update(EX_NAMES())
globals().update(exit_codes())
