from pysyte import os

def exits():
    import os
    return {k:v for k, v in os.globals().items() if k.startswith("EX_")}

@dataclass
class ExitCode:
    exit_code: int = EX_OK

    def __post_init__(self):
        self.exit = self.string()

    def __int__(self) -> int:
        return self.exit_code

    def __str__(self):
        return self.exit

    @property
    def ok(self):
        return self.exit_code == EX_OK

    @property
    def errors(self):
        return not self.ok

    def string(self) -> str:
        if self.ok:
            return "EX_OK"
        import os
        for ex_name, code in exits().items():
            if code == self.exit_code:
                return ex_name
        exit = self.exit_code
        return f"{exit=}"

pass_ = os.ExitCode(os.EX_OK)
fail = os.ExitCode(os.EX_FAIL)

