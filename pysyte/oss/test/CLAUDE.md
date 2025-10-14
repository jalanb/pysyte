# pysyte.oss.test

## Directory Overview

This directory contains doctests for the `pysyte.oss` package, which provides Operating System Specific functionality within the pysyte library.

## Test Files

### linux.test
- Tests the `pysyte.oss.linux` module
- Focuses on Linux-specific functionality, particularly XDG configuration paths
- Tests XDG home directory resolution and environment variable handling
- Tests configuration file path construction

### platforms.test
- Tests the `pysyte.oss.platforms` module
- Tests cross-platform functionality for different OS platforms
- Includes clipboard operations (darwin-specific tests)
- Contains platform-specific conditional testing

## Testing Framework

These are doctest files (`.test` extension) that can be run as part of the pysyte test suite. They follow the doctest format with:
- Module imports and setup
- Executable Python code with `>>>` prompts
- Assertions to verify expected behavior
- Platform-specific conditional logic where needed

## Module Context

The `pysyte.oss` package provides OS-specific utilities that abstract platform differences, allowing the rest of pysyte to work consistently across different operating systems. This test directory ensures that cross-platform functionality works correctly on the supported platforms.