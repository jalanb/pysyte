from unittest import TestCase
from unittest.mock import patch

from pysyte.bash import screen

starting_callbacks = screen.atexit._ncallbacks()


class TestScreen(TestCase):
    def test_alt_screen(self):
        """Calling alt_screen should give a method to start such a screen

        And should register a method to stop it on exitting
            Cannot test that directly,
            Can only test that number of registered atexit funcs has increased
        """
        actual = screen.alt_screen()
        expected = screen._start_alt_screen
        self.assertEqual(actual, expected)
        current_callbacks = screen.atexit._ncallbacks()
        self.assertTrue(current_callbacks > starting_callbacks)

    def test_get_alt_screens(self):
        """get_alt_screens() should return 2 methods"""
        expected = screen._start_alt_screen, screen._stop_alt_screen
        actual = screen.get_alt_screens()
        self.assertEqual(actual, expected)

    @patch("pysyte.bash.screen.run")
    def test_start_alt_screen(self, run):
        """start_alt_screen should run the tput command smcup"""
        start_alt_screen, _ = screen.get_alt_screens()
        start_alt_screen()
        run.assert_called_with("tput smcup")

    @patch("pysyte.bash.screen.run")
    def test_not_stop_alt_screen(self, run):
        """stop_alt_screen will run "tput rmcup" if start_alt_screen() was run

        These tests do not actually run start_alt_screen()
            So stop_alt_screen() should do nothing
        """
        _, stop_alt_screen = screen.get_alt_screens()
        stop_alt_screen()
        run.assert_not_called()

    @patch("pysyte.bash.screen.run")
    def test_stop_alt_screen(self, run):
        """stop_alt_screen should run the tput command rmcup

        it will only run that command if the start_alt_screen() was run first
            These tests do not actually run that
            So we toggle a global sentinel
        """
        _, stop_alt_screen = screen.get_alt_screens()
        safe = screen._alt_screen_started
        try:
            screen._alt_screen_started = True
            stop_alt_screen()
        finally:
            screen._alt_screen_started = safe
        run.assert_called_with("tput rmcup")
