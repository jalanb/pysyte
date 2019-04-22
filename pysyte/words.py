"""This module provides methods to handle some features of English words"""


import re


def match_case(string1, string2):
    """Matches the case of string1 in string2

    >>> match_case('MATCHcase', 'somestuff')
    'SOMEStuff'
    """
    if string1.isupper():
        return string2.upper()
    list2 = list(string2)
    for i, char in enumerate(string1[:len(string2)]):
        if char.isupper():
            list2[i] = list2[i].upper()
        elif char.islower():
            list2[i] = list2[i].lower()
    return ''.join(list2)


def _consonants():
    """Letters that are not vowels

    >>> assert _consonants().isalpha()
    >>> assert not any(_ in _consonants() for _ in 'aeiouy')
    """
    return 'bcdfghjklmnpqrstvwxz'


def _ends_in_consonant_suffix(string, suffix):
    """Whether that string ends in a consonant followed by the suffix

    >>> _ends_in_consonant_suffix('pretty', 'y')
    True
    """
    regexp = re.compile('[%s]%s$' % (_consonants(), suffix))
    return regexp.search(string) is not None


def _ends_in_consonant_y(string):
    """Whether that string ends in a consonant and a y

    >>> _ends_in_consonant_y('pretty')
    True
    """
    return _ends_in_consonant_suffix(string, 'y')


def _ends_in_consonant_ies(string):
    """Whether that string ends in a consonant and ies

    >>> _ends_in_consonant_ies('pretties')
    True
    """
    return _ends_in_consonant_suffix(string, 'ies')


def _uncountables():
    """Nouns which are same in plural as singular"""
    return [
        'cowes',
        'deer',
        'equipment',
        'fish',
        'haiku',
        'information',
        'money',
        'rice',
        'series',
        'sheep',
        'species',
    ]


def _exceptional_plurals():
    """Nouns whose plural is just plain weird"""
    return {
        'child': 'children',
        'fungus' : 'fungi',
        'louse': 'lice',
        'man' : 'men',
        'mouse': 'mice',
        'woman' : 'women',
    }


def pluralize(string):
    """Returns the plural of string.

    >>> pluralize('Index')  == 'Indices'
    True
    """
    lowered = string.lower()
    result = string + 's'
    try:
        result = _exceptional_plurals()[lowered]
    except KeyError:
        if lowered in _uncountables():
            result = string
        elif lowered.endswith('ex'):
            result = lowered[:-2] + 'ices'
        elif any(map(lowered.endswith, ['x', 'ch', 'sh', 'ss', 'z'])):
            result = string+'es'
        elif lowered.endswith('o'):
            eos = ['echo', 'hero', 'potato', 'veto', 'tomato']
            if lowered in eos:
                result = string + 'es'
            else:
                result = string + 's'
        elif _ends_in_consonant_y(lowered):
            result = string[:-1] + 'ies'
        else:
            regexp, subs = re.compile(r'([^f])fe$', re.IGNORECASE), r'\1ves'
            if regexp.search(string):
                return regexp.sub(subs, string)
    return match_case(string, result)


def depluralize(string):
    """Returns the singular of string.

    >>> depluralize('Cows') == 'Cow'
    True
    """
    lowered = string.lower()
    try:
        return match_case(string, _exceptional_plurals()[lowered])
    except KeyError:
        pass
    if lowered in _uncountables():
        return string
    if any(map(lowered.endswith, ['ches', 'shes', 'sses'])):
        return string[:-2]
    if _ends_in_consonant_ies(lowered):
        return string[:-3] + 'y'
    if lowered.endswith('s'):
        return string[:-1]  # Chop off 's'.
    raise NotImplementedError("Do not know how to depluralize %r" % string)


def number_name(item):
    """The English name for that number

    >>> assert number_name(5) == 'five'
    """
    number_names = [
        'zero', 'one', 'two', 'three', 'four',
        'five', 'six', 'seven', 'eight', 'nine',
        'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
        'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen',
    ]
    try:
        i = int(item)
        f = float(item)
    except (ValueError, TypeError):
        return item
    if i < 0:
        return 'minus %s' % number_name(-item)
    if f - i:
        return '%s point %s' % (number_name(i), ' '.join(
            number_name(_) for _ in str(f).split('.')[1]))
    if i < 20:
        return number_names[i]
    if i < 100:
        ten = i // 10
        i = i % 10
        tens_names = ['', '', 'twenty', 'thirty', 'forty', 'fifty',
                      'sixty', 'seventy', 'eighty', 'ninety']
        if not i:
            return tens_names[ten]
        return ' '.join((tens_names[ten], number_names[i]))
    if i < 1_000:
        hundred = i // 100
        i = i % 100
        hundred_name = '%s hundred' % number_name(hundred)
        if not i:
            return hundred_name
        return ' and '.join((hundred_name, number_name(i)))
    limits = [
        ('thousand', 1_000),
        ( 'million', 1_000_000),
        ( 'billion', 1_000_000_000),
        ('trillion', 1_000_000_000_000),
        ('quadrillion', 1_000_000_000_000_000),
        ('quintillion', 1_000_000_000_000_000_000),
    ]
    # Some names of large numbers, such as million, billion, and trillion,
    # have real referents in human experience ...
    # Names of larger numbers, however, have a tenuous, artificial existence,
    # rarely found outside definitions, lists, ...
    # https://en.wikipedia.org/wiki/Names_of_large_numbers#Usage_of_names_of_large_numbers
    for limit_name, limit_number in limits:
        too_big = limit_number * 1_000
        if i < too_big:
            prefix = i // limit_number
            i = i % limit_number
            prefix_name = '%s %s' % (number_name(prefix), limit_name)
            if not i:
                return prefix_name
            suffix = number_name(i)
            joiner = ', ' if ' and ' in suffix else ' and '
            return joiner.join((prefix_name, number_name(i)))

    raise ValueError('Too big')
