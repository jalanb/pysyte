"""Test paths module"""


import random
from unittest import TestCase


from pysyte import paths


class SourcePath(paths.FilePath):
    # pylint: disable=abstract-method
    pass


SourcePath.__file_class__ = SourcePath


class MockFilePathWithLines(paths.FilePath):
    # pylint: disable=abstract-method
    """Mock some known lines into a file"""
    def lines(self, encoding=None, errors='strict', retain=True):
        return [
            '\n',
            'line ends with spaces    ',
            '# comment\n',
            'Normal line\n'
        ]


class TestPaths(TestCase):

    def setUp(self):
        self.path = paths.path(__file__).extend_by('py')
        self.dir = self.path.parent
        self.source = paths.path(paths.__file__.rstrip('c')).extend_by('py')

    def test_path_error(self):
        self.assertRaises(
            paths.PathError,
            paths.path('/not/a/path').assert_exists)

    def test_not_path_error(self):
        p = paths.path('/')
        self.assertEqual(p, p.assert_exists())

    def test_assert_isfile(self):
        self.assertEqual(
            self.path,
            self.path.assert_isfile())

    def test_assert_not_isfile(self):
        self.assertRaises(
            paths.PathError,
            self.dir.assert_isfile)

    def test_assert_isdir(self):
        self.assertEqual(
            self.dir,
            self.dir.assert_isdir())

    def test_assert_not_isdir(self):
        self.assertRaises(
            paths.PathError,
            self.path.assert_isdir)

    def test_join_with_nothing(self):
        self.assertEqual(
            self.dir,
            self.dir / '')

    def test_file_class(self):
        path = SourcePath('').as_existing_file(str(self.source))
        self.assertTrue(path.isfile)
        self.assertIs(path.__file_class__, SourcePath)

    def test_dirnames(self):
        self.assertIn(self.dir.name, self.path.dirnames())

    def test_stripped_lines(self):
        path = MockFilePathWithLines('/not/a/real/file')
        line = random.choice(path.lines())
        self.assertTrue(line[-1].isspace())
        line = random.choice(path.stripped_lines())
        if line:
            self.assertFalse(line[-1].isspace())

    def test_stripped_whole_lines(self):
        path = MockFilePathWithLines('/not/a/real/file')
        self.assertTrue([l for l in path.stripped_lines() if not l])
        self.assertFalse([l for l in path.stripped_whole_lines() if not l])

    def test_non_comment_lines(self):
        path = MockFilePathWithLines('/not/a/real/file')
        self.assertTrue([l for l in path.stripped_whole_lines()
                         if l.startswith('#')])
        self.assertFalse([l for l in path.non_comment_lines()
                          if l.startswith('#')])

    def test_has_line(self):
        path = MockFilePathWithLines('/not/a/real/file')
        self.assertTrue(path.has_line('Normal line'))
        self.assertFalse(path.has_line('Normal'))
        self.assertFalse(path.has_line('Abnormal line'))

    def test_any_line_has(self):
        path = MockFilePathWithLines('/not/a/real/file')
        self.assertTrue(path.any_line_has('Normal line'))
        self.assertTrue(path.any_line_has('Normal'))
        self.assertFalse(path.any_line_has('Abnormal line'))

    def test_directory(self):
        self.assertEquals(self.path.directory(), self.path.parent)

    def test_no_div_for_file(self):
        path = paths.FilePath(__file__)
        with self.assertRaises(paths.PathError):
            path / 'fred'

    def test_directory_iteration(self):
        for item in self.path.directory():
            if item == self.path:
                break
        else:
            self.fail('Could not find %s' % self.path)
