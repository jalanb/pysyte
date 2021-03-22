"""Handle colours for screens and walls"""

from pysyte.colours import colour_numbers


class Colour(object):
    def __init__(self, name):
        self._id = colour_numbers.name_to_id(name)
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
