"""Test the term module"""


import unittest


from pysyte import term


class TestTerm(unittest.TestCase):
    def test_height(self):
        try:
            height = term.screen_height()
        except term.NoTerminalAvailable:
            return
        self.assertTrue(isinstance(height, int))
        self.assertTrue(height > 10)

    def test_width(self):
        try:
            width = term.screen_width()
        except term.NoTerminalAvailable:
            return
        self.assertTrue(isinstance(width, int))
        self.assertTrue(width > 10)
