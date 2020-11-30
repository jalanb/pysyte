"""Test the paths module"""


import unittest


from pysyte.cli import paths
from pysyte.cli import arguments
from pysyte.types.paths import path


class TestPaths(unittest.TestCase):
    """Check that paths are extracted from command line if they exist"""

    def test_add_args(self):
        """Adding args should give a PathParser"""
        actual = paths.add_args(arguments.test_parser())
        self.assertTrue(isinstance(actual, paths.PathParser))

    def test_parse(self):
        """Parse out paths from cli

        Parse a cli with some known paths
            They should come back in the "paths" argument
        Anything else (not a real path) comes back in the "not_paths" argument
        """
        parser = paths.add_args(arguments.test_parser())
        path_to_test = path(__file__)
        path_to_tests = path_to_test.parent
        parsed = parser.parse([path_to_test, path_to_tests, "another"])
        self.assertIn(path_to_test, parsed.paths)
        self.assertIn(path_to_tests, parsed.paths)
        self.assertNotIn("another", parsed.paths)
        self.assertIn("another", parsed.not_paths)

    def test_named_parse(self):
        """CHeck that the paths argument can be named differently"""
        parser = paths.add_args(arguments.test_parser(), "fred")
        path_to_test = path(__file__)
        parsed = parser.parse([path_to_test, "another"])
        self.assertIn(path_to_test, parsed.fred)
        self.assertNotIn("another", parsed.fred)
        self.assertIn("another", parsed.not_fred)
