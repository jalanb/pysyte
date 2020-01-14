# pylint: disable=unused-import
"""Run bash commands"""

try:
    from commands import getstatusoutput
    from commands import getoutput
except ImportError:
    import os
    import shlex
    import subprocess

    from functools import partial
    from subprocess import getoutput

    from pysyte.types.paths import home

    class CommandError(ValueError):
        pass

    def getstatusoutput(command):
        status, output = subprocess.getstatusoutput(command)
        if os.name != 'nt':
            # convert status to be interpreted according to the wait() rules
            status = status << 8
        return status, output

    def run(*args, **kwargs):
        if not args:
            raise CommandError('No command')
        run_out = partial(subprocess.run, capture_output=True, encoding='utf-8')
        try:
            home_bin = home() / 'bin'
            default_paths = ['/usr/local/bin', '/usr/bin', '/bin']
            if home_bin.isdir():
                default_paths.insert(0, home_bin)
            default_path = ':'.join(default_paths)
            # env_path = os.environ.get("PATH", default_path)
            env_command = [
                '/usr/bin/env',
                f'PATH={default_path}',
            ]
            arg_commands = args
            if len(args) == 1:
                arg = args[0]
                if isinstance(arg, str):
                    arg_commands = shlex.split(arg)
                elif isinstance(arg, list):
                    arg_commands = arg
            env_command.extend(arg_commands)
            completed = run_out(env_command, **kwargs)
        except FileNotFoundError:
            raise CommandError(f'Not found: {" ".join(env_command)}')
        if completed.returncode:
            raise CommandError(completed.stderr or completed.stdout)
        return completed.stdout
