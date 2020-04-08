"""A collection of extended path classes and methods

The classes all inherit from the original path.path
"""
import os
import re
import stat
import importlib
from fnmatch import fnmatch
from functools import singledispatch

from pysyte.types.lists import flatten


class PathError(Exception):
    """Something went wrong with a path"""
    prefix = 'Path Error'

    def __init__(self, message):
        Exception.__init__(self, message)


class PathAssertions:
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


from path import Path as PPath  # pylint: disable=wrong-import-order,wrong-import-position


class NonePath(object):
    def __init__(self, string=None):
        self.string = string if string else ''
        self.proxy = DirectPath(self.string)

    def __str__(self):
        return self.string

    def __repr__(self):
        return f'<{self.__class__.__name__} "{str(self)}">'

    def __bool__(self):
        return False

    def __eq__(self, other):
        if self.string:
            return str(self) == str(other)
        return not other

    def __lt__(self, other):
        return bool(other)

    def __contains__(self, _):
        return False

    def __div__(self, child):
        result = os.path.join(self.string, child) if child else self.string
        return makepath(result)

    __truediv__ = __div__

    @property
    def parent(self):
        if '/' not in self.string:
            return None
        parent_string = '/'.join(self.string.split('/')[:-1])
        return makepath(parent_string)

    def exists(self):
        return False

    isdir = isfile = exists

    def __getattr__(self, name):
        return getattr(self.proxy, name, None)


