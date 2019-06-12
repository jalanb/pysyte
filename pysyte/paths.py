"""A collection of extended path classes and methods

The classes all inherit from the original path.path
"""
import os
from fnmatch import fnmatch


class PathError(Exception):
    """Something went wrong with a path"""
    prefix = 'Path Error'

    def __init__(self, message):
        Exception.__init__(self, message)


class PathAssertions(object):
    """Assertions that can be made about paths"""
    # pylint: disable=no-member

    def assert_exists(self):
        """Raise a PathError if this path does not exist on disk"""
        if not self.exists():
            raise PathError(f'{self} does not exist')
        return self

    def assert_isdir(self):
        """Raise a PathError if this path is not a directory on disk"""
        if not self.isdir():
            raise PathError(f'{self} is not a directory')
        return self

    def assert_isfile(self):
        """Raise a PathError if this path is not a file on disk"""
        if not self.isfile():
            raise PathError(f'{self} is not a file')
        return self


from path import Path as PPath  # pylint: disable=wrong-import-position


class DotPath(PPath):
    """Some additions to the classic path class"""
    # pylint: disable=abstract-method

    def __repr__(self):
        string = repr(f'{self}')
        return f'<{self.__class__.__name__} {string}>'

    # The / operator joins paths.
    def __div__(self, child):
        """Join two path components, adding a separator character if needed.

        If the result is a file return self.__file_class__(result)

        >>> p = DotPath('/home/guido')
        >>> p.__div__('fred') == p / 'fred' == p.joinpath('fred')
        True
        """
        if child:
            result = os.path.join(self, child)
        else:
            result = str(self)  # pylint: disable=redefined-variable-type
        return self.as_existing_file(result)

    __truediv__ = __div__

    def __cmp__(self, other):
        return cmp(str(self), str(other))

    def _next_class(self, string):
        return self.as_existing_file(string)

    def as_existing_file(self, filepath):
        """Return the file class for existing files only"""
        if os.path.isfile(filepath) and hasattr(self, '__file_class__'):
            return self.__file_class__(filepath)  # pylint: disable=no-member
        return self.__class__(filepath)

    def parent_directory(self):
        if str(self) == '/':
            return None
        return self.parent

    def directory(self):
        """Return a path to the path's directory"""
        return self.parent

    def dirnames(self):
        """Split the dirname into individual directory names

        An absolute path starts with an empty string, a relative path does not

        >>> DotPath(u'/path/to/module.py').dirnames() == [u'', u'path', u'to']
        True
        >>> DotPath(u'path/to/module.py').dirnames() == [u'path', u'to']
        True
        """
        return self.dirname().split(os.path.sep)

    def dirpaths(self):
        """Split the dirname into individual directory names

        An absolute path starts with an empty string, a relative path does not

        >>> p = DotPath(u'/path/to/x.py')
        >>> p.paths == p.dirpaths()
        True
        """
        parts = self.parts()
        result = [DotPath(parts[0] or '/')]
        for name in parts[1:]:
            result.append(result[-1] / name)
        return result

    def parts(self):
        """Split the path into parts like Pathlib

        >>> expected = ['/', 'path', 'to', 'there']
        >>> assert DotPath('/path/to/there').parts() == expected
        """
        parts = self.split(os.path.sep)
        parts[0] = parts[0] and parts[0] or '/'
        return parts

    def directories(self):
        """Split the dirname into individual directory names

        No empty parts are included

        >>> DotPath(u'path/to/module.py').directories() == [u'path', u'to']
        True
        >>> DotPath(u'/path/to/module.py').directories() == [u'path', u'to']
        True
        """
        return [d for d in self.dirnames() if d]

    parents = property(
        dirnames, None, None,
        """ This path's parent directories, as a list of strings.

        >>> DotPath(u'/path/to/module.py').parents == [u'', u'path', u'to']
        True
        """)

    paths = property(
        dirpaths, None, None,
        """ This path's parent directories, as a sequence of paths.

        >>> paths = DotPath('/usr/bin/vim').paths
        >>> paths[-1].isfile()  # vim might be a link
        True
        >>> paths[-2] == paths[-1].parent
        True
        >>> paths[-3] == paths[-2].parent
        True
        >>> paths[-4] == paths[-3].parent
        True
        >>> paths[-4] == paths[0]
        True
        """)

    def short_relative_path_to(self, destination):
        """The shorter of either the absolute path of the destination,
            or the relative path to it

        >>> print(DotPath('/home/guido/bin').short_relative_path_to(
        ...     '/home/guido/build/python.tar'))
        ../build/python.tar
        >>> print(DotPath('/home/guido/bin').short_relative_path_to(
        ...     '/mnt/guido/build/python.tar'))
        /mnt/guido/build/python.tar
        """
        relative = self.relpathto(destination)
        absolute = self.__class__(destination).abspath()
        if len(relative) < len(absolute):
            return relative
        return absolute

    def short_relative_path_to_here(self):
        """A short path relative to current working directory"""
        return self.short_relative_path_to(os.getcwd())

    def short_relative_path_from_here(self):
        """A short path relative to self to the current working directory"""
        return self.__class__(os.getcwd()).short_relative_path_to(self)

    def walk_some_dirs(self, levels=-1, pattern=None):
        """ D.walkdirs() -> iterator over subdirs, recursively.

        With the optional 'pattern' argument, this yields only
        directories whose names match the given pattern.  For
        example, mydir.walkdirs('*test') yields only directories
        with names ending in 'test'.
        """
        if not levels:
            yield self
            raise StopIteration
        levels -= 1
        for child in self.dirs():
            if pattern is None or child.fnmatch(pattern):
                yield child
            if levels:
                for subsubdir in child.walk_some_dirs(levels, pattern):
                    yield subsubdir

    def fnmatch_basename(self, glob):
        if glob.startswith(os.path.sep):
            glob = glob.lstrip(os.path.sep)
        string = self.basename()
        if fnmatch(string, glob):
            return self
        return None

    def fnmatch_directory(self, glob):
        if glob.startswith(os.path.sep) or glob.endswith(os.path.sep):
            glob = glob.strip(os.path.sep)
        if self.isdir():
            string = self.basename()
        else:
            string = self.parent.basename()
        if fnmatch(string, glob):
            return self
        return None

    def fnmatch_directories(self, glob):
        if glob.startswith(os.path.sep) or glob.endswith(os.path.sep):
            glob = glob.strip(os.path.sep)
        strings = reversed(self.directory().splitall()[1:])
        for string in strings:
            if fnmatch(string, glob):
                return self
        return None

    def fnmatch_part(self, glob):
        if self.fnmatch(glob):
            return self
        if self.fnmatch_basename(glob):
            return self
        if self.fnmatch_directory(glob):
            return self
        if self.fnmatch_directories(glob):
            return self
        return None

    def __get_owner_not_implemented(self):
        pass

    def expandall(self):
        try:
            return self.expand().realpath().abspath()
        except AttributeError:
            return self.__class__(
                os.path.abspath(os.path.realpath(
                    os.path.expanduser(os.path.expandvars(str(self)))
                ))
            )

    def same_path(self, other):
        return self.expandall() == other.expandall()

    @property
    def hidden(self):
        """A 'hidden file' has a name starting with a '.'"""
        s = str(self.basename())
        return s and s[0] == '.'


