# kat

A command-line tool for displaying selected lines from files, similar to `cat` but with line filtering capabilities.

## Purpose

The `kat` module provides a Python implementation of a file display utility that can show specific lines from files based on command-line arguments. It's part of the pysyte library's CLI utilities.

## Architecture

### Core Components

- `__main__.py`: Entry point module containing the main application logic
- `__main__.gwt`: Given-When-Then test specification for the module
- `__init__.py`: Package initialization (empty)

### Key Functions

- `parse_args()`: Command-line argument parsing using pysyte.cli.arguments
- `kat(app)`: Main functionality - processes files and displays filtered lines
- `main()`: Application entry point and orchestration

## Usage

Run as a Python module:

```bash
python3 -m pysyte.kat [options] [files]
```

The tool integrates with pysyte's CLI framework, using:
- `pysyte.cli.arguments` for argument parsing
- `pysyte.cli.lines` for line filtering options
- `pysyte.cli.app.App` for application lifecycle management

## Development Context

This module is part of the `__dev__` clone of pysyte, which serves as the main development branch for changes not requiring their own feature branch. It follows pysyte's architectural patterns for CLI tools.

## Testing

The module includes GWT (Given-When-Then) tests in `__main__.gwt` that verify:
- The module provides a proper `__main__` entry point
- The `main()` function is available for execution

## Integration

As part of the pysyte ecosystem, `kat` leverages the shared CLI infrastructure and follows the project's conventions for command-line utilities.