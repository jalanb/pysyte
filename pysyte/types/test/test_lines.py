from random import randint
from unittest import TestCase
from unittest.mock import patch

from pysyte.randoms import flip
from pysyte.types import lines


class TestLines(TestCase):
    def test_set_width(self):
        line = "01234567890123456789"
        expected = "012345678901234"
        actual = lines.set_width(line, 15)
        self.assertEqual(actual, expected)

    def test_set_no_width(self):
        line = "01234567890123456789"
        expected = line
        actual = lines.set_width(line, None)
        self.assertEqual(actual, expected)

    def test_add_numbers(self):
        """add_numbers() should prefix each line with count

        counts start at 1, not 0
        default prefix is follwed by ": "
        """
        lines_ = [
            "one",
            "two",
            "three",
        ]
        expected = [
            "1: one",
            "2: two",
            "3: three",
        ]
        actual = list(lines.add_numbers(lines_))
        self.assertEqual(actual, expected)

    def test_add_numbers_offset(self):
        """add_numbers() should prefix each line with count

        counts start at the given number plus 1
        default prefix is follwed by ": "
        """
        lines_ = [
            "one",
            "two",
            "three",
        ]
        expected = [
            "3: one",
            "4: two",
            "5: three",
        ]
        actual = list(lines.add_numbers(lines_, 2))
        self.assertEqual(actual, expected)

    def test_add_over_10_numbers(self):
        """add_numbers() should prefix each line with count

        If total number of lines is over 2 digits,
            then all prefixes should shift right
        """
        text = "one,two,three,four,five,six,seven,eight,nine,ten,eleven"
        lines_ = text.split(",")
        actuals = list(lines.add_numbers(lines_, 0))
        expected = " 2: two"
        actual = actuals[1]
        self.assertEqual(actual, expected)
        expected = "10: ten"
        actual = actuals[9]
        self.assertEqual(actual, expected)

    def test_select(self):
        """select() chooses lines"""
        text = "one,two,three,four,five,six,seven,eight,nine,ten,eleven"
        lines_ = text.split(",")
        actual = list(lines.select(lambda x: "o" in x, lines_))
        expected = [
            "one",
            "two",
            "four",
        ]
        self.assertEqual(actual, expected)

    def test_as_text(self):
        """as_text() joins lines into text"""
        text = "one,two,three,four,five,six,seven,eight,nine,ten,eleven"
        lines_ = text.split(",")
        self.assertEqual(lines_[0], "one")
        expected = "one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten\neleven"
        actual = lines.as_text(lines_)
        self.assertEqual(actual, expected)

    def test_reformat_lines(self):
        """reformat_lines() sets width, and can prefix line numbers"""
        text = "one,two,three,four,five"
        lines_ = text.split(",")
        expected = [
            "one",
            "two",
            "thr",
            "fou",
            "fiv",
        ]
        actual = lines.reformat_lines(lines_, first=7, numbers=False, width=3)
        self.assertEqual(actual, expected)

    def test_reformat_lines_with_low_numbers(self):
        """reformat_lines() can prefix line numbers"""
        text = "one,two,three,four,five"
        lines_ = text.split(",")
        expected = [
            "1: one",
            "2: two",
            "3: three",
            "4: four",
            "5: five",
        ]
        actual = lines.reformat_lines(lines_, first=0, numbers=True, width=0)
        self.assertEqual(actual, expected)

    def test_reformat_lines_with_high_numbers(self):
        """reformat_lines() sets width, and can prefix line numbers"""
        text = "one,two,three,four,five"
        lines_ = text.split(",")
        # start counting lines at index 6 (aka line number 7)
        # so highest line number is 11, so all line numbers have width of 2
        expected = [
            " 7: one",
            " 8: two",
            " 9: thr",
            "10: fou",
            "11: fiv",
        ]
        actual = lines.reformat_lines(lines_, first=6, numbers=True, width=3)
        self.assertEqual(actual, expected)

    @patch("pysyte.types.lines.chop")
    def test_arg_lines(self, chop):
        """arg_lines() is a convenience method for chop()

        It just extracts expected args then calls chop
        """

        class MockArgs:
            at = randint(0, 9)
            first = randint(0, 9)
            last = randint(0, 9)

        args = MockArgs()
        text = "one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten"
        lines.arg_lines(text, args)
        chop.assert_called_with(text, args.at, args.first, args.last)

    @patch("pysyte.types.lines.reformat_lines")
    def test_sed(self, reformat_lines):
        """sed() is a convenience method for reformat_lines()

        It just extracts expected args then calls reformat_lines()
        """

        class MockArgs:
            first = randint(0, 9)
            numbers = flip()
            width = 2 if flip() else 0

        args = MockArgs()
        text = "one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten"
        lines_ = text.splitlines()
        lines.sed(lines_, args)
        reformat_lines.assert_called_with(
            lines_, first=args.first, numbers=args.numbers, width=args.width
        )
