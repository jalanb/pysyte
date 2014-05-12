"""Test paths module"""

from unittest import TestCase


from dotsite import paths


class SourcePath(paths.FilePath):
    pass


SourcePath.__file_class__ = SourcePath


class TestPaths(TestCase):

    def setUp(self):
        self.path = paths.makepath(__file__).extend_by('py')
        self.dir = self.path.parent
        self.source = paths.makepath(paths.__file__).extend_by('py')

    def test_path_error(self):
        self.assertRaises(
            paths.PathError,
            paths.makepath('/not/a/path').assert_exists)

    def test_not_path_error(self):
        p = paths.makepath('/')
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
        self.assertIn(self.dir.parent.dirnames(), self.dir.name)
