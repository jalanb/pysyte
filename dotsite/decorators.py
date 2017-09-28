"""A module to provide decorators which change methods"""

from six import StringIO


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
            raise KeyError(
                'Not prevously cached: %s(%s)' % (method.__name__, key))

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
    new_method.__name__ = 'memoize(%s)' % method.__name__
    return new_method


def debug(method):
    """Decorator to debug the given method"""
    def new_method(*args, **kwargs):
        import pdb
        try:
            import pudb
        except ImportError:
            pudb = pdb
        try:
            pudb.runcall(method, *args, **kwargs)
        except pdb.bdb.BdbQuit:
            sys.exit('Normal quit from debugger')
    new_method.__doc__ = method.__doc__
    new_method.__name__ = 'debug(%s)' % method.__name__
    return new_method


def argparser(main_method, options, **kwargs):

    def main(argv):
        args = parser.parse_args(argv)
        for method, _flag, name, _help in options:
            if not method:
                continue
            value = getattr(args, name)
            if not value:
                continue
            method(value)
        return main_method(args)

    from argparse import ArgumentParser
    parser = ArgumentParser(description='Process some integers.')
    for _method, flag, name, help in options:
        name_or_flags = [flag, name] if flag else name
        parser.add_argument(name_or_flags, help=help, **kwargs)
    return main


def streamer(main_method):
    """Open a stream for the first file in arguments, or stdin"""
    def main(arguments):
        streams = [StringIO(get_clipboard_data())] if (arguments and '-c' in arguments) else []
        streams = streams or ([file(_, 'r') for _ in arguments if os.path.isfile(argument)] if arguments else [])
        streams = streams or ([sys.stdin] if not (streams or arguments) else [])
        return main_method(arguments, streams)
    return main


def old_streamer(main_method):
    """Open a stream for the first file in arguments, or stdin"""
    if not arguments:
        return [sys.stdin]
    elif arguments[0] == '-c':
        return [StringIO(get_clipboard_data())]
    for argument in arguments:
        if os.path.isfile(argument):
            return file(argument, 'r')
    return method


def globber(main_method, globs):
    """Recognise globs in args"""
    import os
    from glob import glob

    def main(arguments):
        lists_of_paths = [_ for _ in arguments if glob(pathname, recursive=True)]
        return main_method(arguments, lists_of_paths)
    return main
