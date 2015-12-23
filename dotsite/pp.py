"""Methods to ease pprinting"""

try:
    from pprintpp import pprint as pp
except ImportError:
    from pprint import pprint as pp

