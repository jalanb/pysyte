"""Test the configs module"""


import unittest


from pysyte.cli import config


class TestConfigs(unittest.TestCase):
    def test_pysyte_config(self):
        """Check that we can read a config file for pysyte"""
        self.assertTrue(config.pysyte)
