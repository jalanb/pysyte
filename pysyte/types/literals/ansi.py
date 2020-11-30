"""Handle ANSI colours for pysyte

Colour sequences are derived from the table at

http://en.wikipedia.org/wiki/ANSI_escape_sequences#Colors

"""
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


def highlighted(colour, text):
    return f"{colour}{text}{off}"
