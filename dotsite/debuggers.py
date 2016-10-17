"""Proxies for known debuggers"""

import inspect
from bdb import BdbQuit as DebugExit  # pylint: disable=unused-import


class Debugger(object):
    """Proxy to a debugger"""
    def break_here(self, _frame):
        raise NotImplementedError('To do: breakpoints in de other buggers')


def source_of(frame):
    return frame.f_code.co_filename, frame.f_lineno

try:
    import pudb

    class PudbDebugger(Debugger):
        def __init__(self):
            self.frame = None

        @property
        def debugger(self):
            debuggers = pudb.CURRENT_DEBUGGER
            return debuggers and debuggers[0] or None

        def _break_at(self, frame):
            self.frame = frame
            filename, lineno = source_of(frame)
            pudb.settings.save_breakpoints(
                pudb.settings.load_breakpoints() + [(
                    filename, lineno, False, None, None)])
            if self.debugger:
                self.debugger.reload_breakpoints(0, 0, 0)  # args not used

        def _continue(self, frame):
            if self.debugger:
                pudb.set_interrupt_handler()
                self.debugger.set_trace(frame)
            else:
                pudb.set_trace()

        def break_here(self, frame):
            self._break_at(frame)
            self._continue(frame)

    debugger = PudbDebugger()
except ImportError:
    class PdbDebugger(Debugger):
        def break_here(self, _frame):
            raise NotImplementedError('To do: breakpoints in pdb')

    debugger = PdbDebugger()  # pylint: disable=redefined-variable-type


def debug_here():
    pudb.set_trace()
    frame = inspect.currentframe().f_back
    debugger.break_here(frame)
