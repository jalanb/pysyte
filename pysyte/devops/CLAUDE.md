# pysyte/devops

This directory contains DevOps utilities and tools for the pysyte project.

## Purpose

The `devops` module provides infrastructure and tooling support for pysyte development, focusing on dependency management and development workflow automation.

## Current Modules

### requirements.py

Core module for handling Python package requirements:

- **`Requirement`**: Dataclass representing a Python package with optional version constraints
- **`Requirements`**: Collection class for managing multiple requirements with list-like operations
- **`RequirementDir`**: Directory path handler that finds and processes requirements files (*.txt)
- **`parse()`**: Function for parsing requirement files (currently in development)

Key features:
- Extends pysyte's type system (`packages.Package`, `versions.version`)
- Integrates with pysyte's path handling (`dirs.DirPath`, `files.FilePath`)
- Supports version constraint parsing with regex pattern matching

## Development Status

This module appears to be under active development, with some functions containing `breakpoint()` statements for debugging. The `parse()` function is not yet implemented.

## Testing

Tests are located in `test/requirements.test` using doctest format. The tests validate:
- Module imports and documentation
- `RequirementDir` functionality with pysyte's requirements directory
- Integration with pysyte's number types (`numbers.otml`)

Run tests with:
```bash
python -m doctest test/requirements.test
```

## Directory Context

Part of the pysyte project structure:
- `/opt/clones/github/jalanb/pysyse/__dev__/` - Development clone of pysyte
- `pysyte/devops/` - This DevOps utilities directory
- Parent pysyte project provides foundational Python library functionality

## Integration

This module leverages several pysyte components:
- `pysyte.types.versions` - Version handling
- `pysyte.types.paths` - Path operations
- `pysyte.types.python.packages` - Package abstractions
- `pysyte.types.numbers` - Numeric type utilities

The devops module serves as infrastructure support for the broader pysyte ecosystem, handling development-time concerns like dependency management.