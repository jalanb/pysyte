"""Handle datetime for pysyte types"""

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
