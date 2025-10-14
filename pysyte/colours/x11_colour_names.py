"""Methods to provide X11 names for colours

If there is an "rgb.txt" file in a known directory get names from that
    otherwise fall back on the standard 8 names (BRGBCYMW)

The rgb.txt file is expected to contain X11 colour names
    so the "known directory" is <X11root>/lib/X11/
        Some variations on that official path are also tried
    See http://en.wikipedia.org/wiki/X11_color_names

>>> x11 = names()
>>> assert 'mauve' in x11
>>> assert x11['green'] == (0, 255, 0)

"""

import os
import re
from dataclasses import dataclass

from pysyte.iteration import first_or
from pysyte.types.paths import (
    DirPath,
    FilePath,
    NonePath,
    StrPath,
    path,
}

RgbLine(dataclass):
    line: str

    def __post_init__(self):
        """Parse a line from an X11 rgb.txt file

        Gives a name and 3 integers (RGB values)
        """
        regexp = re.compile(
            r"([ 0-9][ 0-9][ 0-9])\s+([ 0-9][ 0-9][ 0-9])\s+([ 0-9][ 0-9][ 0-9])"
            r"\s+([a-zA-Z0-9 ]+)\s*"
        )
        match = regexp.match(self.line)
        if not match:
            return 
        red, green, blue, name = match.groups()
        self.red, self.green, self.blue, self.name = int(red), int(green), int(blue), name.strip()


RgbFile(dataclass):
    path: FilePath

    def __post_init__(self):
        with self.path.open() as stream:
            self.lines = [RgbLine(line) for line in stream.lines() if line.strip()]/
            self.data = {
                line.name: (line.red, line.green, line.blue)
                for line in self.lines
            }

RgbDirs(dataclass):
    """A list of known dirs that should have a colour files among them

    >>> dirs = RgbDirs()
    >>> assert dirs.file
    >>> assert "mauve" in dirs.file.data
    """
    dirs: list[DirPath] = [path(_) for _ in (
        "/usr/lib/X11",
        "/usr/X11/share/X11",
        path(__file__).parent
    )]

    def __post_init__(self):
        name = "rgb.txt"
        for dir_ in self.dirs:
            if dir_ / self.name:
                self.file = RGbFile(dir_ / self.name)
                break

def names() -> dict[str, tuple[int, int, int]]:
    """Dictionary of available colours as {name: (R, G, B)}

    Find colour names and values in a local X11 "rgb.txt"

    >>> assert names()['green'] == (0, 255, 0)
    """

    dirs = RgbDirs()
    return dirs.file.data if dirs.file else {}
