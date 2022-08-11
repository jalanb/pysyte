"""Test paths module"""

import os
import random
import builtins
from unittest import TestCase


from pysyte.types import paths


class SourcePath(paths.FilePath):
    pass


SourcePath.__file_class__ = SourcePath


class MockFilePathWithLines(paths.FilePath):
    """Mock some known lines into a file"""

    def lines(self, encoding=None, errors="strict", retain=True):
        return [
            "\n",
            "line ends with spaces    ",
            "# comment\n",
            "Normal line\n",
        ]


class MockPythonShebang(MockFilePathWithLines):
    """Mock some lines into a file, with first having '#!'"""

    def lines(self, encoding=None, errors="strict", retain=True):
        return ["#! /usr/bin/env python3\n", "i = 5\n", "pass"]


class MockPythonShebangError(MockFilePathWithLines):
    """Mock some lines into a file, but raise an error"""

    def lines(self, encoding=None, errors="strict", retain=True):
        raise IOError("something went wrong")


class TestDotPath(TestCase):
    """Test DotPath: base class to other path classes"""

    def test_root(self):
        self.assertRaises(NotImplementedError, paths.DotPath("").isroot)

    def test_executability(self):
        """A DotPath should not be executable"""
        self.assertFalse(paths.DotPath("nowhere").has_executable())