def ext_language(ext, exts=None):
    """Language of the extension in those extensions

    If exts is supplied, then restrict recognition to those exts only
    If exts is not supplied, then use all known extensions

    >>> ext_language('.py') == 'python'
    True
    """
    languages = {
        '.py': 'python',
        '.py2': 'python2',
        '.py3': 'python3',
        '.sh': 'bash',
        '.bash': 'bash',
        '.pl': 'perl',
        '.js': 'javascript',
        '.txt': 'english',
    }
    ext_languages = {_: languages[_] for _ in exts} if exts else languages
    return ext_languages.get(ext)


def find_language(script, exts=None):
    """Determine the script's language  extension

    >>> this_script = __file__.rstrip('c')
    >>> find_language(makepath(this_script)) == 'python'
    True

    If exts are given they restrict which extensions are allowed
    >>> find_language(makepath(this_script), ('.sh', '.txt')) is None
    True

    If there is no extension, but shebang is present, then use that
    (Expecting to find "#!" in ~/.bashrc for this test,
        but ~/.bashrc might not exist - then there's no language)

    >>> bashrc = home() / '.bashrc'
    >>> find_language(bashrc) in ('bash', None)
    True
    """
    if not script.isfile():
        return None
    if script.ext:
        return ext_language(script.ext, exts)
    shebang = script.shebang()
    return shebang and str(shebang.name) or None


del PPath


