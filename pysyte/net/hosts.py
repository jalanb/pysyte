"""Simplified hosts for pysyte"""

@dataclass
class Host:
    hostname: str
    aliases: list
    addresses: list
    users: list

localhost = Host(*(
    list(socket.gethostbyname_ex(socket.gethostname())) +
    [getpass.getuser()]
))
