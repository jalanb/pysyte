try:
    from itertools import ifilter
except ImportError:
    ifilter = filter


def first(sequence, message=None):
    """The first item in that sequence

    If there aren't any, raise a ValueError with that message

    >>> assert first([1, 2, 3]) == 1
    """
    try:
        return next(iter(sequence))
    except StopIteration:
        raise ValueError(message or (f'Sequence is empty: {sequence}'))


def last(sequence, message=None):
    """The last item in that sequence

    If there aren't any, raise a ValueError with that message

    >>> assert last([1, 2, 3]) == 3
    """
    try:
        return sequence.pop()
    except AttributeError:
        return list(sequence).pop()
    except IndexError:
        raise ValueError(message or f'Sequence is empty: {sequence}')


def first_or(sequence, value):
    """First item in that sequence, or that value

    >>> assert first_or([1, 2, 3], 4) == 1
    >>> assert first_or([], 4) == 4
    """
    try:
        return first(sequence)
    except ValueError:
        return value


def first_that(predicate, sequence, message=None):
    """The first item in that sequence that matches that predicate

    If none matches raise a KeyError with that message

    >>> assert first_that(lambda x: x > 1, [1, 2, 3]) == 2
    """
    try:
        return next(ifilter(predicate, sequence))
    except StopIteration:
        raise KeyError(message or 'Not Found')
