# pysyte.net

## Overview

Network utilities package within the pysyte foundational Python library. Provides simplified host management and network-related functionality.

## Module Contents

### hosts.py

Core module containing network host utilities:

- **Host dataclass**: Simple structure for representing hosts with hostname, aliases, addresses, and users
- **localhost**: Pre-initialized Host instance for the local machine, automatically loaded on import
- **_read_localhost()**: Internal function that uses `socket.gethostbyname_ex()` and `getpass.getuser()` to gather local host information

## Usage

```python
from pysyte.net import hosts

# Access pre-loaded localhost information
local = hosts.localhost
print(f"Hostname: {local.hostname}")
print(f"Addresses: {local.addresses}")
print(f"Aliases: {local.aliases}")
print(f"Users: {local.users}")
```

## Testing

Test coverage provided in `test/hosts.test` using doctest framework:
- Validates localhost information loading
- Tests cross-platform compatibility (handles CI environments like Travis)
- Ensures basic host properties are accessible

## Context within pysyte

- **Parent project**: pysyte - foundational Python library adding batteries to Python, bash, and other languages
- **Development branch**: `__dev__` - main development branch for incremental changes
- **Module location**: `pysyte/net/` - network utilities package
- **Python Requirements**: 3.13+ (as per project requirements)

## Architecture Notes

This module provides a simplified abstraction over Python's built-in `socket` module, focusing on localhost information retrieval. The design emphasizes simplicity and cross-platform compatibility rather than comprehensive network management.