"""A module to provide decorators which change methods"""

import pdb

try:
    import pudb as pdb
except ImportError:
    pass


def _represent_arguments(*arguments, **keyword_arguments):
    """Represent the aruments in a form suitable as a key (hashable)

    And which will be recognisable to user in error messages
    >>> print(_represent_arguments([1, 2], **{'fred':'here'}))
    [1, 2], fred='here'
    """
    argument_strings = [repr(a) for a in arguments]
    keyword_strings = [
        '='.join((k, repr(v))) for k, v in keyword_arguments.items()]
    return ', '.join(argument_strings + keyword_strings)


def memoize(method):
    """A new method which acts like the given method but memoizes arguments

    See https://en.wikipedia.org/wiki/Memoization for the general idea
    >>> @memoize
    ... def test(arg):
    ...     print('called')
    ...     return arg + 1
    >>> test(1)
    called
    2
    >>> test(2)
    called
    3
    >>> test(1)
    2

    The returned method also has an attached method "invalidate"
        which removes given values from the cache
        Or empties the cache if no values are given
    >>> test.invalidate(2)
    >>> test(1)
    2
    >>> test(2)
    called
    3
    """
    method.cache = {}

    def invalidate(*arguments, **keyword_arguments):
        key = _represent_arguments(*arguments, **keyword_arguments)
        if not key:
            method.cache = {}
        elif key in method.cache:
            del method.cache[key]
        else:
            raise KeyError(f'Not prevously cached: {method.__name__}({key})')

    def new_method(*arguments, **keyword_arguments):
        """Cache the arguments and return values of the call

        The key cached is the repr() of arguments
            This allows more types of values to be used as keys to the cache
            Such as lists and tuples
        """
        key = _represent_arguments(*arguments, **keyword_arguments)
        if key not in method.cache:
            method.cache[key] = method(*arguments, **keyword_arguments)
        return method.cache[key]
    new_method.invalidate = invalidate
    new_method.__doc__ = method.__doc__
    new_method.__name__ = f'memoize({method.__name__})'
    return new_method


def debug(method):
    """Decorator to debug the given method"""
    def new_method(*args, **kwargs):
        try:
            pdb.runcall(method, *args, **kwargs)
        except pdb.bdb.BdbQuit:
            pass
    new_method.__doc__ = method.__doc__
    new_method.__name__ = f'debug({method.__name__})'
    return new_method
