"""Test the literal namespaces"""


import unittest


from dotsite.literals import Punctuation, Digits, Numbers, Empty, Python


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
