"""Handle tracebacks for pysyte"""

import re


def parse_line(string):
    """Parse a single string as traceback line"""

    line_regexp = re.compile(
        r"""\s*
            File\s
            (
                (
                    ["']
                    (?P<path_to_python>[^"']+)
                    ["']
                ) | (
                    (?P<spaceless_path_to_python>[^ ]+)
                )
            )
            ,\sline\s
            (?P<line_number>[0-9]+)
            ,.in..*
        """,
        re.VERBOSE,
    )
    match = line_regexp.match(string)
    if match:
        matches = match.groupdict()
        line_number = int(matches["line_number"])
        path_to_python = matches["path_to_python"]
        spaceless_path_to_python = matches["spaceless_path_to_python"]
        if path_to_python:
            return path_to_python, line_number
        elif spaceless_path_to_python:
            return spaceless_path_to_python, line_number
