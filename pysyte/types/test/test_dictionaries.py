"""Test the dictionaries module"""


import unittest

from pysyte.types import dictionaries


class DictionariesTest(unittest.TestCase):
    def test_get_caselessly(self):
        things = {"Fred": 9, "A": 1, "b": 2}
        self.assertEqual(9, dictionaries.get_caselessly(things, "fred"))

    def test_get_lower_caselessly(self):
        things = {"Fred": 9, "A": 1, "b": 2}
        self.assertEqual(2, dictionaries.get_caselessly(things, "B"))

    def test_get_upper_caselessly(self):
        things = {"Fred": 9, "A": 1, "b": 2}
        self.assertEqual(1, dictionaries.get_caselessly(things, "a"))

    def test_do_not_get_caselessly(self):
        things = {"Fred": 9, "A": 1, "b": 2}
        with self.assertRaises(KeyError):
            dictionaries.get_caselessly(things, "free")

    def test_swap(self):
        pythons = {"John": "Cleese", "Graham": "Chapman", "Eric": "Idle"}
        expected = {"Cleese": "John", "Chapman": "Graham", "Idle": "Eric"}
        actual = dictionaries.swap_dictionary(pythons)
        self.assertEqual(expected, actual)

    def test_swap_empty_dictionary(self):
        actual = dictionaries.swap_dictionary({})
        expected = {}
        self.assertEqual(expected, actual)

    def test_swap_none(self):
        expected = None
        actual = dictionaries.swap_dictionary(None)
        self.assertEqual(expected, actual)

    def test_swap_not_a_dictionary(self):
        with self.assertRaises(AttributeError):
            dictionaries.swap_dictionary("not a dict")

    def test_append_value(self):
        dictionary = {}
        data = [
            ("one", 1, {"one": [1]}),
            ("one", 2, {"one": [1, 2]}),
            ("two", 2, {"one": [1, 2], "two": [2]}),
            ("one", 3, {"one": [1, 2, 3], "two": [2]}),
            ("one", None, {"one": [1, 2, 3, None], "two": [2]}),
        ]
        for key, value, expected in data:
            dictionaries.append_value(dictionary, key, value)
            message = "append(%s, %s): %s != %s" % (
                key,
                value,
                expected,
                dictionary,
            )
            self.assertDictEqual(dictionary, expected, message)

    def test_extend_values(self):
        dictionary = {}
        data = [
            ("one", [1], {"one": [1]}),
            ("one", [2, 3], {"one": [1, 2, 3]}),
            ("two", [2, 3], {"one": [1, 2, 3], "two": [2, 3]}),
            ("one", [2, 3], {"one": [1, 2, 3, 2, 3], "two": [2, 3]}),
        ]
        for key, value, expected in data:
            dictionaries.extend_values(dictionary, key, value)
            message = "extend(%s, %s): %s != %s" % (
                key,
                value,
                expected,
                dictionary,
            )
            self.assertDictEqual(dictionary, expected, message)

    def test_extend_with_non_list(self):
        self.assertRaisesRegex(
            TypeError,
            "Expected a list, got: 2",
            dictionaries.extend_values,
            {},
            "one",
            2,
        )
