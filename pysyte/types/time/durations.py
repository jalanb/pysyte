"""Handle dates and durations for pysyte

    >>> from pysyte.types import durations

Provides durations that can be added

    >>> one = durations.Duration(0, 0, 1, 15)
    >>> two = durations.Duration(0, 0, 2, 45)
    >>> sum = one + two
    >>> assert sum.days + sum.hours + sum.seconds == 0
    >>> assert sum.minutes == 4

And subtracted
    >>> assert one == sum - two

"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Duration:
    """How long an event lasted

    >>> duration = Duration(0, 0, 1, 15)
    >>> assert duration.days + duration.hours == 0
    >>> assert duration.minutes == 1
    >>> assert duration.seconds == 15
    """
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    subs: float = 0.0

    def __add__(self, other: Duration) -> Duration:
        """Add self to other

        >>> one = Duration(0, 0, 1, 15)
        >>> two = Duration(0, 0, 2, 45)
        >>> sum = Duration(0, 0, 4, 0)
        >>> assert sum == one + two
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
        >>> sum = Duration(0, 0, 4, 0)
        >>> assert two = sum - one
        """
        days = self.days - other.days
        hours = self.hours - other.hours
        minutes = self.minutes - other.minutes
        seconds = self.seconds - other.seconds
        subs = self.subs - other.subs
        return Duration(days, hours, minutes, seconds, subs)

