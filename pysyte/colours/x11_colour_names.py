"""Methods to provide X11 names for colours

If there is an "rgb.txt" file in a known directory get names from that
    otherwise fall back on the standard 8 names (BRGBCYMW)

The rgb.txt file is expected to contain X11 colour names
    so the "known directory" is <X11root>/lib/X11/
        Some variations on that official path are also tried
    See http://en.wikipedia.org/wiki/X11_color_names
"""

import os
import re


def names():
    """Dictionary of available colours as {name: (R, G, B)}

    Find colour names and values in a local X11 "rgb.txt"

    >>> assert names()['green'] == (0, 255, 0)
    """

    def rgb_txt_directories():
        """List of directories which should contain rgb.txt

        Look in <X11root>/lib/X11/rgb.txt first
            then <X11root>/X11/share
            then in runtime directory
            then in same dir as this file
        """
        dirs = [
            "/usr/lib/X11",
            "/usr/X11/share/X11",
            ".",
            os.path.dirname(__file__),
        ]
        return dirs

    def first_rgb_file(rgb_txt_paths):
        """The first rgb.txt file in known directories"""
        for path in rgb_txt_paths():
            path_to_txt_file = os.path.join(path, "rgb.txt")
            if os.path.isfile(path_to_txt_file):
                return path_to_txt_file
        return None

    def rgb_txt_names_and_numbers(path_to_file) -> dict:
        """Parse all lines from that file"""

        def rgb_txt_line(string):
            """Parse a line from an X11 rgb.txt file

            Gives a name and 3 integers (RGB values)
            """
            regexp = re.compile(
                r"([ 0-9][ 0-9][ 0-9])\s+([ 0-9][ 0-9][ 0-9])\s+([ 0-9][ 0-9][ 0-9])"
                r"\s+([a-zA-Z0-9 ]+)\s*"
            )
            match = regexp.match(string)
            if not match:
                return "", (-1, -1, -1)
            red, green, blue, name = match.groups()
            return name.strip(), (int(red), int(green), int(blue))

        if not path_to_file or not os.path.isfile(path_to_file):
            return []
        rgb_lines = [rgb_txt_line(_) for _ in open(path_to_file)]
        return {
            name: values for name, values in rgb_lines if name
        }

    path_to_rgb_txt = first_rgb_file(rgb_txt_directories())
    return rgb_txt_names_and_numbers(path_to_rgb_txt)
