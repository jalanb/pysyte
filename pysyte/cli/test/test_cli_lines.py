"""Test the lines module"""


import unittest

from pysyte.cli import arguments
from pysyte.cli import lines


class TestPaths(unittest.TestCase):
    """Check that paths are extracted from command line if they exist"""

    def test_add_args(self):
        """Adding args should give a PathParser"""
        actual = lines.add_args(arguments.test_parser())
        self.assertIsInstance(actual, lines.LinesParser)

    def test_parse_short_numbers(self):
        """Parse out line arguments from cli

        Parse a cli with short versions of numeric line options
            Using the format "-f 22"
        """
        parser = lines.add_args(arguments.test_parser())
        parsed = parser.parse(["-a", "3", "-f", "2", "-l", "1"])
        self.assertEqual(parsed.at, 3)
        self.assertEqual(parsed.first, 2)
        self.assertEqual(parsed.last, 1)

    def test_parse_long_numbers(self):
        """Parse out line arguments from cli

        Parse a cli with long versions of numeric line options
            Using the format "--first=22"
        """
        parser = lines.add_args(arguments.test_parser())
        parsed = parser.parse(["--at=3", "--first=2", "--last=1"])
        self.assertEqual(parsed.at, 3)
        self.assertEqual(parsed.first, 2)
        self.assertEqual(parsed.last, 1)

    def test_parse_spaced_long_numbers(self):
        """Parse out line arguments from cli

        Parse a cli with long versions of numeric line options
            Using the format "--first 22"
        """
        parser = lines.add_args(arguments.test_parser())
        parsed = parser.parse(["--numbers", "--width", "2", "--remove", "1"])
        self.assertEqual(parsed.numbers, True)
        self.assertEqual(parsed.width, 2)
        self.assertEqual(parsed.remove, 1)

    def test_parse_files(self):
        """Parse out files from cli"""
        parser = lines.add_args(arguments.test_parser())
        parser.add_files()
        parsed = parser.parse([__file__, "another"])
        self.assertIn(__file__, parsed.files)
        self.assertIn("another", parsed.files)

    def test_version(self):
        """Parse out version from cli

        Showing the version should cause a sys.exit()
        """
        parser = lines.add_args(arguments.test_parser())
        self.assertRaises(SystemExit, parser.parse, ["--version"])
