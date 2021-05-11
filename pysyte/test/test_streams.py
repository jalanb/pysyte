"""Test stream handlers"""

import sys
from io import StringIO
from unittest import TestCase


from pysyte.streams import swallow_stdout, swallow_stderr


class TestStreams(TestCase):
    def test_swallow_stdout(self):
        stream = StringIO()
        with swallow_stdout(stream):
            print("hello", end="")
        self.assertEqual(stream.getvalue(), "hello")

    def test_swallow_stderr(self):
        stream = StringIO()
        with swallow_stderr(stream):
            print("hello", file=sys.stderr)
        self.assertEqual(stream.getvalue(), "hello\n")

    def test_discard_stdout(self):
        """This method is not programatically testable,

        But will produce no expected output
        If it fails it becomes noticable at command line
        """
        with swallow_stdout():
            print("hello")

    def test_discard_stderr(self):
        """This method is not programatically testable,

        But will produce no expected output
        If it fails it becomes noticable at command line
        """
        with swallow_stderr():
            print("hello", file=sys.stderr)
