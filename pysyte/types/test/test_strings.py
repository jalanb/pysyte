from unittest import TestCase

from pysyte import randoms
from pysyte.types.strings import Stringer


class TestStringer(TestCase):
    """Stringer cannot be used straightforwardly

    Because it does not implement the __str__() function
    """

    def test_str(self):
        string = Stringer()
        with self.assertRaises(NotImplementedError):
            _ = str(string)


class Child(Stringer):
    """This class provides __str__()

    So should get all the extras provided by Stringer
    """

    def __init__(self, string: str):
        self.string = string

    def __str__(self) -> str:
        return self.string


class TestChildOfStringer(TestCase):
    def test_repper(self):
        child = Child("Hello")
        assert repr(child) == '<Child "Hello">'

    def test_equals(self):
        child = Child("Hello")
        kiddy = Child("Hello")
        assert child == kiddy
        assert kiddy == child

    def test_equal_string(self):
        child = "Hello"
        kiddy = Child("Hello")
        assert child == kiddy
        assert kiddy == child

    def test_not_equal(self):
        child = Child("Hello")
        kiddy = Child("World")
        assert child != kiddy
        assert kiddy != child

    def test_not_equal_string(self):
        child = "Hello"
        kiddy = Child("World")
        assert child != kiddy
        assert kiddy != child

    def test_hash(self):
        child = Child("Hello")
        assert hash(child) == hash("Hello")

    def test_less(self):
        low = Child("aaa")
        high = Child("zzz")
        assert low < high

    def test_greater(self):
        low = Child("aaa")
        high = Child("zzz")
        assert high > low

    def test_less_equal(self):
        low = Child("aaa")
        high = Child("aaa" if randoms.flip() else "zzz")
        assert low <= high

    def test_greater_equal(self):
        low = Child("aaa")
        high = Child("aaa" if randoms.flip() else "zzz")
        assert high >= low
