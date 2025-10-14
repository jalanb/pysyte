# pysyte.bash

Python wrappers for bash commands and terminal control within the pysyte foundational library.

## Directory Purpose

The `pysyte.bash` module provides Python interfaces for:

- **shell.py**: Execute bash commands with proper PATH handling, directory management, and error reporting
- **screen.py**: Manage terminal alternate screens using tput commands for full-screen applications

## Module Architecture

### shell.py

Core bash command execution with state management:

- `run(command)` - Execute bash commands with guaranteed PATH (`/usr/local/bin`, `/usr/bin`, `/bin`)
- `cd(path)` - Change working directory for subsequent commands
- `pushd(path)` - Context manager for temporary directory changes
- `BashError` - Exception for command failures with full error output

Internal state tracking:
- `_working_dirs` - Directory stack for `cd`/`pushd` operations
- `_paths` - Cached PATH with essential directories guaranteed

### screen.py

Terminal alternate screen management using tput:

- `alt_screen()` - Setup alternate screen with automatic cleanup on exit
- `get_alt_screens()` - Return start/stop functions for manual control
- Uses `smcup`/`rmcup` tput commands for screen switching

## Integration with pysyte

This module is part of the pysyte foundational library that "adds batteries to Python, bash, and other languages near them". The bash module specifically bridges Python and bash execution, providing:

- Reliable command execution with proper error handling
- Directory state management across command calls
- Terminal control for full-screen applications
- Clean integration with Python's context management

## Testing

Comprehensive test suite in `test/`:
- Unit tests for shell command execution and directory management
- Mocked tests for screen functionality to avoid terminal manipulation
- Doctests demonstrating interactive usage patterns

Run tests from project root:
```bash
python -m pytest pysyte/bash/test/
```

## Dependencies

- `boltons.setutils.IndexedSet` - For PATH deduplication
- Standard library: `os`, `subprocess`, `contextlib`, `atexit`

## Development Notes

- Commands run with enhanced PATH to ensure essential binaries are available
- Directory changes are isolated to the bash execution context
- Screen management includes automatic cleanup to prevent terminal corruption
- Error handling preserves full command and output for debugging