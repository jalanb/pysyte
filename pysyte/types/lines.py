"""Methods for handling lines (of text)"""
import re


def _chop(lines_in, at, first, last):
    def as_int(string, start, end):
        try:
            return int(string)
        except (ValueError, TypeError):
            lines = lines_in[at:at] if isinstance(at, int) else lines_in[start:end]
            matcher = re.compile(string)
            for i, line in enumerate(lines, 1 + start):
                if matcher.search(line):
                    return i
        return 0

    def boundaries():
        def line(i):
            line = i if i >= 0 else length_read + 1 + i
            if line >= length_read:
                return length_read
            return 0 if line < 1 else line

        if at:
            start = first if first else 0
            end = last if last else -1
            first_ = line(as_int(at, start, end) - 1)
            return first_, first_ + 1
        first_ = line(as_int(first, 0, -1) - 1)
        last_ = line(as_int(last, first_, -1) or -1)
        return first_, last_

    length_read = len(lines_in)
    first, last = boundaries()
    rest = [] if first > length_read else lines_in[first:last]
    return first, rest


def chop(text, at, first=1, last=-1):
    r"""Make that text fit those boundaries

    >>> lines = ['one', 'two', 'three', 'four']
    >>> text = '\n'.join(lines)

    >>> assert 'three' not in chop(text, 1, last=2 )

    >>> assert chop(text, at=2) == chop(text, '[t][w][o]' )
    """
    return _chop(text.splitlines() or [], at, first, last)


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
    return "%%%dd: " % digits


def add_numbers(lines, first=0):
    def numbered(line_, line_format_):
        prefix = line_format_ % (first + i + 1)
        return f"{prefix}{line_.rstrip()}"

    for i, line in enumerate(lines):
        yield numbered(line, _number_format(len(lines) + first))


def sed(lines, args):
    return reformat_lines(
        lines, first=args.first, numbers=args.numbers, width=args.width
    )


def reformat_lines(lines, first, numbers, width):
    adder = add_numbers if numbers else lambda x, y: x
    return list(adder([_[:width] if width else _ for _ in lines], first))


def select(predicate, lines):
    for line in lines:
        if not predicate(line):
            continue
        yield line


_selector = lambda method, lines_: (_ for _ in lines_ if method(_))
_converter = lambda method, lines_: (method(_) for _ in lines_)

full = lambda lines_: _converter(
    lambda line: line.rstrip(), _selector(lambda line: line.rstrip(), lines_)
)
grep = lambda lines_: lambda regexp: _selector(
    lambda line: line and re.search(regexp, line), lines_
)


def arg_lines(text, args):
    return chop(text, args.at, args.first, args.last)


def as_text(lines):
    return "\n".join(lines)
