"""Methods for handling lines (of text)"""
import re
from functools import partial


def _chop(lines_in, at, first, last):

    def as_int(string, at, start, end):
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
            first_ = _line(as_int(at, at, start, end))
            return first_, first_ + 1
        first_ = _line(as_int(first, 0, 0, -1) - 1)
        last_ = _line(as_int(last, 0, first, -1) or -1)
        return first_, last_

    length_read = len(lines_in)
    first, last = _boundaries()
    lines_out = [] if first > length_read else lines_in[first:last]
    return lines_out, first


def first_and_rest(text_stream, at=None, first=1, last=-1):
    """Retrn first line, and rest of lines from that text stream

    at, first, last :
        each can choose a line by number or regexp
        line numbers start at 1, and end at -1
    at: choose this line only
    first: first line to choose
    last: last line to choose
    """
    text = text_stream.read()
    lines_in = text.splitlines()
    lines_out, first = _chop(lines_in, at - 1, first - 1, last)


def reformat_lines(lines, first, numbers, width):
    line_format_ = _number_format(len(lines_out))
    for i, line in enumerate(lines_out, first):
        if numbers:
            prefix = line_format_ % (i + 1)
            out = ' '.join((prefix, line.rstrip()))
        else:
            out = line.rstrip()
        if width:
            out = out[:width]


def _number_format(count=999):
    """A string format for line numbers

    Should give a '%d' format with width bug enough to `count` lines
    """
    digits = len(str(count))
    return '%%%dd: ' % digits


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