class TestPaths(TestCase):
    def setUp(self):
        self.setup_dir = paths.pwd()
        self.path_to_test = paths.path(__file__).extend_by("py")
        self.dir = self.path_to_test.parent
        self.path_to_paths = paths.path(paths).extend_by("py")
        self.path_to_package = self.path_to_paths.parent
        # For testing here "path to project" means top-level python package
        #     i.e. not very top-level with ".git", etc
        self.path_to_project = self.path_to_package.parent

    def tearDown(self):
        self.setup_dir.cd()

    def test_path_error(self):
        self.assertRaises(paths.PathError, paths.path("/not/a/path").assertExists)

    def test_not_path_error(self):
        path = paths.path("/")
        self.assertEqual(path, path.assertExists())

    def test_assert_isfile(self):
        self.assertEqual(self.path_to_test, self.path_to_test.assert_isfile())

    def test_assert_not_isfile(self):
        self.assertRaises(paths.PathError, self.dir.assert_isfile)

    def test_assert_isdir(self):
        self.assertEqual(self.dir, self.dir.assert_isdir())

    def test_assert_not_isdir(self):
        self.assertRaises(paths.PathError, self.path_to_test.assert_isdir)

    def test_join_with_nothing(self):
        self.assertEqual(self.dir, self.dir / "")

    def test_file_class(self):
        path = SourcePath(str(self.path_to_paths))
        self.assertTrue(path.isfile)
        self.assertIs(path.__file_class__, SourcePath)

    def test_dirnames(self):
        self.assertIn(self.dir.name, self.path_to_test.dirnames())

    def test_stripped_lines(self):
        path = MockFilePathWithLines("/not/a/real/file")
        line = random.choice(path.lines())
        self.assertTrue(line[-1].isspace())
        line = random.choice(path.stripped_lines())
        if line:
            self.assertFalse(line[-1].isspace())

    def test_stripped_whole_lines(self):
        path = MockFilePathWithLines("/not/a/real/file")
        self.assertTrue([_ for _ in path.stripped_lines() if not _])
        self.assertFalse([_ for _ in path.stripped_whole_lines() if not _])

    def test_non_comment_lines(self):
        path = MockFilePathWithLines("/not/a/real/file")
        self.assertTrue([_ for _ in path.stripped_whole_lines() if _.startswith("#")])
        self.assertFalse([_ for _ in path.non_comment_lines() if _.startswith("#")])

    def test_has_line(self):
        path = MockFilePathWithLines("/not/a/real/file")
        self.assertTrue(path.has_line("Normal line"))
        self.assertFalse(path.has_line("Normal"))
        self.assertFalse(path.has_line("Abnormal line"))

    def test_any_line_has(self):
        path = MockFilePathWithLines("/not/a/real/file")
        self.assertTrue(path.any_line_has("Normal line"))
        self.assertTrue(path.any_line_has("Normal"))
        self.assertFalse(path.any_line_has("Abnormal line"))

    def test_directory(self):
        self.assertEqual(self.path_to_test.directory(), self.path_to_test.parent)

    def test_no_div_for_file(self):
        path = paths.FilePath(__file__)
        with self.assertRaises(paths.PathError):
            path / "fred"

    def test_directory_iteration(self):
        for item in self.path_to_test.directory():
            if item == self.path_to_test:
                break
        else:
            self.fail("Could not find %s" % self.path_to_test)

    def test_vcs_dirs(self):
        self.assertTrue(paths.path("/usr/.git/fred").has_vcs_dir())
        self.assertTrue(paths.path("/usr/local/.svn/fred").has_vcs_dir())
        self.assertTrue(paths.path("/.hg/etc").has_vcs_dir())
        self.assertFalse(paths.path("/usr/local/bin").has_vcs_dir())

    def test_cd_back(self):
        paths.cd.previous = None
        paths.cd("/usr")
        paths.cd("/usr/local")
        paths.cd("-")
        self.assertEqual(paths.pwd(), "/usr")

    def test_cd_back_without_previous(self):
        paths.cd.previous = None
        self.assertRaises(paths.PathError, paths.cd, "-")

    def test_cd_nowhere(self):
        self.assertFalse(paths.cd("/path/to/nowhere"))

    def test_as_path_with_path(self):
        path = paths.makepath("/usr/local")
        self.assertIs(paths.as_path(path), path)

    def test_as_path_with_string(self):
        string = "/usr/local"
        self.assertIsNot(paths.as_path(string), string)
        self.assertEqual(paths.as_path(string), string)

    def test_string_to_paths(self):
        """String_to_paths should split a string with standard path separators

        For example - should work with the ':' used in $PATH
        """
        expected = [
            paths.makepath("/bin"),
            paths.makepath("/usr/bin"),
            paths.makepath("/usr/local/bin"),
        ]
        actual = paths.string_to_paths("/bin:/usr/bin:/usr/local/bin")
        self.assertEqual(actual, expected)

    def test_string_to_paths_without_separator(self):
        """string_to_paths() gives plain path if there are no separators

        It will always give a list
            but in this case, only one element in the list
        """
        expected = [paths.makepath("/usr/local/bin")]
        actual = paths.string_to_paths("/usr/local/bin")
        self.assertEqual(actual, expected)

    def test_paths(self):
        """paths() return all actual paths in a list of strings"""
        expected = [
            paths.makepath("/usr/bin"),
            paths.makepath("/usr/local/bin"),
        ]
        actual = paths.paths(*["/not/a/path", "/usr/bin", "/usr/local/bin"])
        self.assertEqual(actual, expected)

    def test_path_argss(self):
        """paths() return all actual paths in its args"""
        expected = [
            paths.makepath("/usr/bin"),
            paths.makepath("/usr/local/bin"),
        ]
        actual = paths.paths("/not/a/path", "/usr/bin", "/usr/local/bin")
        self.assertEqual(actual, expected)

    def test_directories(self):
        """directories() should return actual directories in strings"""
        expected = [
            paths.makepath("/usr/bin"),
            paths.makepath("/usr/local/bin"),
        ]
        actual = paths.directories(*["/not/a/path", "/usr/bin", "/usr/local/bin"])
        self.assertEqual(actual, expected)

    def test_directories_args(self):
        """directories() should return actual directories in its args"""
        expected = [
            paths.makepath("/usr/bin"),
            paths.makepath("/usr/local/bin"),
        ]
        actual = paths.directories("/not/a/path", "/usr/bin", "/usr/local/bin")
        self.assertEqual(actual, expected)

    def test_files(self):
        """files() should return actual files in a list of strings"""
        expected = [paths.makepath(__file__)]
        actual = paths.files(*["/not/a/path", __file__, "/usr/local/bin"])
        self.assertEqual(actual, expected)

    def test_files_args(self):
        """files() should return actual files in its args"""
        expected = [paths.makepath(__file__)]
        actual = paths.files("/not/a/path", __file__, "/usr/local/bin")
        self.assertEqual(actual, expected)

    def test_list_items_without_path(self):
        """Looking for a glob in non-existent path gives an empty set"""
        actual = paths.list_items("/path/to/nowhere", "*.*")
        expected = list()
        self.assertEqual(actual, expected)

    def test_environ_paths(self):
        """environ_paths() will split a ':' PATH from environ into paths"""
        shell_path = os.environ.get("PATH")
        shell_paths = shell_path.split(":")
        a_path = paths.makepath(random.choice(shell_paths))
        environ_paths = paths.environ_paths("PATH")
        self.assertIn(a_path, environ_paths)

    def test_environ_path(self):
        """environ_path() gets a symbol from environ and converts it to path"""
        os.environ["TEST_PATH"] = "/usr/local"
        actual = paths.environ_path("TEST_PATH")
        expected = paths.makepath("/usr/local")
        self.assertEqual(actual, expected)

    def test_default_environ_path(self):
        """default_environ_path() gets a symbol from environ as a path"""
        os.environ["TEST_PATH"] = "/usr/local"
        actual = paths.default_environ_path("TEST_PATH", "/usr/local/bin")
        expected = paths.makepath("/usr/local")
        self.assertEqual(actual, expected)
        del os.environ["TEST_PATH"]

    def test_default_environ_path_missing_key(self):
        """default_environ_path() gets a symbol from environ as a path

        And takes a default value, in case the key is missing
        """
        os.environ["FRED"] = "/usr/local"
        actual = paths.default_environ_path("TEST_PATH", "/usr/local/bin")
        expected = paths.makepath("/usr/local/bin")
        self.assertEqual(actual, expected)

    def test_pyc_to_py(self):
        """Convert a file like '...pyc' to '...py'"""
        expected = "fred.py"
        actual = paths.pyc_to_py("fred.pyc")
        self.assertEqual(actual, expected)

    def test_py_to_py(self):
        """Don't convert a file like '...py', leave it as '...py'"""
        expected = "fred.py"
        actual = paths.pyc_to_py("fred.py")
        self.assertEqual(actual, expected)

    def test_equality(self):
        """Two paths are same as strings to be == as paths

        But, any trailing '/' on a directory does not matter
        """
        self.assertEqual(paths.path("/usr/local"), paths.path("/usr/local/"))

    def test_less_than(self):
        """Paths use strings for testing less than"""
        self.assertLess(paths.path("/usr/local"), paths.path("/usr/local/bin"))

    def test_total_ordering(self):
        """Greater than is based on less than"""
        self.assertGreater(paths.path("/usr/local/bin"), paths.path("/usr/local"))

    def test_relative_paths(self):
        expected = self.path_to_package.basename()
        actual = self.path_to_project.short_relative_path_to(self.path_to_package)
        self.assertEqual(actual, expected)
        expected = ".."
        actual = self.path_to_package.short_relative_path_to(self.path_to_project)
        self.assertEqual(actual, expected)

    def test_relative_path_hither(self):
        self.path_to_package.cd()
        expected = self.path_to_package.basename()
        actual = self.path_to_project.short_relative_path_to_here()
        self.assertEqual(actual, expected)

    def test_relative_path_hence(self):
        self.path_to_package.cd()
        expected = ".."
        actual = self.path_to_project.short_relative_path_from_here()
        self.assertEqual(actual, expected)

    def test_fnmatch_basename(self):
        """The name of this file should start with 'test_'"""
        self.assertTrue(self.path_to_test.fnmatch_basename("test_*"))
        self.assertTrue(self.path_to_test.fnmatch_basename("/test_*"))

    def test_fnmatch_directory(self):
        """The name of this file's dir should start with 'test'

        Check against "te*" as well, as the name may be 'test'
        """
        self.assertTrue(self.path_to_test.fnmatch_directory("test*"))
        self.assertTrue(self.path_to_test.fnmatch_directory("/test*"))
        self.assertTrue(self.path_to_test.fnmatch_directory("/test*/"))
        self.assertTrue(self.path_to_test.fnmatch_directory("te*"))

    def test_fnmatch_directories(self):
        """One pf the parent dires from this file should be 'pysyte'

        But this (test) file is not in that directory
        """
        self.assertTrue(self.path_to_test.fnmatch_directories("py*te"))
        self.assertTrue(self.path_to_test.fnmatch_directories("/py*te"))
        self.assertTrue(self.path_to_test.fnmatch_directories("py*te/"))
        self.assertTrue(self.path_to_test.fnmatch_directories("/py*te/"))
        self.assertFalse(self.path_to_test.fnmatch_directory("py*te"))

    def test_fnmatch_part(self):
        """The fnmatch_part() method tries globs against all parts

        So - all of the above test globs should match
        """
        self.assertTrue(self.path_to_test.fnmatch_part("test*"))
        self.assertTrue(self.path_to_test.fnmatch_part("/test_*"))
        self.assertTrue(self.path_to_test.fnmatch_part("te*"))
        self.assertTrue(self.path_to_test.fnmatch_part("py*te"))

    def test_no_shebang(self):
        """This file should not have a shebang line"""
        expected = ""
        actual = self.path_to_test.shebang()
        self.assertEqual(actual, expected)

    def test_python_shebang(self):
        """Read the shebang line from a file"""
        path = MockPythonShebang("/not/a/real/file")
        expected = "/usr/bin/env python3"
        actual = path.shebang()
        self.assertEqual(actual, expected)

    def test_python_shebang_unicode(self):
        """Read the shebang line from an erroring file gives nothing

        It should not propogate the error
            just give an empty result
        """
        path = MockPythonShebangError("/not/a/real/file")
        expected = ""
        actual = path.shebang()
        self.assertEqual(actual, expected)

    def test_language(self):
        expected = "python"
        actual = self.path_to_test.language
        self.assertEqual(actual, expected)

    def test_set_language(self):
        self.assertEqual(self.path_to_test.language, "python")
        self.path_to_test.language = "python3"
        self.assertEqual(self.path_to_test.language, "python3")

    def test_builtin_module(self):
        """makepath() works for modules, except builtins which has no file"""
        self.assertTrue(paths.makepath(os).isfile())
        self.assertFalse(paths.makepath(builtins).isfile())


