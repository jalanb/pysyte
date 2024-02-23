import unittest

import pytest

from pysyte import iteration


def is_one(item):
    return item[0] == 1


class TestFirstThat(unittest.TestCase):
    """iteration.find_first() should return first item matching a predicate

    For tests the predicate is the is_one() method (above)
        that first part of the item is 1

    We test against sequences where this is true of 2 items
        and check that we always get the first one
    """

    def test_find_first(self):
        sequence = [(1, "one"), (2, "two"), (1, "ONE")]
        actual = iteration.first_that(is_one, sequence)
        expected = (1, "one")
        assert actual == expected

    def test_find_second(self):
        sequence = [(2, "two"), (1, "one"), (1, "ONE")]
        actual = iteration.first_that(is_one, sequence)
        expected = (1, "one")
        assert actual == expected

    def test_not_found(self):
        sequence = [(2, "two"), (7, "one"), (8, "ONE")]
        expected = "my message"
        with pytest.raises(KeyError, match=expected):
            iteration.first_that(is_one, sequence, expected)


class TestFirst(unittest.TestCase):
    """iteration.first() should return the only item in a sequence

    It should raise errors if there are no items
    """

    def test_first(self):
        expected = "expected"
        actual = iteration.first([expected])
        assert actual == expected

    def test_exception_on_empty(self):
        expected = "this message"
        with pytest.raises(ValueError, match=expected):
            iteration.first([], expected)

    def test_generator(self):
        def generate():
            while True:
                yield expected

        expected = 1
        actual = iteration.first(generate())
        assert actual == expected


if __name__ == "__main__":
    unittest.main()

