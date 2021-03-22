"""Handle Freds for pysyte

"If in doubt, name it Fred"
"""

from dataclasses import dataclass

from pysyte.types import paths


@dataclass
class FredsData:
    dirs: list


class Freds(FredsData):
    """Handle fred.* as strings, paths, files, ..."""

    def extended(self):
        exts = ("", ".py", ".sh", ".txt", ".now", ".html", ".xlsx", ".csv")
        return [str("%s/fred%s" % (d, e)) for d in self.dirs for e in exts]

    def _paths(self):
        return [paths.path(_) for _ in self.extended()]

    def _files(self):
        return [_ for _ in self._paths() if _.isfile()]

    def sized(self):
        return set(_ for _ in self._files() if _.size)

    def zero_sized(self):
        return [_ for _ in self._files() if not _.size]

    def remove_empties(self):
        return [_.remove() for _ in self.zero_sized()]
