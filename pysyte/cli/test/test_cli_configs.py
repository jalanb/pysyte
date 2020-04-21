"""Test the configs module"""


import unittest


from pysyte.cli import config
from pysyte.types import paths


class TestConfigs(unittest.TestCase):
    """For each of these tests the config file may not exist

    The config methods will always give a dictionary
        So our "actual" data below should always have ".keys()"

    If the file is missing, the dictionary keys will be empty
    """
    def test_user_config(self):
        """Check that we can read a config file in $XDG_HOME"""
        path_to_config = paths.path('~/.config/pysyte.yml')
        actual = config.user('pysyte').keys()
        if path_to_config.isfile():
            self.assertTrue(actual)
        else:
            self.assertFalse(actual)

    def test_machine_config(self):
        """Check that we can read a config file in /etc"""
        path_to_config = paths.path('/etc/pysyte.yml')
        actual = config.machine('pysyte').keys()
        if path_to_config.isfile():
            self.assertTrue(actual)
        else:
            self.assertFalse(actual)

    def test_all_configs(self):
        user = list(config.user('pysyte').keys())
        machine = list(config.machine('pysyte').keys())
        actual = list(config.all('pysyte').keys())
        for key in user + machine:
            self.assertIn(key, actual)
