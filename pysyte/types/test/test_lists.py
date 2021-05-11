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
        actual = lists.as_list({1: 4, 2: 5, 3: 6})
        self.assertEqual(actual, expected)

    def test_string_as_list(self):
        """string in, list of chars out"""
        expected = ["f", "r", "e", "d"]
        actual = lists.as_list("fred")
        self.assertEqual(actual, expected)

    def test_int_as_list(self):
        """Tring to turn a non-sequence to a list raise error"""
        self.assertRaises(TypeError, lists.as_list, 999)


class TestUniques(TestCase):
    def test_uniqueness(self):
        """Duplicate items should be ignored"""
        expected = [1, 3, 2, 0]
        actual = list(lists.Uniques([1, 1, 3, 1, 2, 3, 0]))
        self.assertEqual(actual, expected)

    def test_appending_new(self):
        """New items should be appended"""
        expected = [1, 3, 2, 0, 4]
        uniques = lists.Uniques([1, 1, 3, 1, 2, 3, 0])
        uniques.append(4)
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_appending_old(self):
        """Duplicate items should not be appended"""
        expected = [1, 3, 2, 0]
        uniques = lists.Uniques([1, 1, 3, 1, 2, 3, 0])
        uniques.append(3)
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_extending_new(self):
        """New items should be extended"""
        expected = [1, 3, 2, 0, 4, 5]
        uniques = lists.Uniques([1, 1, 3, 1, 2, 3, 0])
        uniques.extend([4, 5])
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_extending_set(self):
        """A set of new items should be extended"""
        expected = [1, 3, 2, 0, 4, 5]
        uniques = lists.Uniques([1, 1, 3, 1, 2, 3, 0])
        uniques.extend({4, 5})
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_extending_dict(self):
        """A dict of new items should be extended with the keys"""
        expected = [1, 3, 2, 0, 4, 5]
        uniques = lists.Uniques([1, 1, 3, 1, 2, 3, 0])
        uniques.extend({4: 0, 5: 0})
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_extending_old(self):
        """Duplicate items should not be extended"""
        expected = [1, 3, 2, 0, 4]
        uniques = lists.Uniques([1, 1, 3, 1, 2, 3, 0])
        uniques.extend([2, 3, 4])
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_extending_empty(self):
        """Extending with an empty list does nothing"""
        expected = [1, 3, 2, 0]
        uniques = lists.Uniques([1, 1, 3, 1, 2, 3, 0])
        uniques.extend([])
        actual = list(uniques)
        self.assertEqual(actual, expected)


class TestUniquelyTrues(TestCase):
    def test_uniqueness(self):
        """Duplicate and false items should be ignored"""
        expected = [1, 3, 2]
        actual = list(lists.UniquelyTrues([1, 1, 3, 1, 2, 3, 0]))
        self.assertEqual(actual, expected)

    def test_appending_new(self):
        """New items should be appended"""
        expected = [1, 3, 2, 4]
        uniques = lists.UniquelyTrues([1, 1, 3, 1, 2, 3, 0])
        uniques.append(4)
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_appending_old(self):
        """Duplicate items should not be appended"""
        expected = [1, 3, 2]
        uniques = lists.UniquelyTrues([1, 1, 3, 1, 2, 3, 0])
        uniques.append(3)
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_appending_false(self):
        """False items should not be appended"""
        expected = [1, 3, 2]
        uniques = lists.UniquelyTrues([1, 1, 3, 1, 2, 3])
        uniques.append(0)
        uniques.append(None)
        uniques.append(False)
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_extending_new(self):
        """New items should be extended

        Items do not all have to have same type
        """
        expected = [1, 3, 2, 4, "9"]
        uniques = lists.UniquelyTrues([1, 1, 3, 1, 2, 3, 0])
        uniques.extend([4, "9"])
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_extending_old(self):
        """Duplicate items should not be extended"""
        expected = [1, 3, 2, 9]
        uniques = lists.UniquelyTrues([1, 1, 3, 1, 2, 3, 0])
        uniques.extend([3, 9])
        actual = list(uniques)
        self.assertEqual(actual, expected)

    def test_extending_false(self):
        """False items should not be extended"""
        expected = [1, 3, 2, 9]
        uniques = lists.UniquelyTrues([1, 1, 3, 1, 2, 3])
        uniques.extend([0, 9])
        actual = list(uniques)
        self.assertEqual(actual, expected)