class FilePath(DotPath, PathAssertions):
    """A path to a known file"""

    def __div__(self, child):
        raise PathError('%r has no children' % self)

    __truediv__ = __div__

    def __iter__(self):
        for line in self.stripped_lines():
            yield line

    def try_remove(self):
        """Try to remove the file"""
        self.remove()

    def stripped_lines(self):
        """A list of all lines without trailing whitespace

        If lines can not be read (e.g. no such file) then an empty list
        """
        try:
            return [l.rstrip() for l in self.lines(retain=False)]
        except (IOError, UnicodeDecodeError):
            return []

    def stripped_whole_lines(self):
        """A list of all lines without trailing whitespace or blank lines"""
        return [l for l in self.stripped_lines() if l]

    def non_comment_lines(self):
        """A list of all non-empty, non-comment lines"""
        return [l
                for l in self.stripped_whole_lines()
                if not l.startswith('#')]

    def has_line(self, string):
        for line in self:
            if string == line:
                return True
        return False

    def any_line_has(self, string):
        for line in self:
            if string in line:
                return True
        return False

    def split_all_ext(self):
        copy = self[:]
        filename, ext = os.path.splitext(copy)
        if ext == '.gz':
            filename, ext = os.path.splitext(filename)
            ext = f'{ext}.gz'
        return self.__class__(filename), ext

    def as_python(self):
        """The path to the file with a .py extension

        >>> FilePath('/path/to/fred.txt').as_python()
        <FilePath '/path/to/fred.py'>
        """
        return self.extend_by('.py')

    def extend_by(self, extension):
        """The path to the file changed to use the given extension

        >>> FilePath('/path/to/fred').extend_by('.txt')
        <FilePath '/path/to/fred.txt'>
        >>> FilePath('/path/to/fred.txt').extend_by('..tmp')
        <FilePath '/path/to/fred.tmp'>
        >>> FilePath('/path/to/fred.txt').extend_by('fred')
        <FilePath '/path/to/fred.fred'>
        """
        copy = self[:]
        filename, _ = os.path.splitext(copy)
        return self.__class__(f'{filename}.{extension.lstrip(".")}')

    def make_read_only(self):
        """chmod the file permissions to -r--r--r--"""
        self.chmod(ChmodValues.readonly_file)

    def cd(self):  # pylint: disable=invalid-name
        """Change program's current directory to self"""
        return cd(self.parent)

    def dirname(self):
        return DirectPath(os.path.dirname(self))
    parent = property(dirname)

    def shebang(self):
        """The  #! entry from the first line of the file

        If no shebang is present, return an empty string
        """
        try:
            try:
                first_line = self.lines(retain=False)[0]
            except (OSError, UnicodeDecodeError):
                return ''
            if first_line.startswith('#!'):
                rest_of_line = first_line[2:].strip()
                parts = rest_of_line.split(' ')
                interpreter = parts[0]
                return makepath(interpreter)
        except IndexError:
            pass
        return ''

    def mv(self, destination):  # pylint: disable=invalid-name
        return self.move(destination)

    def make_file_exist(self):
        """Make sure the parent directory exists, then touch the file"""
        self.parent.make_directory_exist()
        self.parent.touch_file(self.name)
        return self

    @property
    def language(self):
        """The language of this file"""
        try:
            return self._language
        except AttributeError:
            self._language = find_language(self, getattr(self, 'exts', None))
        return self._language

    @language.setter
    def language(self, value):
        self._langauge = value

    def choose_language(self, exts):
        self._exts = exts
        self._language = ext_language(self.ext, exts)


