"""Test the decorators module"""


from cStringIO import StringIO
import unittest


from dotsite import decorators


@decorators.memoize
def initials(forename, surname, stream):
    """Print initials of the name

    Method is memoized, so we show an actual call by writing to stream
    """
    print >> stream, 'Call:', forename, surname
    return '%s%s' % (forename[0], surname[0])


@decorators.memoize
def no_args():
    return None


@decorators.memoize
def default_args(arg=None):
    return arg


def method():
    pass


def average(a, b, stream):
    result = (a + b) / 2
    print >> stream, 'Average of', a, 'and', b, 'is', result
    return result


class MemoizeTest(unittest.TestCase):
    def setUp(self):
        self.stream = StringIO()

    def test_first_call(self):
        self.assertEqual('FM', initials('Fred', 'Murphy', self.stream))
        self.assertEqual('Call: Fred Murphy\n',
                         self.stream.getvalue())

    def test_method_name(self):
        """A memoized method has been renamed"""
        self.assertEqual('memoize(initials)', initials.__name__)

    def test_method_docstring(self):
        docstring = initials.__doc__.splitlines()[0]
        self.assertEqual('Print initials of the name', docstring)

    def test_method_module(self):
        self.assertNotEquals(method.__module__, initials.__module__)

    def test_second_call_different_args(self):
        """Second call of method gives twice the output"""
        self.assertEqual('FS', initials('Fred', 'Smith', self.stream))
        self.assertEqual('FS', initials('Fred', 'Silly', self.stream))
        self.assertEqual('Call: Fred Smith\nCall: Fred Silly\n',
                         self.stream.getvalue())

    def test_second_call_same_args(self):
        """Second call of method with same args gives once the output

        Method was not actually called this time (nothing extra on stream)
            but produced the same output
        """
        self.assertEqual('FS', initials('Fred', 'Smith', self.stream))
        self.assertEqual('FS', initials('Fred', 'Smith', self.stream))
        self.assertEqual('Call: Fred Smith\n',
                         self.stream.getvalue())

    def test_invalidate(self):
        """Invalidating a cached call loses the memory

        So, after invalidation, it is actually called again

        Call twice with Fred - see only one call in the stream
        invalidate, then call again
            now a second call appears in the stream
        """
        self.assertEqual('FS', initials('Fred', 'Smith', self.stream))
        self.assertEqual('FS', initials('Fred', 'Smith', self.stream))
        self.assertEqual('Call: Fred Smith\n',
                         self.stream.getvalue())
        initials.invalidate()
        self.assertEqual('FS', initials('Fred', 'Smith', self.stream))
        self.assertEqual('Call: Fred Smith\nCall: Fred Smith\n',
                         self.stream.getvalue())

    def test_particular_invalidation(self):
        """Calls can be invalidated for particular arguments

        We test by invalidating for Fred
            then re-calling for Fred and John
            Fred gets re-added to the stream (full call)
            John doesn't
        """
        self.assertEqual('FS', initials('Fred', 'Smith', self.stream))
        self.assertEqual('FS', initials('Fred', 'Smith', self.stream))
        self.assertEqual('JS', initials('John', 'Silly', self.stream))
        self.assertEqual('Call: Fred Smith\nCall: John Silly\n',
                         self.stream.getvalue())
        initials.invalidate('Fred', 'Smith', self.stream)
        self.assertEqual('JS', initials('John', 'Silly', self.stream))
        self.assertEqual('FS', initials('Fred', 'Smith', self.stream))
        self.assertEqual(
            'Call: Fred Smith\nCall: John Silly\nCall: Fred Smith\n',
            self.stream.getvalue())

    def test_use_wtithout_decorator(self):
        memo_average = decorators.memoize(average)
        one = memo_average(1, 6, self.stream)
        two = memo_average(2, 5, self.stream)
        three = memo_average(1, 6, self.stream)
        self.assertEqual(one, two)
        self.assertEqual(two, three)
        self.assertEqual('Average of 1 and 6 is 3\nAverage of 2 and 5 is 3\n',
                         self.stream.getvalue())

    def test_no_arguments(self):
        """Methods without arguments can lead to barfing in some memoisers"""
        self.assertIsNone(no_args())
        self.assertIsNone(no_args())

    def test_default_arguments(self):
        """Methods without arguments can lead to barfing in some memoisers

        Defaults are a slightly different form of "no args"
        """
        self.assertIsNone(default_args())
        self.assertIsNone(default_args())

    def test_mutable_arguments(self):
        """Call with lists is handled (despite list not being hashable)"""
        self.assertEqual('FS',
                         initials(['F', 'red'], ['S', 'mith'], self.stream))
        self.assertEqual('FS',
                         initials(['F', 'red'], ['S', 'mith'], self.stream))
        self.assertEqual("Call: ['F', 'red'] ['S', 'mith']\n",
                         self.stream.getvalue())
