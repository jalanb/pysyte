
class Server(object):
    pass


class Protocol(object):
    def __init__(self, server):
        pass


class File(Protocol):
    name = 'file'


class Http(Protocol):
    name = 'http'


class Https(Protocol):
    name = 'https'


class Git(Protocol):
    name = 'git'


class Ssh(Protocol):
    name = 'ssh'


class Tcp(Protocol):
    name = 'tcp'
