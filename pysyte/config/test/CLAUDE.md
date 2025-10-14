# pysyte config test directory

## Overview

This directory contains test files for the pysyte configuration module. The tests are written in doctest format and validate the functionality of various configuration components.

## Test Files

### types.test
Tests for `pysyte.config.types` module which provides configuration classes:
- `YamlConfiguration` - YAML-based configuration handling
- `ModuleConfiguration` - Module-based configuration handling

### urator.test
Tests for `pysyte.config.urator` module which handles config file operations:
- Loading configuration from YAML files (`.yamly` extension)
- Dumping configuration data to files
- File I/O operations for configuration management

### xdg.test
Tests for `pysyte.config.xdg` module which implements XDG Base Directory specification:
- User configuration directory detection (`~/.config`)
- XDG-compliant configuration file location handling

## Testing Approach

All tests use Python's doctest format, allowing them to serve as both documentation and executable tests. The tests validate:

- Module imports and basic functionality
- Configuration file loading and saving
- XDG directory specification compliance
- Edge cases and error conditions

## Location Context

This test directory is part of the larger pysyte project structure:
- Project root: `/opt/clones/github/jalanb/pysyse/__dev__/`
- Config module: `pysyte/config/`
- Test directory: `pysyte/config/test/` (this directory)

The tests here validate the configuration management capabilities that support the broader pysyte library's functionality.