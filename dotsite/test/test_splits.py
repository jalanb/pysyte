"""Test the splits module"""


import unittest


from dotsite import splits


class TestSplits(unittest.TestCase):

    def test_docstring(self):
        self.assertTrue(splits.__doc__)

    def test_split(self):
        """Basic split method is similar to that of string

        Except that it splits on commas, not spaces
        """
        expected = ['fred', ' was here']
        actual = splits.split('fred, was here')
        self.assertEqual(expected, actual)

    def test_on_space(self):
        """But spaces can be specified (or any other regexp)"""
        expected = ['fred,', 'was', 'here']
        actual = splits.split('fred, was here', ' ')
        self.assertEqual(expected, actual)

    def test_separator_regexp(self):
        """Can split on a regular expression"""
        data = [
            ('one,two;three', '[,;]', ['one', 'two', 'three']),
            ('one,,,two', ',*', ['one', 'two']),
            ('*blackduck*', '[*?[]', ['', 'blackduck', '']),
        ]
        for string, separator, expected in data:
            actual = splits.split(string, separator)
            self.assertEqual(expected, actual)

    def test_split_and_strip(self):
        """Split a string on commas, and trim any spaces from the results"""
        expected = ['fred', 'was', 'here', 'today']
        actual = splits.split_and_strip('fred,was   , here ,today')
        self.assertEqual(expected, actual)

    def test_regexp(self):
        """Can supply a more complicated separator, which is a regexp

        Let's separate on commas or spaces
        """
        expected = ['fred', 'was', '', '', '', '', 'here', '', 'today']
        actual = splits.split_and_strip(
            'fred,was   , here ,today',
            separator_regexp='[, ]')
        self.assertEqual(expected, actual)

    def test_maxsplit(self):
        """Can supply a max number of parts"""
        expected = ['fred', 'was   , here ,today']
        actual = splits.split_and_strip('fred,was   , here ,today', maxsplit=1)
        self.assertEqual(expected, actual)

    def test_separator_and_maxsplit(self):
        expected = ['fred', 'was', '', ', here ,today']
        actual = splits.split_and_strip(
            'fred,was   , here ,today',
            separator_regexp='[, ]',
            maxsplit=3)
        self.assertEqual(expected, actual)

    def test_without(self):
        """We can say that we do not want some values in the result"""
        expected = ['fred', 'was', 'today']
        actual = splits.split_and_strip_without(
            'fred,was   , here ,today',
            ['', 'here'])
        self.assertEqual(expected, actual)

    def test_join(self):
        """Simple joins can handle non-strings"""
        expected = '1,2,3'
        actual = splits.join([1, 2, 3])
        self.assertEqual(expected, actual)

    def test_joiner(self):
        """Any character can act as a joiner"""
        expected = '1--2--3'
        actual = splits.join([1, 2, 3], '--')
        self.assertEqual(expected, actual)

    def test_rejoin(self):
        """Splitting and rejoining allows better control of spaces between

        (not just "remove all spaces")
        """
        expected = 'fred,was,here with some nice people,today'
        actual = splits.rejoin('fred,was   , here with some nice people,today')
        self.assertEqual(expected, actual)

    def test_rejoin_spaced(self):
        """The rejoin can add back minimal separator spaces"""
        expected = 'fred, was, here, today'
        actual = splits.rejoin('fred,was   , here ,today', spaced=True)
        self.assertEqual(expected, actual)

    def test_despaced(self):
        """Split a string into spaceless items"""
        expected = ['fred,', ',', 'was,here', 'today']
        actual = splits.despaced('fred, , was,here today')
        self.assertEqual(expected, actual)

    def test_despaced_edge_cases(self):
        self.assertEquals(splits.despaced('despaced'), ['despaced'])
        self.assertEquals(splits.despaced(''), [])
        self.assertEquals(splits.despaced(None), [])

    def test_split_mirrors_join(self):
        tests = ['', ',', 'a,', ',b', 'a,b']
        actual = all([splits.join(splits.split(t)) == t for t in tests])
        self.assertTrue(actual)
        tests = [[], ['one'], ['one', 'two']]
        actual = all([splits.split(splits.join(t)) == t for t in tests])
        self.assertTrue(actual)
