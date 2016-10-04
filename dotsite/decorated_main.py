#! python3
"""A simpler main program

Usage:
"""
"""

import dotsite as site

def py_catcher(glob, path):
    assert path.isfile() or path.isdir()
    assert glob.ext == path.ext
    if not glob.scripts:
        print('Please enter Python globs on command line', file=sys.stderr)
        return False
    assert path.ext and path.ext.startswith('.py')
    assert 'Python' in glob.scripts.languages


def world(arg):
    assert arg in ['-w', '--hello']
    print('Hello World')


@site.decorators.streamer
@site.decorators.globber([(py_catcher, '*.py')])
@site.decorators.argparser((world, '-w', '--hello', 'Say "Hello World"'))
def main(streams, globs):
    for stream in streams:
        if stream.read() in 'qQ':
            return True
    for glob in globs:
        assert os.path.isfile(glob)
        assert os.path.splitext(glob) == '.py'
    return True


sys.exit(site.main(main, __name__))
"""

import sys

def py_catcher(glob, path):
    class Scripts(object):
        def __init__(self, languages = None):
            self.languages = languages and languages or defaultdict(set)

    glob.scripts = Scripts()
    if glob.ext in ('.py', 'py[0-9]'):
        glob.scripts.languages |= 'Python'
    else:
        matches = re.search('([Pp]ython|PYTHON)([2-9])', path.lines[0])
        if bool(matches):
            glob.scripts.languages |= 'Python'
            groups = match.groups()
            import pudb
            pudb.set_trace()
            glob.scripts.languages |= 'Python%s' % groups[1]
    if '__name__ == "__main__"' in path.text:
        glob.scripts.languages |= 'Executable'


def main(method, name):
    import os
    if name != '__main__':
        return os.EX_USAGE
    result = method(sys.argv)
    return result and os.EX_OK or result

if __name__ == '__main__':
    sys.exit(main(main, __name__))
