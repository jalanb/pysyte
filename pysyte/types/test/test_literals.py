"""Test the literal namespaces"""
import unittest


from pysyte.types.literals import ansi
from pysyte.types.literals import digits
from pysyte.types.literals import numbers
from pysyte.types.literals import punctuation


class TestLiterals(unittest.TestCase):

    def test_punctuation(self):
        self.assertEqual(punctuation.dot, punctuation.period)
        self.assertEqual(punctuation.dot, punctuation.full_stop)
        self.assertEqual(punctuation.apostrophe, punctuation.single_quote)

    def test_digits(self):
        self.assertEqual(int(digits.zero), 0)
        self.assertEqual(int(digits.six + digits.seven), 67)
        self.assertEqual(digits.one + digits.two, numbers.twelve)

    def test_colours(self):
        self.assertEqual(ansi.red.replace('[0', '[1'),
                         ansi.light_red)
        coloured = ansi.highlighted(
            ansi.red, 'Fred')
        self.assertTrue(coloured.startswith(ansi.red))
        self.assertTrue(coloured.endswith(ansi.off))
