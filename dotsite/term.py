import commands


def _tput(tput_command):
    command='tput %s' % tput_command
    status, output = commands.getstatusoutput(command)
    if status:
        raise NotImplementedError(output)
    if not output:
        return 0
    try:
        return int(output) - 1
    except TypeError:
        return 0


def screen_width():
    return _tput('cols')


def screen_height():
    return _tput('lines')
