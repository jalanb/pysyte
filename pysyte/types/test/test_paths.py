"""Test paths module"""

import os
import random
from unittest import TestCase


from pysyte.types import paths


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
        path = SourcePath(str(self.source))
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
        self.assertEqual(self.path.directory(), self.path.parent)

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

    def test_vcs_dirs(self):
        self.assertTrue(paths.path('/usr/.git/fred').has_vcs_dir())
        self.assertTrue(paths.path('/usr/local/.svn').has_vcs_dir())
        self.assertTrue(paths.path('/.hg/etc').has_vcs_dir())
        self.assertFalse(paths.path('/usr/local/bin').has_vcs_dir())

    def test_cd_back(self):
        paths.cd.previous = None
        paths.cd('/usr')
        paths.cd('/usr/local')
        paths.cd('-')
        self.assertEqual(paths.pwd(), '/usr')

    def test_cd_back_without_previous(self):
        paths.cd.previous = None
        self.assertRaises(paths.PathError, paths.cd, '-')

    def test_cd_nowhere(self):
        self.assertFalse(paths.cd('/path/to/nowhere'))

    def test_as_path_with_path(self):
        path = paths.makepath('/usr/local')
        self.assertTrue(paths.as_path(path) is path)

    def test_as_path_with_string(self):
        string = '/usr/local'
        self.assertFalse(paths.as_path(string) is string)
        self.assertTrue(paths.as_path(string) == string)

    def test_string_to_paths(self):
        """String_to_paths should split a string with standard path separators

        For example - should work with the ':' used in $PATH
        """
        expected = [
            paths.makepath('/bin'),
            paths.makepath('/usr/bin'),
            paths.makepath('/usr/local/bin'),
        ]
        actual = paths.string_to_paths('/bin:/usr/bin:/usr/local/bin')
        self.assertEqual(actual, expected)

    def test_string_to_paths_without_separator(self):
        """string_to_paths() gives plain path if there are no separators

        It will always give a list
            but in this case, only one element in the list
        """
        expected = [paths.makepath('/usr/local/bin')]
        actual = paths.string_to_paths('/usr/local/bin')
        self.assertEqual(actual, expected)

    def test_paths(self):
        """paths() return all actual paths in a list of strings

        Then returns a list of existing paths
        """
        expected = [
            paths.makepath('/usr/bin'),
            paths.makepath('/usr/local/bin'),
        ]
        actual = paths.paths(['/not/a/path', '/usr/bin', '/usr/local/bin'])
        self.assertEqual(actual, expected)

    def test_split_files(self):
        """files() aplits a list of paths into 2 lists

        First is a list of existing files
        Second is the remainder
        """
        path_to_paths = paths.makepath(paths)
        tests = [path_to_paths, path_to_paths.parent]
        actual = paths.split_files(tests)
        expected = ([path_to_paths], [path_to_paths.parent])
        self.assertEqual(actual, expected)

    def test_files(self):
        """files() filters existing files from a list of paths"""
        path_to_paths = paths.makepath(paths)
        tests = [path_to_paths, path_to_paths.parent]
        expected = [path_to_paths]
        actual = paths.files(tests)
        self.assertEqual(actual, expected)

    def test_split_directories(self):
        """directories() aplits a list of paths into 2 lists

        First is a list of existing directories
        Second is the remainder
        """
        path_to_paths = paths.makepath(paths)
        tests = [path_to_paths, path_to_paths.parent]
        actual = paths.split_directories(tests)
        expected = ([path_to_paths.parent], [path_to_paths])
        self.assertEqual(actual, expected)

    def test_directories(self):
        """directories() filters existing directories from a list of paths"""
        path_to_paths = paths.makepath(paths)
        tests = [path_to_paths, path_to_paths.parent]
        expected = [path_to_paths.parent]
        actual = paths.directories(tests)
        self.assertEqual(actual, expected)

    def test_split_files_directories(self):
        """split_files_directories() aplits a list of paths into 3 lists

        First is a list of existing files
        Second is a list of existing directories
        Third is the remainder
        """
        path_to_paths = paths.makepath(paths)
        tests = ['/path/to/nowhere', path_to_paths, path_to_paths.parent]
        actual = paths.split_directories_files(tests)
        self.assertEqual(actual[0], [path_to_paths.parent])
        self.assertEqual(actual[1], [path_to_paths])
        self.assertEqual(actual[2], ['/path/to/nowhere'])

    def test_list_items_without_path(self):
        """Looking for a glob in non-existent path gives an empty set"""
        actual = paths.list_items('/path/to/nowhere', '*.*')
        expected = set()
        self.assertEqual(actual, expected)

    def test_environ_paths(self):
        """environ_paths() will split a ':' PATH from environ into paths"""
        shell_path = os.environ.get('PATH')
        shell_paths = shell_path.split(':')
        a_path = paths.makepath(random.choice(shell_paths))
        environ_paths = paths.environ_paths('PATH')
        self.assertTrue(a_path in environ_paths)
        self.assertTrue(random.choice(environ_paths).exists())

    def test_environ_path(self):
        """environ_path() gets a symbol from environ and converts it to path"""
        os.environ['TEST_PATH'] = '/usr/local'
        actual = paths.environ_path('TEST_PATH')
        expected = paths.makepath('/usr/local')
        self.assertEqual(actual, expected)

    def test_default_environ_path(self):
        """default_environ_path() gets a symbol from environ as a path"""
        os.environ['TEST_PATH'] = '/usr/local'
        actual = paths.default_environ_path('TEST_PATH', '/usr/local/bin')
        expected = paths.makepath('/usr/local')
        self.assertEqual(actual, expected)
        del os.environ['TEST_PATH']

    def test_default_environ_path_missing_key(self):
        """default_environ_path() gets a symbol from environ as a path

        And takes a default value, in case the key is missing
        """
        os.environ['FRED'] = '/usr/local'
        actual = paths.default_environ_path('TEST_PATH', '/usr/local/bin')
        expected = paths.makepath('/usr/local/bin')
        self.assertEqual(actual, expected)

    def test_pyc_to_py(self):
        """Convert a file like '...pyc' to '...py'"""
        expected = 'fred.py'
        actual = paths.pyc_to_py('fred.pyc')
        self.assertEqual(actual, expected)

    def test_py_to_py(self):
        """Convert a file like '...pyc' to '...py'"""
        expected = 'fred.py'
        actual = paths.pyc_to_py('fred.py')
        self.assertEqual(actual, expected)


