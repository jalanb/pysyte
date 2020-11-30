"""Test random choices"""

from unittest import TestCase

from pysyte import randoms


class TestRandoms(TestCase):
    def test_coin(self):
        self.assertIn(randoms.coin(), ("heads", "tails"))

    def test_flip(self):
        self.assertIn(randoms.flip(), (True, False))
