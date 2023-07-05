"""Check all imports in the package

Find *.py under the package
    find all import lines in each file, and execute them
"""

# "noqa": This imports a lot of unused modules just for testing with


import os  # noqa: F401
import unittest
from collections import defaultdict  # noqa: F401

from pysyte import importers


class TestDashboardImports(unittest.TestCase):
    def setUp(self):
        source = __file__.replace(".pyc", ".py")  # just in case
        self.visitor = importers.parse(source)

    def test_import_count(self):
        """Check that we can find imports in a file

        Simple check - just make sure we can count imports here
        Adding some unusual imports in this test
            to make sure getting more than top-level imports
            and can handle the edge-cases
        """
        import os, sys as system  # noqa: F811, F401, E401
        from os import path, kill as killer  # noqa: F401

        self.assertEqual(len(self.visitor.imports), 7)
        self.assertEqual(len(self.visitor.froms), 3)
        self.assertEqual(len(self.visitor.used), 2)

    def test_redundant_imports(self):
        self.assertEqual(
            set(self.visitor.unused().keys()),
            {"defaultdict", "system", "killer", "path", "os"},
        )

    def test_multiples(self):
        """Check that multiple imports of 'os' are found

        They are on lines 10 and 30
        """
        multiples = self.visitor.multiples()
        self.assertEqual(list(multiples.keys()), ["os"])
        self.assertEqual(multiples["os"], [10, 30])

    def test_redundant_has_line_numbers(self):
        """Check that each module entry in unused imports has a line numbers

        We will only test here for the first line number
            See above to verify
        """
        redundant = self.visitor.unused()
        self.assertEqual(redundant["system"][0], 30)
        self.assertEqual(redundant["killer"][0], 31)

    def test_redundant_lines(self):
        """The unused_lines() gives a dict keyed by line number

        With values for all redundant modules imported on that line
            See above to verify
        """
        lines = self.visitor.unused_lines()
        assert 'os' in lines[10]
        assert 'system' in lines[30]
        assert 'killer' in lines[31]


class TestErrorImports(unittest.TestCase):
    def test_handles_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            importers.parse("/not/a/file")
