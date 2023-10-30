"""Handle datetime for pysyte


    >>> from pysyte.types.time import times as this
    >>> dt = datetime.datetime


    >>> assert this.seconds_since_epoch()      > 1_000_000_000
    >>> assert this.microseconds_since_epoch() > 1_000_000_000_000
    >>> one = dt(1979, 12, 25, 1, 2, 3)
    >>> two = dt(1979, 12, 25, 1, 2, 4)
    >>> a_second_past = two - one
    >>> assert this.seconds_taken(a_second_past) == 1
    >>> assert this.taken(a_second_past) == 1000
"""

import datetime
import time


def taken(diff):
    """Convert a time diff to total number of microseconds"""
    microseconds = diff.seconds * 1_000 + diff.microseconds
    return abs(diff.days * 24 * 60 * 60 * 1_000 + microseconds)


def seconds_taken(diff):
    """Convert a time diff to total number of seconds"""
    return int(diff.total_seconds())


def now():
    """Convenience method to call datetime's now"""
    return datetime.datetime.now()


def microseconds_since_epoch():
    """Number of microseconds since the epoch"""
    return int(time.time() * 1_000)


def seconds_since_epoch():
    """Number of seconds since the epoch"""
    return int(time.time())
