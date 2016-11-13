"""Facilities for tracebacks"""

import re


def line_regexp():
    """Regular expression to match a traceback file line"""
    return re.compile(r'''\s*
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
    ''', re.VERBOSE)


def parse_line(string):
    """Parse a single string as traceback line"""
    match = line_regexp().match(string)
    if match:
        matches = match.groupdict()
        line_number = matches['line_number']
        path_to_python = matches['path_to_python']
        spaceless_path_to_python = matches['spaceless_path_to_python']
        if path_to_python:
            return path_to_python, line_number
        elif spaceless_path_to_python:
            return spaceless_path_to_python, line_number