class TestNonePath(TestCase):
    """A NonePath is made from an empty or non-existent path

    It should act like None (always false, contains nothing, ...)
    But still act like a Path (has 'isfile()', can be extended ...)
    """

    def test_none_to_none(self):
        for item in (None, "", 0):
            path = paths.path(item)
            self.assertTrue(isinstance(path, paths.NonePath))

    def test_repr(self):
        actual = repr(paths.path(None))
        expected = '<NonePath "">'
        self.assertEqual(actual, expected)

    def test_string_repr(self):
        actual = repr(paths.path("not/real/path"))
        expected = '<NonePath "not/real/path">'
        self.assertEqual(actual, expected)

    def test_has_parent(self):
        """A non-existent path can have a parent that does exist"""
        path = paths.path("/usr/fred")
        self.assertFalse(path.exists())
        self.assertTrue(path.parent.exists())

    def test_has_no_parent_without_slash(self):
        """A NonePath with no '/' has no parent

        This is unlike an existing path which always has a parent
            all the way up to root of the filesystem
        """
        self.assertIsNone(paths.path("fred_was_here").parent)

    def test_equality(self):
        """A NonePath is equal to anything else none-ish"""
        path = paths.path(None)
        self.assertEqual(path, "")
        self.assertEqual(path, 0)

    def test_equality_from_string(self):
        """A NonePath is equal to anything else none-ish

        Except: if made from a string, then do a string comparison
        """
        path = paths.path("/path/to/nowhere")
        self.assertEqual(path, "/path/to/nowhere")
        self.assertEqual(paths.path(None), path)

    def test_less_than(self):
        """A NonePath is less than anything that's not false-y"""
        path = paths.path("/path/to/nowhere")
        self.assertLess(path, "/path/to/nowhere/else")
        self.assertLess(path, paths.path("/usr"))

    def test_not_less_than(self):
        """A NonePath is not less than anything that's false-y"""
        path = paths.path("/path/to/nowhere")
        self.assertGreaterEqual(path, False)
        self.assertGreaterEqual(path, paths.path(None))

    def test_total_ordering(self):
        """NonePath has __eq__, and __lt__, but can use other comparisons"""
        path = paths.path("/path/to/nowhere")
        self.assertGreater(path, "/path/to")
        self.assertLessEqual(path, paths.path("/usr"))
        self.assertLessEqual(path, paths.path("/path/to/nowhere"))

    def test_contains_nothing(self):
        """There's nothing in a NonePath

        Unlike an existing path
            where "in" means "in that directory"
        """
        self.assertIn(paths.path("/usr/local"), paths.path("/usr"))
        self.assertNotIn(paths.path("/a/path"), paths.path("/a"))

    def test_div(self):
        """Can still use the '/' operator with a NonePath"""
        parent = paths.path("/path/to")
        child = paths.path("/path/to/nowhere")
        self.assertEqual(parent / "nowhere", child)

    def test_executable(self):
        """A NonePath should not be executable"""
        self.assertFalse(paths.path(None).has_executable())
