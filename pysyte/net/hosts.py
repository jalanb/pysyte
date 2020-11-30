"""Simplified hosts for pysyte"""

import getpass
import socket
from dataclasses import dataclass


@dataclass
class Host:
    hostname: str
    aliases: list
    addresses: list
    users: list


localhost = Host(
    *(
        list(socket.gethostbyname_ex(socket.gethostname()))
        + [getpass.getuser()]
    )
)
