from dataclasses import dataclass

from pysyte import os

OK = os.EX_OK
FAIL = os.EX_FAIL

def exits():
    """All the EX_* symbols in the os module, by name

    >>> x = exits()
    >>> assert x["EX_OK"] == 0
    """
    return {_: getattr(os, _) for _ in dir(os) if 'EX_' in _}



@dataclass
class ExitCode:
    code: int = OK

    def __post_init__(self):
        self.exit = self.string()

    def __int__(self) -> int:
        return self.code

    def __str__(self):
        return self.name

    def raise(self, message: str = "") -> None:
        raise SystemExit(self.code, message) if message else SystemExit(self.code)

    @property
    def ok(self):
        return self.code == OK

    @property
    def errors(self):
        return not self.ok

    @property
    def name(self) -> str:
        for name, code in exits().items():
            if code == self.code:
                return name
        code = self.code
        return f"{code=}"


ok = ExitCode(OK)
fail = ExitCode(FAIL)
