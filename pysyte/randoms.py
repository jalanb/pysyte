"""
This module provides functions for making random choices, such as flipping a coin.

Examples:
    >>> from pysyte.randoms import coin
    >>> assert coin() in ('heads', 'tails')
"""

import random


def flip() -> bool:
    """
    Flip a coin and return a boolean value.

    >>> assert flip() in (True, False)
    """
    return random.choice((True, False))


def coin() -> str:
    """
    Simulate a coin flip and return the result as a string.

    >>> assert coin() in ('heads', 'tails')
    """
    return "heads" if flip() else "tails"
