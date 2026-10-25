"""Test stream handlers"""

from io import StringIO
import sys
from unittest import TestCase

from pysyte.streams import swallow_stderr, swallow_stdout


class TestStreams(TestCase):
    def test_swallow_stdout(self) -> None:
        stream = StringIO()
        with swallow_stdout(stream):
            print("hello", end="")
        self.assertEqual(stream.getvalue(), "hello")

    def test_swallow_stderr(self) -> None:
        stream = StringIO()
        with swallow_stderr(stream):
            print("hello", file=sys.stderr)
        self.assertEqual(stream.getvalue(), "hello\n")

    def test_discard_stdout(self) -> None:
        """This method is not programatically testable,

        But will produce no expected output
        If it fails it becomes noticable at command line
        """
        with swallow_stdout():
            print("hello")

    def test_discard_stderr(self) -> None:
        """This method is not programatically testable,

        But will produce no expected output
        If it fails it becomes noticable at command line
        """
        with swallow_stderr():
            print("hello", file=sys.stderr)
