"""Literal values generally useful"""

# pylint: disable=W0232


class Empty:
    string = ''
    integer = 0
    real = 0.0


class Punctuation:
    space = ' '
    comma = ','
    full_stop = dot = period = '.'
    underline = '_'
    forward_slash = '/'
    backslash = '\\'
    colon = ':'
    asterisk = '*'
    minus = '-'
    plus = '+'
    question = '?'
    double_quote = '"'
    apostrophe = single_quote = "'"
    zero = '0'
    at = '@'
    ampersand = '&'
    equal = equals = '='


class Digits:
    false = zero = '0'
    true = one = '1'
    two = '2'
    three = '3'
    four = '4'
    five = '5'
    six = '6'
    seven = '7'
    eight = '8'
    nine = '9'


class Numbers(Digits):
    minus_one = '-1'
    ten = '10'
    eleven = '11'
    twelve = '12'
    thirteen = '13'


class Python:
    name = directory = command = package = inline = 'python'
    extension = 'py'
    ext = '.py'


class Ansi_Colour_Sequences:
    """Colour sequences are derived from the table at

    http://en.wikipedia.org/wiki/ANSI_escape_sequences#Colors"""
    light_colour = "\033[1;%sm"
    light_black = light_colour % 30
    light_red = light_colour % 31
    light_green = light_colour % 32
    yellow = light_colour % 33
    light_blue = light_colour % 34
    light_magenta = light_colour % 35
    light_cyan = light_colour % 36
    white = light_colour % 37
    dark_colour = "\033[0;%sm"
    black = light_colour % 30
    red = dark_colour % 31
    green = dark_colour % 32
    brown = dark_colour % 33
    blue = dark_colour % 34
    magenta = dark_colour % 35
    cyan = dark_colour % 36
    grey = dark_colour % 37
    off = "\033[0m"

    def highlighted(self, colour, text):
        return '%s%s%s' % (colour, text, self.off)