class DirectPath(DotPath, PathAssertions):
    """A path which knows it might be a directory

    And that files are in directories
    """

    __file_class__ = FilePath

    def __iter__(self):
        for a_path in DotPath.listdir(self):
            yield a_path

    def directory(self):
        """Return a path to a directory.

        Either the path itself (if it is a directory), or its parent)
        """
        if self.isdir():
            return self
        return self.parent

    def try_remove(self):
        """Try to remove the path

        If it is a directory, try recursive removal of contents too
        """
        if self.islink():
            self.unlink()
        elif self.isfile():
            self.remove()
        elif self.isdir():
            self.empty_directory()
            if self.isdir():
                self.rmdir()
        else:
            return False
        return True

    def empty_directory(self):
        """Remove all contents of a directory

        Including any sub-directories and their contents"""
        for child in self.walkfiles():
            child.remove()
        for child in reversed([d for d in self.walkdirs()]):
            if child == self or not child.isdir():
                continue
            child.rmdir()

    def cd(self):  # pylint: disable=invalid-name
        """Change program's current directory to self"""
        return cd(self)

    def listdir(self, pattern=None):
        return [self.as_existing_file(_)
                for _ in DotPath.listdir(self, pattern)]

    def list_dirs(self, pattern=None):
        return self.list_dirs_files(pattern)[0]

    def list_files(self, pattern=None):
        return self.list_dirs_files(pattern)[1]

    def list_dirsfiles(self, pattern=None):
        dirs, others = self.list_dirs_files(pattern)
        return dirs + others

    def list_dirs_files(self, pattern=None):
        items = self.listdir(pattern)
        dirs = [_ for _ in items if _.isdir()]
        others = [_ for _ in items if not _.isdir()]
        return dirs, others

    def make_directory_exist(self):
        if self.isdir():
            return False
        if os.path.exists(self):
            raise PathError(f'{self} exists but is not a directory')
        self.makedirs()

    def make_file_exist(self, filename=None):
        """Make the directory exist, then touch the file

        If the filename is None, then use self.name as filename
        """
        if filename is None:
            path_to_file = FilePath(self)
            path_to_file.make_file_exist()
            return path_to_file
        else:
            self.make_directory_exist()
            path_to_file = self.touch_file(filename)
            return FilePath(path_to_file)

    def make_read_only(self):
        """chmod the directory permissions to -r-xr-xr-x"""
        self.chmod(ChmodValues.readonly_directory)

    def touch_file(self, filename):
        """Touch a file in the directory"""
        path_to_file = self.__file_class__(os.path.join(self, filename))
        path_to_file.touch()
        return path_to_file

    def existing_sub_paths(self, sub_paths):
        """Those in the given list of sub_paths which do exist"""
        paths_to_subs = [self / _ for _ in sub_paths]
        return [_ for _ in paths_to_subs if _.exists()]

    def clear_directory(self):
        """Make sure the directory exists and is empty"""
        self.make_directory_exist()
        self.empty_directory()

    # pylint: disable=arguments-differ
    def walkdirs(self, pattern=None, errors='strict', ignores=None):
        ignored = ignore_globs(ignores)
        for path_to_dir in super(DirectPath, self).walkdirs(pattern, errors):
            if not ignored(path_to_dir.relpath(self)):
                yield path_to_dir

    # pylint: disable=arguments-differ
    def walkfiles(self, pattern=None, errors='strict', ignores=None):
        ignored = ignore_globs(ignores)
        for path_to_file in super(DirectPath, self).walkfiles(pattern, errors):
            if not ignored(path_to_file.relpath(self)):
                yield path_to_file

    def listfiles(self, pattern=None, ignores=None):
        ignored = ignore_globs(ignores)
        return [_ for _ in self.listdir(pattern) if _.isfile() and not ignored(_)]

    def has_vcs_dir(self):
        parts = self.splitall()
        for vcs_dir in ('.git', '.svn', '.hg'):
            if self.fnmatch_part(vcs_dir):
                return True
        return False



def ignore_globs(ignores):

    def ignored(a_path):
        if not ignores:
            return False
        for ignore in ignores:
            if a_path.fnmatch_part(ignore):
                return True
        return False

    return ignored


class ChmodValues(object):
    # pylint: disable=too-few-public-methods
    readonly_file = 0o444
    readonly_directory = 0o555


def makepath(s, as_file=False):
    """Make a path from a string

    Expand out any variables, home squiggles, and normalise it
    See also http://stackoverflow.com/questions/26403972
    """
    if s is None:
        return None
    result = FilePath(s) if (os.path.isfile(s) or as_file) else DirectPath(s)
    return result.expandall()

path = makepath  # pylint: disable=invalid-name


def cd(path_to):  # pylint: disable=invalid-name
    """cd to the given path

    If the path is a file, then cd to its parent directory

    Remember current directory before the cd
        so that we can cd back there with cd('-')
    """
    if path_to == '-':
        if not cd.previous:
            raise PathError('No previous directory to return to')
        return cd(cd.previous)
    if not hasattr(path_to, 'cd'):
        path_to = makepath(path_to)
    try:
        previous = os.getcwd()
    except OSError as e:
        if 'No such file or directory' in str(e):
            return False
        raise
    if path_to.isdir():
        os.chdir(path_to)
    elif path_to.isfile():
        os.chdir(path_to.parent)
    elif not os.path.exists(path_to):
        return False
    else:
        raise PathError(f'Cannot cd to {path_to}')
    cd.previous = previous
    return True


try:
    cd.previous = makepath(os.getcwd())
except (OSError, AttributeError):
    cd.previous = None


def as_path(string_or_path):
    """Return the argument as a DirectPath

    If it is already one, return it unchanged
    If not, return the makepath()
    """
    if isinstance(string_or_path, DirectPath):
        return string_or_path
    return makepath(string_or_path)


def string_to_paths(string):
    for c in ':, ;':
        if c in string:
            return strings_to_paths(string.split(c))
    return [makepath(string)]


