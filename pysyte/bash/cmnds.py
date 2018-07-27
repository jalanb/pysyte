# pylint: disable=unused-import

try:
    from commands import getstatusoutput
    from commands import getoutput
except ImportError:
    import os
    import subprocess

    from subprocess import getoutput

    def getstatusoutput(command):
        status, output = subprocess.getstatusoutput(command)
        if os.name != 'nt':
            # convert status to be interpreted according to the wait() rules
            status = status << 8
        return status, output
