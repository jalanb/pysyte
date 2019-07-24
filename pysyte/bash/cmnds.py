# pylint: disable=unused-import

from functools import partial

try:
    from commands import getstatusoutput
    from commands import getoutput
except ImportError:
    import os
    import subprocess

    from subprocess import getoutput

    class CommandError(ValueError):
        pass


    def getstatusoutput(command):
        status, output = subprocess.getstatusoutput(command)
        if os.name != 'nt':
            # convert status to be interpreted according to the wait() rules
            status = status << 8
        return status, output

    def run(command :str, *args, **kwargs):
        if not command:
            return
        run_out = partial(subprocess.run, capture_output=True, encoding='utf-8')
        try:
            completed = run_out(command, *args, **kwargs)
        except FileNotFoundError:
            raise CommandError(f'Not found: {command}')
        if completed.returncode:
            raise CommandError(completed.stderr or completed.stdout)
        return completed.stdout
