"""Methods for handling lines (of text)"""
import re
from functools import partial


def _chop(lines_in, at, first, last):

    def as_int(string, start, end):
        try:
            return int(string)
        except (ValueError, TypeError):
            lines = lines_in[at:at] if at else lines_in[start:end]
            matcher = re.compile(string)
            for i, line in enumerate(lines, 1 + start):
                if matcher.search(line):
                    return i
        return 0

    def _line(i):
        line = i if i >= 0 else length_read + 1 + i
        if line >= length_read:
            return length_read
        return 0 if line < 1 else line

    def _boundaries():
        if at:
            start = first if first else 0
            end = last if last else -1
            first_ = _line(as_int(at, start, end) - 1)
            return first_, first_ + 1
        first_ = _line(as_int(first, 0, -1) - 1)
        last_ = _line(as_int(last, first_, -1) or -1)
        return first_, last_

    length_read = len(lines_in)
    first, last = _boundaries()
    rest = [] if first > length_read else lines_in[first:last]
    return first, rest


def first_and_rest(text, at=None, first=1, last=-1):
    """First line, and rest of those lines from that text

    at, first, last :
        each can choose a line by number or regexp
        line numbers start at 1, and end at -1
    at: choose this line only
    first: first line to choose
    last: last line to choose
    """
    lines_in = text.splitlines()
    return _chop(lines_in, at, first, last)


def set_width(line, width):
    if not width:
        return line
    return line[:width]

def _number_format(count=999):
    """A string format for line numbers

    Should give a '%d' format with width big enough to `count` lines

    >>> assert _number_format(77) == '%2d: '
    """
    digits = len(str(count))
    return '%%%dd: ' % digits


def add_numbers(lines, first, numbers):
    if not numbers:
        numbered = lambda x, y: x
    else:
        def numbered(line_, line_format_):
            prefix = line_format_ % (first + i + 1)
            return ' '.join((prefix, line_.rstrip()))

    for i, line in enumerate(lines):
        yield numbered(line, _number_format(len(lines)))


def reformat_lines(lines, first, numbers, width):
    return [l[:width] if width else l for l in add_numbers(lines, first, numbers)]


def as_text(lines):
    return '\n'.join(lines)


def select(predicate, lines):
    for line in lines:
        if not predicate(line):
            continue
        yield line

def result(converter, lines):
    for line in lines:
        yield converter(line)

_selector = lambda lambda_, lines_: (i for i in lines_ if lambda_(i))
_converter = lambda lambda_, lines_: (lambda_(i) for i in lines_)

full = lambda lines_: _converter(
    lambda line: line.rstrip(),
    _selector(lambda line: line.rstrip(), lines_)
)
grep = lambda lines_: lambda regexp: _selector(lambda line: line and re.search(regexp, line), lines_)
