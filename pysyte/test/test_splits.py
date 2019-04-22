"""Test the splits module"""


import unittest


import pysyte as site


class TestSplits(unittest.TestCase):

    def test_docstring(self):
        self.assertTrue(site.splits.__doc__)

    def test_split(self):
        """Basic split method is similar to that of string

        Except that it splits on commas, not spaces
        """
        expected = ['fred', ' was here']
        actual = site.splits.split('fred, was here')
        self.assertEqual(expected, actual)

    def test_on_space(self):
        """But spaces can be specified (or any other regexp)"""
        expected = ['fred,', 'was', 'here']
        actual = site.splits.split('fred, was here', ' ')
        self.assertEqual(expected, actual)

    def test_separator_regexp(self):
        """Can split on a regular expression"""
        data = [
            ('one,two;three', '[,;]', ['one', 'two', 'three']),
            ('one,,,two', ',+', ['one', 'two']),
            ('*blackduck*', '[*?[]', ['', 'blackduck', '']),
        ]
        for string, separator, expected in data:
            actual = site.splits.split(string, separator)
            self.assertEqual(expected, actual)

    def test_split_and_strip(self):
        """Split a string on commas, and trim any spaces from the results"""
        expected = ['fred', 'was', 'here', 'today']
        actual = site.splits.split_and_strip('fred,was   , here ,today')
        self.assertEqual(expected, actual)

    def test_regexp(self):
        """Can supply a more complicated separator, which is a regexp

        Let's separate on commas or spaces
        """
        expected = ['fred', 'was', '', '', '', '', 'here', '', 'today']
        actual = site.splits.split_and_strip(
            'fred,was   , here ,today',
            separator_regexp='[, ]')
        self.assertEqual(expected, actual)

    def test_maxsplit(self):
        """Can supply a max number of parts"""
        expected = ['fred', 'was   , here ,today']
        actual = site.splits.split_and_strip(
            'fred,was   , here ,today', maxsplit=1)
        self.assertEqual(expected, actual)

    def test_separator_and_maxsplit(self):
        expected = ['fred', 'was', '', ', here ,today']
        actual = site.splits.split_and_strip(
            'fred,was   , here ,today',
            separator_regexp='[, ]',
            maxsplit=3)
        self.assertEqual(expected, actual)

    def test_without(self):
        """We can say that we do not want some values in the result"""
        expected = ['fred', 'was', 'today']
        actual = site.splits.split_and_strip_without(
            'fred,was   , here ,today',
            ['', 'here'])
        self.assertEqual(expected, actual)

    def test_join(self):
        """Simple joins can handle non-strings"""
        expected = '1,2,3'
        actual = site.splits.join([1, 2, 3])
        self.assertEqual(expected, actual)

    def test_joiner(self):
        """Any character can act as a joiner"""
        expected = '1--2--3'
        actual = site.splits.join([1, 2, 3], '--')
        self.assertEqual(expected, actual)

    def test_rejoin(self):
        """Splitting and rejoining allows better control of spaces between

        (not just "remove all spaces")
        """
        expected = 'fred,was,here with some nice people,today'
        actual = site.splits.rejoin(
            'fred,was   , here with some nice people,today')
        self.assertEqual(expected, actual)

    def test_rejoin_spaced(self):
        """The rejoin can add back minimal separator spaces"""
        expected = 'fred, was, here, today'
        actual = site.splits.rejoin('fred,was   , here ,today', spaced=True)
        self.assertEqual(expected, actual)

    def test_despaced(self):
        """Split a string into spaceless items"""
        expected = ['fred,', ',', 'was,here', 'today']
        actual = site.splits.despaced('fred, , was,here today')
        self.assertEqual(expected, actual)

    def test_despaced_edge_cases(self):
        self.assertEqual(site.splits.despaced('despaced'), ['despaced'])
        self.assertEqual(site.splits.despaced(''), [])
        self.assertEqual(site.splits.despaced(None), [])

    def test_split_mirrors_join(self):
        tests = ['', ',', 'a,', ',b', 'a,b']
        actual = all(
            [site.splits.join(site.splits.split(t)) == t for t in tests])
        self.assertTrue(actual)
        tests = [[], ['one'], ['one', 'two']]
        actual = all(
            [site.splits.split(site.splits.join(t)) == t for t in tests])
        self.assertTrue(actual)

    def test_empty_separator(self):
        self.assertEqual(
            site.splits.split('i was here', ''),
            'i was here'.split())

    def test_empties_separator(self):
        self.assertEqual(
            site.splits.split_and_strip('i  was here', ''),
            'i was here'.split())

    def test_no_exclusions(self):
        self.assertEqual(
            site.splits.split_and_strip_without('i was here', ''),
            site.splits.split_and_strip('i was here'))

    def test_split_by_count(self):
        items = [1, 2, 3]
        actual = site.splits.split_by_count(items, 2, 4)
        expected = [(1, 2), (3, 4)]
        self.assertEqual(actual, expected)
        self.assertEqual(items, [1, 2, 3])
