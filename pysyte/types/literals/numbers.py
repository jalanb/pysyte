"""Handle numbers for pysyte

>>> from pysyte.types.literals import numbers

>>> assert numbers.ten == 10
>>> assert numbers.twelve == 12
>>> assert numbers.ninety_nine == 99

"""
from bidict import bidict

zero = 0


def on_import():
    digits = (
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    )
    teens = (
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
    )
    tens = (
        "ten",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
    )

    data = {}
    data.update({v: k for k, v in enumerate(digits, 1)})
    data.update({v: k for k, v in enumerate(teens, 11)})
    for i, dd in enumerate(tens, 1):
        data[dd] = i * 10
        if i == 1:
            continue
        for j, d in enumerate(digits, 1):
            data[f"{dd}_{d}"] = i * 10 + j
    return data


def name(n: int) -> str:
    """Get the name of an integer

    >>> assert name(0) == "zero"
    >>> assert name(7) == "seven"
    >>> assert name(123) == "one hundred and twenty three"
    >>> assert name(2_000) == "two thousand"
    >>> assert name(2_001) == "two thousand and one"
    >>> assert name(2_100) == "two thousand, one hundred"
    >>> assert name(2_101) == "two thousand, one hundred and one"
    >>> assert name(54321) == "fifty four thousand, three hundred and twenty one"
    >>> assert name(2_000_000) == "two million"
    >>> assert name(2_000_001) == "two million and one"
    >>> assert name(2_000_100) == "two million and one hundred"
    >>> assert name(2_001_000) == "two million and one thousand"
    >>> assert name(2_000_101) == "two million, one hundred and one"
    >>> assert name(2_001_001) == "two million, one thousand and one"
    >>> assert name(2_001_100) == "two million and one thousand, one hundred"
    >>> assert name(2_001_101) == "two million, one thousand, one hundred and one"
    >>> assert (
    ...     name(7654321)
    ...     == "seven million, six hundred and fifty four thousand, three hundred and twenty one"
    ... )
    >>> assert (
    ...     name(77654021)
    ...     == "seventy seven million, six hundred and fifty four thousand and twenty one"
    ... )
    >>> assert (
    ...     name(7777654001)
    ...     == "seven billion, seven hundred and seventy seven million, six hundred and fifty four thousand and one"
    ... )
    >>> assert (
    ...     name(12000000000000000000007890000000000000000000045391)
    ...     == "twelve quindecillion, seven octillion, eight hundred and ninety heptillion, forty five thousand, three hundred and ninety one"
    ... )
    """

    def bigger_name(n: int, m: int, units: str) -> str:
        """Get the name of a bigger number

        This will only be called with n > 1_000_000
        """
        assert n > m
        div, mod = divmod(n, m)
        assert div
        divs_ = f"{name(div)} {units}" if 0 < div else ""
        if not mod:
            return divs_
        mods_ = name(mod)
        and_ = ", " if " and " in mods_ else " and "
        result = f"{divs_}{and_}{mods_}"
        return result

    if n < 0:
        return f'minus {name(-n)}'
    result_ = f"{n:_}"
    data = {k: v for k, v in globals().items() if isinstance(v, int)}
    numbers = dict(bidict(data).inverse)
    if n in numbers:
        return numbers[n].replace('_', ' ')
    thousands, units = divmod(n, 1_000)
    hundreds, tens = divmod(units, 100)
    tens_ = f"{name(tens)}" if tens else ""
    hundreds_ = f"{name(hundreds)} hundred" if 0 < hundreds < 100 else ""
    and_ = " and " if hundreds and tens else ""
    result = f'{hundreds_}{and_}{tens_}'
    if n < 1_000:
        return result
    and_ = ""
    if thousands:
        if tens:
            and_ = " and "
        if hundreds:
            and_ = ", "
    thousands_ = f"{name(thousands)} thousand" if 0 < thousands else ""
    result = f"{thousands_}{and_}{result}"
    if n < 1_000_000:
        return result
    prefixes = (
        "m",
        "b",
        "tr",
        "quadr",
        "quint",
        "sext",
        "hept",
        "oct",
        "non",
        "dec",
        "undec",
        "duodec",
        "tredec",
        "quattuordec",
        "quindec",
        "sexdec",
        "septdec",
        "octodec",
        "novemdec",
        "vigint",
    )
    i = 1_000_000
    for prefix in prefixes:
        j = i * 1_000
        if n < j:
            name_ = f"{prefix}illion"
            return bigger_name(n, i, name_)
        i = j
    return "bigger"


globals().update(on_import())


del on_import

if __name__ == '__main__':
    import doctest

    doctest.testmod()
