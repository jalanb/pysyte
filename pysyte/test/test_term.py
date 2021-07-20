"""Test the term module"""


import unittest


from pysyte import term


class TestTerm(unittest.TestCase):
    def test_height(self):
        try:
            height = term.screen_height()
        except term.NoTerminalAvailable:
            return
        self.assertIsInstance(height, int)
        self.assertGreater(height, 10)

    def test_width(self):
        try:
            width = term.screen_width()
        except term.NoTerminalAvailable:
            return
        self.assertIsInstance(width, int)
        self.assertGreater(width, 10)
