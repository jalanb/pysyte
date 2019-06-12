"""This module provides some known ANSI escape codes which work with terminals

All numbers used in this file are values usable in an ANSI escape sequence
    See http://en.wikipedia.org/wiki/ANSI_escape_code for values
"""


def escape(string):
    return f'\033{string}'


def escape_sequence(string):
    return escape(f'[{string}m')


def bold():
    return escape_sequence('1')


def no_bold():
    return escape_sequence('22')


def no_colour():
    return escape_sequence('2') + escape_sequence('0')


def no_prompt():
    return prompt(no_colour())


def _colour_16(ground, i):
    if i > 7:
        prefix = bold()
        i = i - 8
    else:
        prefix = ''
    escaped = escape(f'[{ground}{i}m')
    return f'{prefix}{escaped}'


def _colour_256(ground, i):
    return escape_sequence(f'{ground};5;{i}')


def _background_16(i):
    return _colour_16(4, i)


def _background_256(i):
    return _colour_256(48, i)


def _foreground_16(i):
    return _colour_16(3, i)


def _foreground_256(i):
    return _colour_256(38, i)


def _small_colour_number(i):
    return i < 16


def foreground(i):
    return _small_colour_number(i) and _foreground_16(i) or _foreground_256(i)


def background(i):
    return _small_colour_number(i) and _background_16(i) or _background_256(i)


def prompt(string):
    return f'\001{string}\002'


def foreground_string(text, i):
    return f'{foreground(i)}{text}{no_colour()}'


def background_string(text, i):
    return f'{background(i)}{text}{no_colour()}'


def grounds_string(text, background_colour, foreground_colour):
    return '%s%s%s%s' % (
        background(background_colour),
        foreground(foreground_colour),
        text,
        no_colour())


def prompt_string(text, i):
    string = foreground(i)
    return f'{prompt(string)}{text}{no_prompt()}'
