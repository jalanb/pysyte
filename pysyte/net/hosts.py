"""Simplified hosts for pysyte"""

import getpass
import socket
from dataclasses import dataclass
from typing import List


@dataclass
class Host:
    hostname: str
    aliases: List[str]
    addresses: List[str]
    users: List[str]


def _read_localhost() -> Host:
    """Read host values for localhost"""
    host, aliases, addresses = socket.gethostbyname_ex(socket.gethostname())
    user = getpass.getuser()
    return Host(host, aliases, addresses, [user])

localhost = _read_localhost()
