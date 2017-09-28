"""Test the term module"""


import unittest


from dotsite import term


class TestTerm(unittest.TestCase):
    def test_height(self):
        height = term.screen_height()
        self.assertTrue(isinstance(height, int))
        self.assertTrue(height > 10)

    def test_width(self):
        width = term.screen_width()
        self.assertTrue(isinstance(width, int))
        self.assertTrue(width > 10)
