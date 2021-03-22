import unittest

from pysyte.colours import ansi_escapes


class TestEscapes(unittest.TestCase):
    def test_emphasis(self):
        """Assert values of emphasis functions"""
        self.assertEqual(ansi_escapes.bold(), "\x1b[1m")
        self.assertEqual(ansi_escapes.no_bold(), "\x1b[22m")
        self.assertEqual(ansi_escapes.no_colour(), "\x1b[2m\x1b[0m")
        self.assertEqual(ansi_escapes.no_prompt(), "\x01\x1b[2m\x1b[0m\x02")

    def test_foreground(self):
        """Adding a foreground colour"""
        prefix, suffix = ansi_escapes.foreground_string("X", 3).split("X")
        self.assertEqual(prefix.count("\x1b"), 1)
        self.assertEqual(suffix.count("\x1b"), 2)
        prefix, suffix = ansi_escapes.foreground_string("X", 300).split("X")
        self.assertEqual(prefix.count("\x1b"), 1)
        self.assertEqual(suffix.count("\x1b"), 2)

    def test_background(self):
        """Adding a background colour"""
        prefix, suffix = ansi_escapes.background_string("X", 3).split("X")
        self.assertEqual(prefix.count("\x1b"), 1)
        self.assertEqual(suffix.count("\x1b"), 2)
        prefix, suffix = ansi_escapes.background_string("X", 11).split("X")
        self.assertEqual(prefix.count("\x1b"), 2)
        self.assertEqual(suffix.count("\x1b"), 2)
        prefix, suffix = ansi_escapes.background_string("X", 300).split("X")
        self.assertEqual(prefix.count("\x1b"), 1)
        self.assertEqual(suffix.count("\x1b"), 2)

    def test_grounds(self):
        """Adding a foreground and background"""
        prefix, suffix = ansi_escapes.grounds_string("X", 3, 5).split("X")
        self.assertEqual(prefix.count("\x1b"), 2)
        self.assertEqual(suffix.count("\x1b"), 2)

    def test_prompt(self):
        """Adding a background colour"""
        prefix, suffix = ansi_escapes.prompt_string("X", 3).split("X")
        self.assertEqual(prefix.count("\x1b"), 1)
        self.assertEqual(suffix.count("\x1b"), 2)
        self.assertTrue(prefix.startswith("\x01"))
        self.assertTrue(suffix.startswith("\x01"))
        self.assertTrue(prefix.endswith("\x02"))
        self.assertTrue(suffix.endswith("\x02"))

    def test_no_background(self):
        "Nothing in, nothing out" ""
        self.assertFalse(ansi_escapes.background(0))
