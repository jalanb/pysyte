# pysyte.bash.test

Test suite for the `pysyte.bash` module, which provides Python wrappers for bash commands and terminal control.

## Directory Purpose

This directory contains test files for the `pysyte.bash` module:

- **test_shell.py**: Unit tests for `shell.py` - tests bash command execution, directory changes, and error handling
- **test_screen.py**: Unit tests for `screen.py` - tests terminal alternate screen functionality using tput commands
- **shell.test**: Doctest file demonstrating interactive usage of shell commands

## Module Under Test

The `pysyte.bash` module provides:

- **shell.py**: Execute bash commands with `run()`, manage working directories with `cd()` and `pushd()`, handle errors with `BashError`
- **screen.py**: Manage terminal alternate screens using tput commands (`smcup`/`rmcup`)

## Testing Approach

### Unit Tests
- **Shell tests**: Verify directory navigation, command execution, and error handling
- **Screen tests**: Mock tput commands to test alternate screen start/stop functionality without actual terminal manipulation

### Doctests
- **shell.test**: Interactive examples showing real command execution and expected behavior

## Running Tests

From the project root (`/opt/clones/github/jalanb/pysyse/__dev__/`):

```bash
# Run all tests
python -m pytest pysyte/bash/test/

# Run specific test files
python -m pytest pysyte/bash/test/test_shell.py
python -m pytest pysyte/bash/test/test_screen.py

# Run doctests
python -m doctest pysyte/bash/test/shell.test
```

## Dependencies

Tests use:
- `unittest` - Standard testing framework
- `unittest.mock` - For mocking bash commands in screen tests
- `callee` - For flexible argument matching in mocks

## Notes

- Screen tests avoid actual terminal manipulation by mocking the `run` function
- Shell tests use real directory operations for realistic testing
- Error handling tests verify proper `BashError` exceptions are raised