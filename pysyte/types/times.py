"""Handle datetime for pysyte's types"""
import datetime
epoch = datetime.datetime.fromtimestamp(0)


def taken(diff, days=True):
    seconds = diff.seconds * 1_000 + diff.microseconds
    if days:
        return seconds
    result = abs(diff.days * 24 * 60 * 60 + seconds)
    return result
