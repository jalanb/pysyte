"""Simplified hosts for pysyte"""

from dataclasses import dataclass
import getpass
import socket
from typing import List


@dataclass
class Host:
    hostname: str
    aliases: list[str]
    addresses: list[str]
    users: list[str]


def _read_localhost() -> Host:
    """Read host values for localhost"""
    host, aliases, addresses = socket.gethostbyname_ex(socket.gethostname())
    user = getpass.getuser()
    return Host(host, aliases, addresses, [user])


localhost = _read_localhost()