def strings_to_paths(strings):
    return [makepath(s) for s in strings]


def paths(strings):
    return [p for p in strings_to_paths(strings) if p.exists()]


def split_directories(strings):
    paths = strings_to_paths(strings)
    return [_
            for _ in paths
            if _.isdir()], [_ for _ in paths if not _.isdir()]


def split_files(strings):
    paths = strings_to_paths(strings)
    return ([_ for _ in paths if _.isfile()],
            [_ for _ in paths if not _.isfile()])


def split_directories_files(strings):
    paths = strings_to_paths(strings)
    return ([_ for _ in paths if _.isdir()],
            [_ for _ in paths if _.isfile()],
            [_ for _ in paths if not (_.isfile() or _.isdir())])


def files(strings):
    return split_files(strings)[0]


def directories(strings):
    return split_directories(strings)[0]


def home(sub_path = None):
    return makepath('~') / sub_path


def pwd():
    return makepath(os.getcwd())

here = pwd  # pylint: disable=invalid-name


def first_dir(path_string):
    """Get the first directory in that path

    >>> first_dir('usr/local/bin') == 'usr'
    True
    """
    parts = path_string.split(os.path.sep)
    return parts[0]


def first_dirs(path_strings):
    """Get the roots of those paths

    >>> first_dirs(['usr/bin', 'bin']) == ['usr', 'bin']
    True
    """
    return [first_dir(_) for _ in path_strings]


def unique_first_dirs(path_strings):
    """Get the unique roots of those paths

    >>> unique_first_dirs(['usr/local/bin', 'bin']) == set(['usr', 'bin'])
    True
    """
    return set(first_dirs(path_strings))


def _names_in_directory(path_to_directory):
    """Get all items in the given directory

    Swallow errors to give an empty list
    """
    try:
        return os.listdir(path_to_directory)
    except OSError:
        return []


def make_needed(pattern, path_to_directory, wanted):
    """Make a method to check if an item matches the pattern, and is wanted

    If wanted is None just check the pattern
    """
    if wanted:
        def needed(name):
            return fnmatch(name, pattern) and wanted(
                os.path.join(path_to_directory, name))
        return needed
    else:
        return lambda name: fnmatch(name, pattern)


def list_items(path_to_directory, pattern, wanted):
    """All items in the given path which match the given glob and are wanted"""
    if not path_to_directory:
        return set()
    needed = make_needed(pattern, path_to_directory, wanted)
    return [os.path.join(path_to_directory, name)
            for name in _names_in_directory(path_to_directory)
            if needed(name)]


def list_sub_directories(path_to_directory, pattern):
    """All sub-directories of the given directory matching the given glob"""
    return list_items(path_to_directory, pattern, os.path.isdir)


def set_items(path_to_directory, pattern, wanted):
    return set(list_items(path_to_directory, pattern, wanted))


def set_files(path_to_directory, pattern):
    """A list of all files in the given directory matching the given glob"""
    return set_items(path_to_directory, pattern, os.path.isfile)


def contains_glob(path_to_directory, pattern, wanted=None):
    """Whether the given path contains an item matching the given glob"""
    if not path_to_directory:
        return False
    needed = make_needed(pattern, path_to_directory, wanted)
    for name in _names_in_directory(path_to_directory):
        if needed(name):
            return True
    return False


def contains_directory(path_to_directory, pattern):
    """Whether the given path contains a directory matching the given glob"""
    return contains_glob(path_to_directory, pattern, os.path.isdir)


def contains_file(path_to_directory, pattern):
    """Whether the given directory contains a file matching the given glob"""
    return contains_glob(path_to_directory, pattern, os.path.isfile)


def environ_paths(key):
    return [makepath(_) for _ in os.environ[key].split(':')]


def environ_path(key):
    return makepath(os.environ[key])


def default_environ_path(key, default):
    return makepath(os.environ.get(key, default))


def tab_complete(string):
    """Finish file names "left short" by tab-completion

    For example, if an argument is "fred."
        and no file called "fred." exists
        but "fred.py" does exist
        then return fred.py
    """
    if is_option(string):
        return string
    if not missing_extension(string):
        return string
    if os.path.isfile(string):
        return string
    extended_files = [f for f in extend(string) if os.path.isfile(f)]
    try:
        return extended_files[0]
    except IndexError:
        return string


def pyc_to_py(path_to_file):
    """Change some file extensions to those which are more likely to be text

    >>> pyc_to_py('vim.pyc') == 'vim.py'
    True
    """
    stem, ext = os.path.splitext(path_to_file)
    if ext == '.pyc':
        return f'{stem}.py'
    return path_to_file