class TestNonePath(TestCase):
    """A NonePath is made from an empty or non-existent path

    It should act like None (always false, contains nothing, ...)
    But still act like a Path (has 'isfile()', can be extended ...)
    """
    def test_none_to_none(self):
        for item in (None, '', 0):
            p = paths.makepath(item)
            self.assertTrue(isinstance(p, paths.NonePath))

    def test_repr(self):
        actual = repr(paths.makepath(None))
        expected = '<NonePath "">'
        self.assertEqual(actual, expected)

    def test_string_repr(self):
        actual = repr(paths.makepath('not/real/path'))
        expected = '<NonePath "not/real/path">'
        self.assertEqual(actual, expected)

    def test_has_parent(self):
        """A non-existent path can have a parent that does exist"""
        p = paths.path('/usr/fred')
        self.assertFalse(p.exists())
        self.assertTrue(p.parent.exists())

    def test_has_no_parent_without_slash(self):
        """A NonePath with no '/' has no parent

        This is unlike an existing path which always has a parent
            all the way up to root of the filesystem
        """
        self.assertIsNone(paths.path('fred_was_here').parent)

    def test_equality(self):
        """A NonePath is equal to anything else none-ish"""
        p = paths.makepath(None)
        self.assertTrue(p == '')
        self.assertTrue(p == 0)

    def test_equality_from_string(self):
        """A NonePath is equal to anything else none-ish

        Except: if made from a string, then do a string comparison
        """
        p = paths.makepath('/path/to/nowhere')
        self.assertTrue(p == '/path/to/nowhere')
        self.assertTrue(paths.makepath(None) == p)

    def test_less_than(self):
        """A NonePath is less than anything that's not false-y"""
        p = paths.makepath('/path/to/nowhere')
        self.assertTrue(p < '/path/to/nowhere/else')
        self.assertTrue(p < paths.makepath('/usr'))

    def test_not_less_than(self):
        """A NonePath is not less than anything that's false-y"""
        p = paths.makepath('/path/to/nowhere')
        self.assertFalse(p < False)
        self.assertFalse(p < paths.makepath(None))

    def test_total_ordering(self):
        """NonePath has __eq__, and __lt__, but can use other comparisons"""
        p = paths.makepath('/path/to/nowhere')
        self.assertTrue(p > '/path/to')
        self.assertTrue(p <= paths.makepath('/usr'))
        self.assertTrue(p <= paths.makepath('/path/to/nowhere'))

    def test_contains_nothing(self):
        """There's nothing in a NonePath

        Unlike an existing path
            where "in" means "in that directory"
        """
        self.assertTrue(paths.makepath('/usr/local') in paths.makepath('/usr'))
        self.assertFalse(paths.makepath('/a/path') in paths.makepath('/a'))

    def test_div(self):
        """Can still use the '/' operator with a NonePath"""
        parent = paths.makepath('/path/to')
        child = paths.makepath('/path/to/nowhere')
        self.assertTrue(parent / 'nowhere' == child)
