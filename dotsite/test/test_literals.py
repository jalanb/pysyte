"""Test the literal namespaces"""
import unittest


from dotsite.literals import AnsiColourSequences
from dotsite.literals import Digits
from dotsite.literals import Empty
from dotsite.literals import Numbers
from dotsite.literals import Punctuation
from dotsite.literals import Python


class TestLiterals(unittest.TestCase):

    def test_punctuation(self):
        self.assertEqual(Punctuation.dot, Punctuation.period)
        self.assertEqual(Punctuation.dot, Punctuation.full_stop)
        self.assertEqual(Punctuation.apostrophe, Punctuation.single_quote)

    def test_digits(self):
        self.assertEqual(int(Digits.zero), 0)
        self.assertEqual(int(Digits.six + Digits.seven), 67)
        self.assertEqual(Digits.one + Digits.two, Numbers.twelve)

    def test_empty(self):
        self.assertFalse(Empty.string)
        self.assertFalse(Empty.integer)
        self.assertFalse(Empty.real)

    def test_python(self):
        self.assertEqual(Python.name, 'python')
        self.assertEqual(Python.command, 'python')
        self.assertEqual(Python.package, 'python')

    def test_colours(self):
        self.assertEqual(AnsiColourSequences.red.replace('[0', '[1'),
                         AnsiColourSequences.light_red)
        coloured = AnsiColourSequences.highlighted(
            AnsiColourSequences.red, 'Fred')
        self.assertTrue(coloured.startswith(AnsiColourSequences.red))
        self.assertTrue(coloured.endswith(AnsiColourSequences.off))
