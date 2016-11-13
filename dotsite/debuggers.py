"""Proxies for known debuggers"""

import inspect
from bdb import BdbQuit as DebugExit  # pylint: disable=unused-import


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

    def _make_break(self, filename, lineno):
        return (filename, lineno)

    def add_breaks(self, filenames_lines):
        self.save_breaks(
            self.load_breaks() + [
                _make_break(f, l) for f, l in filenames_lines
            ])


class PudbDebugger(Debugger):
    """Proxy to the pudb debugger"""
    @property
    def debugger(self):
        debuggers = pudb.CURRENT_DEBUGGER
        return debuggers and debuggers[0] or None

    def _make_break(self, filename, lineno):
        return (filename, lineno, False, None, None)

    def _continue(self, frame):
        if self.debugger:
            pudb.set_interrupt_handler()
            self.debugger.set_trace(frame)
        else:
            pudb.set_trace()

    def save_breaks(self, breakpoints):
        pudb.settings.save_breakpoints(breakpoints)

    def load_breaks(self):
        return pudb.settings.load_breakpoints()

    def add_breaks(self, filenames_lines):
        super(PudbDebugger, self).add_breaks(filenames_lines)
        if self.debugger:
            self.debugger.reload_breakpoints(0, 0, 0)  # args not used


class PymDebugger(object):
    """Proxy to pym's debugger"""
    def _continue(self, frame):
        pymdb.continue_(frame)

    def save_breaks(self, breakpoints):
        return pymdb.save_breaks(breakpoints)

    def load_breaks(self):
        return pymdb.load_breaks()


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
        import ipdb
        db = IPythonDebugger()
    except ImportError:
        from pym.debugger import pymdb
        db = PymDebugger()


def debug_here():
    pudb.set_trace()
    frame = inspect.currentframe().f_back
    db.break_here(frame)
