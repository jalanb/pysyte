"""Test the term module"""


import unittest


from pysyte.bash import shell


class TestShell(unittest.TestCase):
    def test_double_cd(self):
        """This test is purely for sake of coverage

        The second cd (to same dir) should have no effect
        """
        shell.cd("/usr/local")
        expected = shell.run("basename $PWD")
        shell.cd("/usr/local")
        actual = shell.run("basename $PWD")
        self.assertEqual(actual, expected)
