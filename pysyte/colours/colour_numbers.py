"""Convert between some numbers known to represent colours

Methods handle two known representations:
    1) hex RGB
        Methods are provided for strings like "0xFF0000" (for red)
            and the equivalent numbers
        See http://en.wikipedia.org/wiki/Web_colors#Shorthand_hexadecimal_form
    2) ANSI
        Convert RGB to ANSI values
        See http://en.wikipedia.org/wiki/ANSI_escape_code#Colors
"""


import re

from pysyte.colours import colour_names


def integer_to_ansi(integer):
    if integer < 16:
        return integer

    def rgb_to_decimal(i):
        i -= 0x10
        if i < 0:
            return 0
        return i // 40

    def grey_shade(red, green, blue):
        for i in red, green, blue:
            if (i - 8) % 10:
                return False
        return 232 + ((red - 8) // 10)

    red = (integer & 0xFF0000) >> 16
    green = (integer & 0x00FF00) >> 8
    blue = integer & 0x0000FF
    result = grey_shade(red, green, blue)
    if result:
        return result
    red = rgb_to_decimal(red)
    green = rgb_to_decimal(green)
    blue = rgb_to_decimal(blue)
    return (red * 36) + (green * 6) + blue + 16


def ansi_to_red_green_blue(ansi):
    a = ansi
    assert 231 >= a >= 16
    red, green, blue = ((a - 16) / 36) % 6, ((a - 16) / 6) % 6, (a - 16) % 6

    def decimal_to_rgb(i):
        if not i:
            return 0
        return int((i * 40) + 55)

    return decimal_to_rgb(red), decimal_to_rgb(green), decimal_to_rgb(blue)


def red_green_blue_to_int(red, green, blue):
    assert 0 <= red < 512
    assert 0 <= blue < 512
    assert 0 <= green < 512, green
    return (red << 16) + (green << 8) + blue


def _hex_regexp():
    return re.compile("(([0-9a-f]{6})|([0-9a-f]{3}))", re.IGNORECASE)


def _extract_html_hex(string):
    """Get the first 3 or 6 hex digits in the string"""
    try:
        hex_string = string and _hex_regexp().search(string).group(0) or ""
    except AttributeError:
        return None
    if len(hex_string) == 3:
        hex_string = hex_string[0] * 2 + hex_string[1] * 2 + hex_string[2] * 2
    return hex_string


def html_to_int(string):
    """Use the first 3 or 6 hex digits in the string as a html colour picker"""
    hex_string = _extract_html_hex(string)
    if hex_string is None:
        return None
    if not hex_string:
        return 0
    return int(hex_string, 16)


def html_to_html(string):
    digits = string.lstrip("#").upper()
    if len(digits) == 3:
        return "".join([d * 2 for d in digits])
    return digits


def hashed_html(string):
    return f"#{html_to_html(string)}"


def html_to_red_green_blue(string):
    string = _extract_html_hex(string)
    if not string:
        return None, None, None
    return int(string[:2], 16), int(string[2:4], 16), int(string[4:], 16)


def integer_to_html(integer):
    return "#%06X" % integer


def html_to_ansi(string):
    i = html_to_small_ansi(string)
    if i is not None:
        return i
    i = html_to_int(string)
    return integer_to_ansi(i)


def ansi_to_int(ansi):
    if ansi <= 16:
        return ansi
    elif ansi > 231:
        i = ansi - 232
        r = g = b = (i * 10) + 8
    else:
        r, g, b = ansi_to_red_green_blue(ansi)
    return red_green_blue_to_int(r, g, b)


def small_values():
    return [
        (0x00, "#000000"),
        (0x01, "#800000"),
        (0x02, "#008000"),
        (0x03, "#808000"),
        (0x04, "#000080"),
        (0x05, "#800080"),
        (0x06, "#008080"),
        (0x07, "#C0C0C0"),
        (0x08, "#808080"),
        (0x09, "#FF0000"),
        (0x0A, "#00FF00"),
        (0x0B, "#FFFF00"),
        (0x0C, "#0000FF"),
        (0x0D, "#FF00FF"),
        (0x0E, "#00FFFF"),
        (0x0F, "#000000"),
    ]


def small_integers():
    return [integer for integer, _html in small_values()]


def small_ansi_to_html(i):
    for ansi, html in small_values():
        if i == ansi:
            return html
    return None


def html_to_small_ansi(string):
    hashed = hashed_html(string)
    for ansi, html in small_values():
        if html == hashed:
            return ansi
    return None


def ansi_to_html(ansi):
    if ansi < 16:
        return small_ansi_to_html(ansi)
    i = ansi_to_int(ansi)
    return integer_to_html(i)


def name_to_id(name):
    """Get a number for that colour name

    if not a name, then not a number

    >>> assert name_to_id("red") == 1
    """
    if not name:
        return None
    lower = name.lower()
    cga_names = {s: i for i, s in enumerate(colour_names.cga())}
    return cga_names.get(lower) or html_to_small_ansi(lower)


def id_to_name(i):
    """get the name of the colour with that id

    >>> assert id_to_name(1) == "red"
    """
    assert i >= 0
    cgas = colour_names.cga()
    if i < len(cgas):
        return cgas[i].lower()
    return ansi_to_html(i)
