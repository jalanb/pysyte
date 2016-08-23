"""This module handles lists"""


def de_duplicate(items):
    """Remove any duplicate item, preserving order"""
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result
