# pysyte config module

## Overview

The config module provides configuration management functionality for the pysyte library. It handles loading, parsing, and managing configuration data from various sources including YAML files and XDG-compliant directories.

## Module Components

### types.py
Core configuration classes and data structures:
- `Configuration` - Base configuration class extending NameSpaces
- `PysyteConfiguration` - Base class for pysyte-specific configuration handling
- `YamlConfiguration` - YAML-based configuration loader with `.yml` and `.yaml` support
- `ModuleConfiguration` - Module-based configuration handling
- `ConfigPaths` - Multi-path configuration discovery and loading
- `ConfigPathsData` - Data container for configuration paths

### urator.py
Configuration file I/O operations:
- `Config` - Configuration wrapper around NameSpaces
- `load()` - Load YAML configuration from file paths
- `dump()` - Save configuration data to YAML files with explicit start markers

### xdg.py
XDG Base Directory specification compliance:
- `user` - User-specific configuration directories (`~/.config`)
- `machine` - System-wide configuration directories
- Integration with `pysyte.oss.linux` for XDG directory discovery

## Architecture

The config module follows a layered approach:

1. **Base Layer**: `Configuration` class extends `NameSpaces` for attribute-style access
2. **Format Layer**: `YamlConfiguration` handles YAML parsing and file extension detection
3. **Discovery Layer**: `ConfigPaths` manages multiple configuration sources and loading priority
4. **Standards Layer**: XDG specification support for cross-platform configuration management

## Usage Patterns

- Configuration files use `.yml` or `.yaml` extensions
- Multiple configuration paths supported with merge capabilities
- XDG-compliant directory structure for user and system configs
- Attribute-style access to configuration values via NameSpaces inheritance

## Testing

Tests are located in `test/` directory using doctest format:
- `types.test` - Configuration classes and path handling
- `urator.test` - File I/O operations and YAML processing
- `xdg.test` - XDG directory specification compliance

## Integration

This module integrates with:
- `pysyte.types.paths` - Path handling and file operations
- `pysyte.types.dictionaries.NameSpaces` - Attribute-style data access
- `pysyte.oss.linux` - XDG directory discovery
- External `yaml` library for YAML processing

## Location Context

- Project root: `/opt/clones/github/jalanb/pysyse/__dev__/`
- Module path: `pysyte/config/` (this directory)
- Part of the foundational pysyte Python library adding batteries to Python, bash, and other languages