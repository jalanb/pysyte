"""Handle dates and durations for pysyte

    >>> from pysyte.types.time.durations import duration

Provides durations

    >>> one = duration(1, 15)
    >>> two = duration(2, 45)

They can be added
    >>> both = one + two

And subtracted
    >>> assert one == both - two

Handy attributes
    >>> assert both.minutes == 4
    >>> assert both.days + both.hours + both.seconds == 0
"""

from __future__ import annotations

import datetime
from functools import singledispatch
from typing import Tuple

from lazy import lazy

from pysyte.types.methods import none_args
from pysyte.types.time import times

class Duration:
    """How long an event lasted

    >>> duration = Duration(1, 15)
    >>> assert duration.minutes == 1
    >>> assert duration.seconds == 15
    >>> assert duration.days + duration.hours == 0
    """

    limits = [
        ('seconds', 60),
        ('minutes', 60),
        ('hours', 24),
        ('days', 365),
        ('years', 9999)
    ]

    @classmethod
    def seconds_dict(cls, seconds:int) -> dict:
        """divide seconds into intervals

        >>> seven = Duration.seconds_dict(7)
        >>> assert seven['seconds'] == 7
        >>> seventy = Duration.seconds_dict(70)
        >>> assert seventy['seconds'] == 10
        >>> assert seventy['minutes'] == 1
        """
        names = {
            'seconds': 0,
        }
        i = seconds
        for name, limit in cls.limits:
            i, rem = divmod(i, limit)
            names[name] = rem
            if not i:
                break
        return names

    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    subs: float = 0.0

    def __init__(self, *args, **kwargs):
        """Initialise a Duration

        >>> assert Duration(1, 15) == Duration(0, 0, 1, 15)
        >>> assert Duration(1, 15) is Duration(0, 0, 1, 15)
        """
        ints = list(args) + list(kwargs.values())
        counts = [0, 0, 0, 0, 0]
        z = len(counts)
        if len(ints) > z:
            raise ValueError(f"Too many: {ints!r}")
        i = z - 1
        for x in reversed(args):
            counts[i] = x
            i -= 1
            if i < 0:
                break
        aliases = {
            'dd': 'days',
            'hh': 'hours',
            'mm': 'minutes',
            'ss': 'seconds',
            'uu': 'subs',
        }
        attrs = list(aliases.values())
        a_counts = { _: 0 for _ in attrs }
        a_counts['subs'] = 0.0
        data = dict(zip(attrs, a_counts))
        names = self.__dict__
        for k, v in kwargs.items():
            if k in aliases:
                k = aliases[k]
            if k in a_counts:
                a_counts[k] = v
        self.__dict__.update(a_counts)

    def __bool__(self, other) -> bool:
        return int(self) != 0

    def __int__(self) -> int:
        return int(self.total_seconds)

    def __str__(self) -> str:
        return str(int(self))

    def __repr__(self) -> str:
        return f'''{self.__class__.__name__}(
days={self.days},
hours={self.hours},
minutes={self.minutes},
seconds={self.seconds},
subs={self.subs},
) == int({int(self)})'''

    def __add__(self, other: Duration) -> Duration:
        """Add self to other

        >>> one = Duration(0, 0, 1, 15)
        >>> two = Duration(0, 0, 2, 45)
        >>> both = Duration(0, 0, 4, 0)
        >>> assert both == one + two
        """
        days = self.days + other.days
        hours = self.hours + other.hours
        minutes = self.minutes + other.minutes
        seconds = self.seconds + other.seconds
        subs = self.subs + other.subs
        return Duration(days, hours, minutes, seconds, subs)

    def __sub__(self, other: Duration) -> Duration:
        """Subtract other from self

        >>> one = Duration(0, 0, 1, 15)
        >>> two = Duration(0, 0, 2, 45)
        >>> both = Duration(0, 0, 4, 0)
        >>> assert two = both - one
        """
        days = self.days - other.days
        hours = self.hours - other.hours
        minutes = self.minutes - other.minutes
        seconds = self.seconds - other.seconds
        subs = self.subs - other.subs
        return Duration(days, hours, minutes, seconds, subs)

    @lazy
    def total_seconds(self) -> int:
        return self.seconds

    @lazy
    def delta(self) -> datetime.timedelta:
        pass

    @lazy
    def taken(self):
        return times.taken()


class NoDuration(Duration):
    """A class for instantineity

    For mypy and other typing nerds

    >>> none = duration(None)
    >>> assert none isinstance(NoDuration)
    """
    def __init__(self):
        super().__init__(0, 0, 0, 0)

    def __bool__(self, other) -> bool:
        return False

    def __int__(self) -> int:
        return 0

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(0) == 0'

    def __eq__(self, other) -> bool:
        return not other

    def __add__(self, other: Duration) -> Duration:
        return other

    def __sub__(self, other: Duration) -> Duration:
        return other


@singledispatch
def duration(*args, **kwargs) -> Duration:
    """Convert all args to a Duration()

    >>> one = duration(67)
    >>> two = duration((1, 7))
    >>> assert one.seconds == 7 == two.seconds, f'{one.seconds=}, {two=}'
    >>> assert one.minutes == 1 == two.minutes
    >>> diff = two - one
    >>> assert diff.seconds == 0 and diff.minutes == 1
    """
    return NoDuration() if none_args(*args, **kwargs) else Duration(*args, **kwargs)


@duration.register(int)
def _dur(i=0) -> Duration:
    """
    >>> short = duration(7)
    >>> long = duration(67)
    >>> assert short.seconds == 7 == long.seconds
    >>> assert short.minutes == 0
    >>> assert long.minutes == 1
    >>> diff = long - short
    >>> assert diff.minutes == 1
    >>> assert diff.seconds == 0
    """
    return dict_to_duration(Duration.seconds_dict(i))


@duration.register(tuple)
def __dur(items=None) -> Duration:
    """
    >>> passed = duration(5, 6, 7)
    >>> assert passed.hours == 5
    >>> assert passed.minutes == 6
    >>> assert passed.seconds == 7 == duration(6, 7).seconds
    """
    items = items if items else tuple()
    if not all(isinstance(i, int) for i in items):
        raise TypeError(f"Not ints: {items=}")
    return Duration(items)


@duration.register(datetime.timedelta)
def ___dur(arg=None) -> Duration:
    """
    >>> one = datetime.datetime(1979, 12, 25, 1, 2, 3)
    >>> two = datetime.datetime(1979, 12, 25, 1, 2, 4)
    >>> x = duration(two - one)
    >>> assert x.second = 1
    >>> assert x.days + x.hours + x.minutes == 0
    """
    arg = arg if arg else datetime.timedelta(seconds=0)
    return duration(int(arg.seconds))


def dict_to_duration(data: dict) -> Duration:
    """Make a Duration from a dict

    >>> fred = dict_to_duration({'minutes': 3, 'seconds': 7})
    >>> assert fred.seconds == 7
    >>> assert fred.minutes == 3
    >>> assert fred.years is 0
    """

    default = lambda x: data.get(x, 0)

    return Duration(
        days=default('days'),
        hours=default('hours'),
        minutes=default('minutes'),
        seconds=default('seconds'),
        subs=default('subs'),
    )