class DotPath(PPath):
    """Some additions to the classic path class"""
    # pylint: disable=abstract-method
    # pylint: disable=too-many-public-methods

    def __hash__(self):
        return hash(str(self))

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
        string = str(self)
        result = os.path.join(string, child) if child else string
        return makepath(result)

    __truediv__ = __div__

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def basename(self):
        return str(super().basename())

    @property
    def name(self):
        return str(super().name)

    def isroot(self):
        return str(self) == '/'

    def parent_directory(self):
        if self.isroot():
            return None
        return self.parent

    def parent_directories(self):
        if self.isroot():
            return []
        parent = self.parent
        if not parent:
            return []
        return [parent] + parent.parent_directories()

    def directory(self):
        """Return a path to the path's directory"""
        return self.parent

    def dirnames(self):
        """Split the dirname into individual directory names

        An absolute path starts with an empty string, a relative path does not

        >>> DotPath('/path/to/module.py').dirnames() == ['/', 'path', 'to']
        True
        >>> DotPath('path/to/module.py').dirnames() == ['path', 'to']
        True
        """
        return [str(_) for _ in self.directory().split(os.path.sep)]

    def dirpaths(self):
        """Split the dirname into individual directory names

        An absolute path starts with an empty string, a relative path does not

        >>> p = DotPath('/path/to/x.py')
        >>> assert p.paths == p.dirpaths()
        """
        parts = self.split()
        result = [DotPath(parts[0] or '/')]
        for name in parts[1:]:
            result.append(result[-1] / name)
        return result

    def directories(self):
        """Split the dirname into individual directory names

        No empty parts are included

        >>> DotPath('path/to/module.py').directories() == ['path', 'to']
        True
        >>> DotPath('/path/to/module.py').directories() == ['/', 'path', 'to']
        True
        """
        return [d for d in self.dirnames() if d]

    parents = property(
        dirnames, None, None,
        """ This path's parent directories, as a list of strings.

        >>> DotPath('/path/to/module.py').parents == ['/', 'path', 'to']
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

    def split(self, sep=None, maxsplit=-1):
        separator = sep or os.path.sep
        parts = super().split(separator, maxsplit)
        parts[0] = makepath(parts[0] if parts[0] else '/')
        return parts
        root, *names = self.splitall()
        path_ = makepath(str(root))
        result = [path_]
        for name in names:
            path_ = path_ / name
            if not path_.isdir():
                break
            result.append(path_)
        return result

    def abspath(self):
        return makepath(os.path.abspath(str(self)))

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
        if len(str(relative)) < len(str(absolute)):
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
            return
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

    def expand(self):
        _expand = lambda x : os.path.expanduser(os.path.expandvars(x))
        try:
            p = makepath(_expand(self))
            return p.realpath().abspath()
        except AttributeError:
            assert False, str(self.__class__(
                os.path.abspath(os.path.realpath(
                    os.path.expanduser(os.path.expandvars(str(
                        self
            )))))))

    def same_path(self, other):
        return self.expand() == other.expand()

    @property
    def hidden(self):
        """A 'hidden file' has a name starting with a '.'"""
        s = str(self.basename())
        return s and s[0] == '.'

    def add_ext(self, *args):
        """Join all args as extensions

        Strip any leading `.` from args

        >>> source = makepath(__file__)
        >>> new = source.add_ext('txt', '.new')
        >>> assert new.name.endswith('.py.txt.new')
        """
        exts = [(a[1:] if a[0] == '.' else a) for a in args]
        string = '.'.join([self] + list(exts))
        return makepath(string)

    def add_missing_ext(self, ext):
        """Add that extension, if it is missing

        >>> fred = makepath('fred.py')
        >>> assert fred.add_missing_ext('.py') == fred
        >>> assert fred.add_missing_ext('.txt').endswith('.py.txt')
        """
        copy = self[:]
        _stem, old = os.path.splitext(copy)
        extension = f'.{ext.lstrip(".")}'
        if old == extension:
            return makepath(self)
        return self.add_ext(extension)

    def is_executable(self):
        """Whether the path is executable"""
        # pylint: disable=no-self-use
        return False

    def isexec(self):
        return self.is_executable()

    def has_executable(self):
        """Whether the path has any executable bits set """
        executable_bits = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
        try:
            return bool(os.stat(self).st_mode & executable_bits)
        except OSError:
            return False


def ext_language(ext, exts=None, simple=True):
    """Language of the extension in those extensions

    If exts is supplied, then restrict recognition to those exts only
    If exts is not supplied, then use all known extensions

    >>> ext_language('.py') == 'python'
    True
    """
    languages = {
        '.py': 'python',
        '.py2': 'python' if simple else 'python2',
        '.py3': 'python' if simple else 'python3',
        '.sh': 'bash',
        '.bash': 'bash',
        '.pl': 'perl',
        '.txt': 'english',
    }
    ext_languages = {_: languages[_] for _ in exts} if exts else languages
    return ext_languages.get(ext)

def mime_language(ext, exts=None):
    if ext == '.txt':
        return 'txt'
    language = ext_language(ext, exts, True)
    if language:
        return f'txt/{language}'
    return ''


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

    def is_executable(self):
        """Whether the file has any executable bits set"""
        return self.has_executable()

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

    def split_exts(self):
        """Split all extensions from the path

        >>> p = FilePath('here/fred.tar.gz')
        >>> assert p.split_exts() == ('here/fred', '.tar.gz')
        """
        copy = self[:]
        filename, ext = os.path.splitext(copy)
        if ext == '.gz':
            filename, ext = os.path.splitext(filename)
            ext = f'{ext}.gz'
        return self.__class__(filename), ext

    split_all_ext = split_ext = split_exts

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

    def mimetype(self):
        import magic  # pylint: disable=import-outside-toplevel
        result = magic.from_file(str(self))
        if result.startswith('txt'):
            return mime_language(self.ext)
        return result


class DirectPath(DotPath, PathAssertions):
    """A path which knows it might be a directory

    And that files are in directories
    """

    __file_class__ = FilePath

    def __iter__(self):
        for a_path in DotPath.listdir(self):
            yield a_path

    def __contains__(self, thing):
        return self.contains(thing)

    def contains(self, thing):
        try:
            _ = thing.contains
            return str(thing).startswith(str(self))
        except AttributeError:
            return thing in str(self)

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
        for child in reversed([self.walkdirs()]):
            if child == self or not child.isdir():
                continue
            child.rmdir()

    def cd(self):  # pylint: disable=invalid-name
        """Change program's current directory to self"""
        return cd(self)

    def listdir(self, pattern=None):
        return [self._next_class(_)
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
        return True

    def make_file_exist(self, filename=None):
        """Make the directory exist, then touch the file

        If the filename is None, then use self.name as filename
        """
        if filename is None:
            path_to_file = FilePath(self)
            path_to_file.make_file_exist()
            return path_to_file
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
        ignored = ignore_fnmatches(ignores)
        for path_to_dir in super(DirectPath, self).walkdirs(pattern, errors):
            if not ignored(path_to_dir.relpath(self)):
                yield path_to_dir

    # pylint: disable=arguments-differ
    def walkfiles(self, pattern=None, errors='strict', ignores=None):
        ignored = ignore_fnmatches(ignores)
        for path_to_file in super(DirectPath, self).walkfiles(pattern, errors):
            if not ignored(path_to_file.relpath(self)):
                yield path_to_file

    def listfiles(self, pattern=None, ignores=None):
        ignored = ignore_fnmatches(ignores)
        return [_ for _ in self.listdir(pattern) if _.isfile() and not ignored(_)]

    def has_vcs_dir(self):
        for vcs_dir in ('.git', '.svn', '.hg'):
            if self.fnmatch_part(vcs_dir):
                return True
        return False


def ignore_fnmatches(ignores):

    def ignored(a_path):
        if not ignores:
            return False
        for ignore in ignores:
            if a_path.fnmatch_part(ignore):
                return True
        return False

    return ignored


class ChmodValues:
    # pylint: disable=too-few-public-methods
    readonly_file = 0o444
    readonly_directory = 0o555


def _make_module_path(arg):
    """Make a path from a thing that has a module

    classes and functions have modules, they'll be needing this
    """
    try:
        return makepath(importlib.import_module(arg.__module__))
    except (AttributeError, ModuleNotFoundError):
        return None

@singledispatch
def makepath(arg):
    attribute = getattr(arg, 'path', False)
    return makepath(attribute) if attribute else makepath(str(arg))


path = makepath


@makepath.register(type(None))
def _(arg):
    return NonePath()


@makepath.register(DotPath)
def _(arg):
    return arg


@makepath.register(str)
def _(arg):
    """Make a path from a string

    Expand out any variables, home squiggles, and normalise it
    See also http://stackoverflow.com/questions/26403972
    """
    if not arg:
        return NonePath()
    if os.path.isfile(arg):
        return FilePath(arg)
    if os.path.isdir(arg):
        return DirectPath(arg)
    v = os.path.expandvars(arg)
    u = os.path.expanduser(v)
    if arg == u:
        return NonePath(arg)
    if os.path.exists(u):
        return makepath(u)
    return NonePath(arg)


@makepath.register(type(os))
def _(arg):
    """Make a path from a module"""
    if arg == 'builtins':
        return None
    return makepath(arg.__file__)


@makepath.register(type(makepath))
def _(arg):
    """Make a path from a function's module"""
    terminal_regexp = re.compile('<(stdin|.*python-input.*)>')
    method = getattr(arg, '__wrapped__', arg)
    filename = method.__code__.co_filename
    if terminal_regexp.match(filename):
        return None
    return _make_module_path(method)


@makepath.register(type(DotPath))
def _(arg):
    """Make a path from a class's module"""
    return _make_module_path(arg)


def makestr(string: str):
    """Make a path from a string"""
    if not string:
        return ''
    if os.path.isfile(string) or os.path.isdir(string):
        return makepath(string)
    return string


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
    elif not path_to.exists():
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
    paths_ = strings_to_paths(strings)
    return [_
            for _ in paths_
            if _.isdir()], [_ for _ in paths_ if not _.isdir()]


def split_files(strings):
    paths_ = strings_to_paths(strings)
    return ([_ for _ in paths_ if _.isfile()],
            [_ for _ in paths_ if not _.isfile()])


def split_directories_files(strings):
    paths_ = strings_to_paths(strings)
    return ([_ for _ in paths_ if _.isdir()],
            [_ for _ in paths_ if _.isfile()],
            [_ for _ in paths_ if not (_.isfile() or _.isdir())])


def files(strings):
    return split_files(strings)[0]


def directories(strings):
    return split_directories(strings)[0]


def tmp():
    return makepath('/tmp')


def home():
    _home = makepath(os.path.expanduser('~'))
    assert _home
    _x = _home.expand()
    return _home


def pwd():
    return makepath(os.getcwd())


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


def fnmatcher(pattern, path_to_directory=None, wanted=lambda x: True):
    """Gives a method to check if an item matches the pattern, and is wanted

    If path_to_directory is given then items are checked there
    By default, every item is wanted
    """
    return lambda x: fnmatch(x, pattern) and wanted(
        os.path.join(path_to_directory, x) if path_to_directory else x)


def list_items(path_to_directory, pattern, wanted=lambda x: True):
    """All items in the given path which match the given glob and are wanted

    By default, every path is wanted
    """
    if not path_to_directory:
        return set()
    needed = fnmatcher(pattern, path_to_directory, wanted)
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


def contains_glob(path_to_directory, pattern, wanted=lambda x: True):
    """Whether the given path contains an item matching the given glob"""
    if not path_to_directory:
        return False
    needed = fnmatcher(pattern, path_to_directory, wanted)
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


def add_star(string):
    """Add '.*' to string

    >>> assert add_star('fred') == 'fred.*'
    """
    suffix = '*' if '.' in string else '.*'
    return f'{string}{suffix}'

def add_stars(strings):
    """Add '.*' to each string

    >>> assert add_stars(['fred', 'Fred.']) == ['fred.*', 'Fred.*']
    """
    paths_ = [strings] if isinstance(strings, str) else strings
    return [add_star(p) for p in paths_]


def tab_complete_files(paths_, globber):
    return tab_complete(paths_, globber, os.path.isfile)


def tab_complete_dirs(paths_, globber):
    return tab_complete(paths_, globber, os.path.isdir)


def tab_complete(strings, globber=add_stars, select=os.path.exists):
    """Finish path names "left short" by bash's tab-completion

    strings is a string or strings
        if any string exists as a path return those as paths

    globber is a method which should return a list of globs
        default: add_stars(['fred.']) == ['fred.*']
            or, e.g: add_python(['fred', 'fred.']) == ['fred.py*']
        if any expanded paths exist return those

    select is a method to choose wanted paths
        Defaults to selecting existing paths
    """
    strings_ = [strings] if isinstance(strings, str) else strings
    globs = flatten([globber(s) for s in strings_])
    here_ = pwd()
    matches = []
    for glob_ in globs:
        if '/' in glob_:
            directory, base = os.path.split(glob_)
            dir_ = here_ / directory
        else:
            dir_ = here_
            base = glob_
        match = [p for p in dir_.listdir() if p.fnmatch_basename(base)]
        matches.extend(match)
    result = [p for p in set(matches) if select(p)]
    return result if result[1:] else strings


def pyc_to_py(path_to_file):
    """Change some file extensions to those which are more likely to be text

    >>> pyc_to_py('vim.pyc') == 'vim.py'
    True
    """
    stem, ext = os.path.splitext(path_to_file)
    if ext == '.pyc':
        return f'{stem}.py'
    return path_to_file
