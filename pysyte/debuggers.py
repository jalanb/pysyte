"""Proxies for known debuggers"""

import inspect
from bdb import BdbQuit as DebugExit  # pylint: disable=unused-import


try:
    from pprintpp import pprint as pp
except ImportError:
    from pprint import pprint as pp


def ppd(_):
    return pp(dir(_))


def ppv(_):
    return pp(vars(_))


def source_of(frame):
    return frame.f_code.co_filename, frame.f_lineno


class Debugger(object):
    """Proxy to a debugger"""
    def _continue(self, frame):
        raise NotImplementedError('To do: running in de other buggers')

    def save_breaks(self, breakpoints):
        raise NotImplementedError('To do: breakpoints in de other buggers')

    def load_breaks(self):
        raise NotImplementedError('To do: breakpoints in de other buggers')

    def _break_on(self, frame):
        filename, lineno = source_of(frame)
        self.add_break(filename, lineno)

    def break_here(self, frame):
        self._break_on(frame)
        self._continue(frame)

    def add_break(self, filename, lineno):
        self.add_breaks([(filename, lineno)])

    def _make_break(self, filename, lineno):  # pylint: disable=no-self-use
        return (filename, lineno)

    def add_breaks(self, filenames_lines):
        self.save_breaks(
            self.load_breaks() + [
                self._make_break(f, l) for f, l in filenames_lines
            ])


class PythonDebugger(Debugger):
    def _continue(self, frame):
        raise NotImplementedError('To do: running in de other buggers')

    def save_breaks(self, breakpoints):
        raise NotImplementedError('To do: breakpoints in de other buggers')

    def load_breaks(self):
        raise NotImplementedError('To do: breakpoints in de other buggers')


class PudbDebugger(Debugger):
    """Proxy to the pudb debugger"""
    @property
    def debugger(self):
        try:
            return pudb.CURRENT_DEBUGGER[0]
        except IndexError:
            return None

    def _make_break(self, filename, lineno):
        return (filename, lineno, False, None, None)

    def _continue(self, frame):
        if self.debugger:
            pudb.set_interrupt_handler()
            self.debugger.set_trace(frame)
        else:
            pudb.set_trace()

    def break_here(self, frame):
        # pylint: disable=protected-access
        if self.debugger:
            self.debugger.break_here(frame)
        else:
            dbg = pudb._get_debugger()
            import threading
            if isinstance(threading.current_thread(), threading._MainThread):
                pudb.set_interrupt_handler()
            dbg.set_trace(frame)

    def save_breaks(self, breakpoints):
        class PudbBreakpoint(object):
            """Cadged from .../pudb/settings.py

            https://github.com/inducer/pudb/blob/master/pudb/settings.py#L494
            """
            def __init__(self, filename, lineno, condition):
                self.file = filename
                self.line = lineno
                self.cond = condition

        save_breakpoints = [PudbBreakpoint(*b[:3]) for b in breakpoints]
        pudb.settings.save_breakpoints(save_breakpoints)

    def load_breaks(self):
        return pudb.settings.load_breakpoints()

    def add_breaks(self, filenames_lines):
        super(PudbDebugger, self).add_breaks(filenames_lines)
        if self.debugger:
            self.debugger.reload_breakpoints(0, 0, 0)  # args not used


class IPythonDebugger(object):
    """Proxy to ipdb's debugger"""
    def _continue(self, frame):
        raise NotImplementedError('To do: running in de other buggers')

    def save_breaks(self, breakpoints):
        raise NotImplementedError('To do: breakpoints in de other buggers')

    def load_breaks(self):
        raise NotImplementedError('To do: breakpoints in de other buggers')


try:
    import pudb
    db = PudbDebugger()
except ImportError:
    try:
        # pylint: disable=redefined-variable-type
        db = IPythonDebugger()
    except ImportError:
        db = PythonDebugger()


def debug_here(really=True):
    if not really or not db:
        return
    frame = inspect.currentframe().f_back
    db.break_here(frame)


def stack_sources():
    """A list of sources for frames above this"""
    # lazy imports
    import linecache
    result = []
    for frame_info in reversed(inspect.stack()):
        _frame, filename, line_number, _function, _context, _index = frame_info
        linecache.lazycache(filename, {})
        _line = linecache.getline(filename, line_number).rstrip()

    # Each record contains a frame object, filename, line number, function
    # name, a list of lines of context, and index within the context
    _sources = [(path, line) for _, path, line, _, _, _ in inspect.stack()]
    return result
