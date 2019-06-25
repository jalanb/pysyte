"""Test the term module"""


import unittest


from pysyte.cli import arguments


class TestExtractStrings(unittest.TestCase):
    def test_a_string(self):
        """A single string gets extracted as a list"""
        data = {'fred': 'string'}
        expected = ['string']
        actual = arguments.extract_strings(data, 'fred')
        self.assertEqual(expected, actual)

    def test_strings(self):
        """A list of strings gets extracted as-is"""
        data = {'fred': ['one', 'two']}
        expected = ['one', 'two']
        actual = arguments.extract_strings(data, 'fred')
        self.assertEqual(expected, actual)

    def test_missing_strings(self):
        """No strings gets extracted as an empty list"""
        data = {'fred': ['one', 'two']}
        expected = []
        actual = arguments.extract_strings(data, 'mary')
        self.assertEqual(expected, actual)

    def test_ignore_non_strings(self):
        """Non-strings are ignored in lists"""
        data = {'fred': [1, 'two']}
        expected = ['two']
        actual = arguments.extract_strings(data, 'fred')
        self.assertEqual(expected, actual)

    def test_ignore_uniterables(self):
        """Non-iterables are ignored"""
        data = {'fred': 1}
        expected = []
        actual = arguments.extract_strings(data, 'fred')
        self.assertEqual(expected, actual)
