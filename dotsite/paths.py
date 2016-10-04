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
            raise PathError('%s does not exist' % self)
        return self

    def assert_isdir(self):
        """Raise a PathError if this path is not a directory on disk"""
        if not self.isdir():
            raise PathError('%s is not a directory' % self)
        return self

    def assert_isfile(self):
        """Raise a PathError if this path is not a file on disk"""
        if not self.isfile():
            raise PathError('%s is not a file' % self)
        return self


from path import Path as path_path # pylint: disable=wrong-import-position


class Path(path_path):
    """Some additions to the classic path class"""
    # pylint: disable=abstract-method

    def __repr__(self):
        return '<%s %s>' % (
            self.__class__.__name__,
            repr(str(self)))

    # The / operator joins paths.
    def __div__(self, child):
        """Join two path components, adding a separator character if needed.

        If the result is a file return self.__file_class__(result)

        >>> p = Path('/home/guido')
        >>> p.__div__('fred') == p / 'fred' == p.joinpath('fred')
        True
        """
        if child:
            result = os.path.join(self, child)
        else:
            result = str(self) # pylint: disable=redefined-variable-type
        return self.as_existing_file(result)

    def as_existing_file(self, filepath):
        """Return the file class for existing files only"""
        if os.path.isfile(filepath) and hasattr(self, '__file_class__'):
            return self.__file_class__(filepath)  # pylint: disable=no-member
        return self.__class__(filepath)

    def directory(self):
        """Return a path to the path's directory"""
        return self.parent

    def dirnames(self):
        """Split the dirname into individual directory names

        An absolute path starts with an empty string, a relative path does not

        >>> Path(u'/path/to/module.py').dirnames() == [u'', u'path', u'to']
        True
        >>> Path(u'path/to/module.py').dirnames() == [u'path', u'to']
        True
        """
        return self.dirname().split(os.path.sep)

    def dirpaths(self):
        """Split the dirname into individual directory names

        An absolute path starts with an empty string, a relative path does not

        >>> p = Path(u'/path/to/x.py')
        >>> p.paths == p.dirpaths()
        True
        """
        parts = self.split(os.path.sep)
        root, rest = Path('/'), parts[1:]
        return [makepath(root / os.path.sep.join(rest[:i]))
                for i in range(len(parts))]

    def directories(self):
        """Split the dirname into individual directory names

        No empty parts are included

        >>> Path(u'path/to/module.py').directories() == [u'path', u'to']
        True
        >>> Path(u'/path/to/module.py').directories() == [u'path', u'to']
        True
        """
        return [d for d in self.dirnames() if d]

    parents = property(
        dirnames, None, None,
        """ This path's parent directories, as a list of strings.

        >>> Path(u'/path/to/module.py').parents == [u'', u'path', u'to']
        True
        """)

    paths = property(
        dirpaths, None, None,
        """ This path's parent directories, as a sequence of paths.

        >>> paths = Path('/usr/bin/vim').paths
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

        >>> print Path('/home/guido/bin').short_relative_path_to(
        ...     '/home/guido/build/python.tar')
        ../build/python.tar
        >>> print Path('/home/guido/bin').short_relative_path_to(
        ...     '/mnt/guido/build/python.tar')
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
        else:
            return
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
        return self.expand().realpath().abspath()

    def same_path(self, other):
        return self.expandall() == other.expandall()


del path_path


class FilePath(Path, PathAssertions):
    """A path to a known file"""

    def __div__(self, child):
        raise PathError('%r has no children' % self)

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
            return [l.rstrip() for l in self.lines()]
        except IOError:
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
            ext = '%s.gz' % ext
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
        return self.__class__('%s.%s' % (filename, extension.lstrip('.')))

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
                first_line = self.lines()[0]
            except OSError:
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


def ext_language(ext):
    return {
        '.py': 'python',
        '.py2': 'python2',
        '.py3': 'python3',
        '.sh': 'bash',
        '.bash': 'bash',
        '.pl': 'perl',}[ext]


class ScriptPath(FilePath): # pylint: disable=too-many-ancestors
    """A file recognised by its interptreter

    The language is determined by extension

    >>> ScriptPath('/path/to/fred.py').language == 'python'
    True

    If there is no extension, but shebang is present, then use that
    (~/.bashrc might not exist - then there's no language)

    >>> p = ScriptPath(home() / '.bashr')
    >>> p.language == ('bash' if p.isfile() else None)
    True
    """

    @property
    def language(self):
        """The language of this script"""
        try:
            return self._language
        except AttributeError:
            if self.ext:
                language = ext_language(self.ext)
            else:
                shebang = self.shebang()
                language = shebang and str(shebang.name) or None
            self._language = language
        return self._language


class DirectPath(Path, PathAssertions):
    """A path which knows it might be a directory

    And that files are in directories
    """

    __file_class__ = FilePath


    def __iter__(self):
        for a_path in Path.listdir(self):
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
        return [self.as_existing_file(_) for _ in Path.listdir(self, pattern)]

    def make_directory_exist(self):
        if self.isdir():
            return False
        if os.path.exists(self):
            raise PathError('%s exists but is not a directory' % self)
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
    def walkfiles(self, pattern=None, errors='strict', ignores=None):
        def ignored(a_path):
            for ignore in ignores:
                if a_path.fnmatch_part(ignore):
                    return True
            return False

        if not ignores:
            ignores = []

        for path_to_file in super(DirectPath, self).walkfiles(pattern, errors):
            if not ignored(path_to_file):
                yield path_to_file


class ChmodValues(object):
    # pylint: disable=too-few-public-methods
    readonly_file = 0o444
    readonly_directory = 0o555


def makepath(string, as_file=False):
    """Make a path from a string

    Expand out any variables, home squiggles, and normalise it
    See also http://stackoverflow.com/questions/26403972/how-do-i-get-rid-of-make-xxx-method
    """
    if string is None:
        return None
    string_path = Path(string).expand()
    if string_path.isfile() or as_file:
        result = FilePath(string_path)
    else:
        result = DirectPath(string_path) # pylint: disable=redefined-variable-type
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
        raise PathError('Cannot cd to %s' % path_to)
    cd.previous = previous
    return True


try:
    cd.previous = makepath(os.getcwd())
except OSError:
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


def split_directories(strings):
    strings = strings_to_paths(strings)
    return [_
            for _ in strings
            if _.isdir()], [_ for _ in strings if not _.isdir()]


def split_files(strings):
    strings = strings_to_paths(strings)
    return ([_ for _ in strings if _.isfile()],
            [_ for _ in strings if not _.isfile()])


def split_directories_files(strings):
    strings = strings_to_paths(strings)
    return ([_ for _ in strings if _.isdir()],
            [_ for _ in strings if _.isfile()],
            [_ for _ in strings if not (_.isfile() or _.isdir())])


def files(strings):
    return split_files(strings)[0]


def directories(strings):
    return split_directories(strings)[0]


def home():
    return makepath('~')


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
