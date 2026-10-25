"""Test the literal namespaces"""

import unittest

from pysyte.types.literals import ansi, digits, numbers, punctuation


class TestLiterals(unittest.TestCase):
    def test_punctuation(self) -> None:
        self.assertEqual(punctuation.dot, punctuation.period)
        self.assertEqual(punctuation.dot, punctuation.full_stop)
        self.assertEqual(punctuation.apostrophe, punctuation.single_quote)

    def test_digits(self) -> None:
        self.assertEqual(int(digits.zero), 0)
        self.assertEqual(int(digits.six + digits.seven), 67)
        self.assertEqual(digits.one + digits.two, numbers.twelve)

    def test_colours(self) -> None:
        self.assertEqual(ansi.red.replace("[0", "[1"), ansi.light_red)
        coloured = ansi.highlighted(ansi.red, "Fred")
        self.assertTrue(coloured.startswith(ansi.red))
        self.assertTrue(coloured.endswith(ansi.off))
