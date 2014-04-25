"""Some methods to help with the handling of dictionaries"""


def get_caselessly(dictionary, sought):
    """Find the sought key in the given dictionary regardless of case

    >>> things = {'Fred' : 9}
    >>> print get_caselessly(things, 'fred')
    9
    """
    try:
        return dictionary[sought]
    except KeyError:
        caseless_keys = dict([(k.lower(), k) for k in dictionary.keys()])
        real_key = caseless_keys[sought.lower()]  # allow any KeyError here
        return dictionary[real_key]


def swap_dictionary(dictionary):
    """Swap keys for values in the given dictionary"""
    if not dictionary:
        return {}
    result = {}
    for k, v in dictionary.iteritems():
        result[v] = k
    return result
