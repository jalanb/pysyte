# pysyte.unix.test

Test directory for the pysyte.unix module.

## Purpose

This directory contains doctests for the Unix filesystem utilities in `pysyte.unix`. The unix module provides abstractions for working with Unix filesystem concepts, particularly around the filesystem root and directory structures.

## Test Files

Following the project's established testing conventions:

- `root.test`: Doctests for the `pysyte.unix.root` module
  - Tests the Unix filesystem root functionality
  - Validates that the root directory object behaves correctly
  - Contains examples showing usage of the `root` module

## Module Context

The parent `pysyte.unix` module focuses on Unix-specific utilities:
- **root.py**: Provides `UnixDirectory` class and filesystem root access
- Implements Unix filesystem concepts like the single rooted tree structure
- Uses `pysyte.types.paths.DirectPath` as the base for Unix directory handling

## Testing Approach

Tests follow the project's established patterns:
- `.test` files contain doctests with "a story to tell"
- Tests validate both functionality and API examples
- Part of the broader pysyte testing strategy using pytest with doctest discovery

## Running Tests

From the project root, use the standard pysyte test commands:

```bash
tox -e devs    # Fast development tests
tox -e tests   # Full test suite with coverage
```

The pytest configuration automatically discovers and runs doctests in `.test` files throughout the project.