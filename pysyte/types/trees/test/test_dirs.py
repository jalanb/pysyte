import os
from unittest import TestCase

from pysyte.types.trees import dirs
from pysyte.types.trees import paths

class TestHere(TestCase):
    def test_here(self):
        assert dirs.here().isdir()
        assert dirs.here() == os.getcwd()


class TestCD(TestCase):

    def test_cd_back(self):
        dirs.cd.previous = None
        dirs.cd("/usr")
        dirs.cd("/usr/local")
        dirs.cd("-")
        self.assertEqual(paths.pwd(), "/usr")

    def test_cd_back_without_previous(self):
        dirs.cd.previous = None
        self.assertRaises(paths.PathError, dirs.cd, "-")

    def test_cd_nowhere(self):
        self.assertFalse(dirs.cd("/path/to/nowhere"))
