"""Check all imports in the dashboard package

Find *.py under the dashboard package
    find all import lines in each file, and execute them
"""

import os
import unittest
from collections import defaultdict

from dotsite import imports


class TestDashboardImports(unittest.TestCase):
    def setUp(self):
        source = __file__.replace('.pyc', '.py')  # just in case
        self.visitor = imports.extract_imports(source)

    def test_import_count(self):
        """Check that we can find imports in a file

        Simple check - just make sure we can count imports here
        Adding some unusual imports in this test
            to make sure getting more than top-level imports
            and can handle the edge-cases
        """
        import os, sys
        from os import (path,
                        kill)
        self.assertEqual(len(self.visitor.imports), 7)
        self.assertEqual(len(self.visitor.froms), 3)
        self.assertEqual(len(self.visitor.used), 2)

    def test_redundant_imports(self):
        self.assertEqual(
            set(self.visitor.unused().keys()),
            {'defaultdict', 'sys', 'kill', 'path', 'os'})

    def test_mutiples(self):
        """Check that mutiple imports of 'os' are found

        They are on lines 7 and 27
        """
        self.assertEquals(self.visitor.mutiples().keys(), ['os'])
        self.assertEquals(self.visitor.mutiples()['os'], [7, 27])

    def test_redundant_lines(self):
        redundant = self.visitor.unused()
        self.assertEqual(redundant['sys'][0], 27)
        self.assertEqual(redundant['kill'][0], 28)


if __name__ == '__main__':
    unittest.main()
