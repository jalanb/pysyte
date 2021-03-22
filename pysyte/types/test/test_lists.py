from unittest import TestCase

from pysyte.types import lists


class TestAsList(TestCase):

    def test_as_list(self):
        """list in, list out"""
        actual = lists.as_list([1, 2, 3])
        expected = [1, 2, 3]
        self.assertEqual(actual, expected)

    def test_tuple_as_list(self):
        """set in, list out"""
        expected = [1, 2, 3]
        actual = lists.as_list((1, 2, 3))
        self.assertEqual(actual, expected)

    def test_set_as_list(self):
        """set in, list out"""
        expected = [1, 2, 3]
        actual = lists.as_list({1, 2, 3})
        self.assertEqual(actual, expected)

    def test_dict_as_list(self):
        """dict in, list of items out"""
        expected = [(1, 4), (2, 5), (3, 6)]
        actual = lists.as_list({1:4, 2:5, 3:6})
        self.assertEqual(actual, expected)

    def test_string_as_list(self):
        """string in, list of chars out"""
        expected = ["f", "r", "e", "d"]
        actual = lists.as_list("fred")
        self.assertEqual(actual, expected)

    def test_int_as_list(self):
        """Tring to turn a non-sequence to a list raise error"""
        self.assertRaises(TypeError, lists.as_list, 999)
