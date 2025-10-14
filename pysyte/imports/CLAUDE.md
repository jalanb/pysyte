# pysyte.imports

Python module for analyzing import statements in Python source files.

## Purpose

This module provides a command-line tool to analyze Python files for import-related issues:
- **Unused imports**: Import statements that are never referenced in the code
- **Multiple imports**: The same module imported more than once

## Files

- `__init__.py`: Empty module initializer
- `__main__.py`: Main CLI implementation for import analysis

## Usage

The module can be run as a script:

```bash
python -m pysyte.imports [options] <source_files_or_directories>
```

### Options

- `--edit`: Show vim command for editing files with issues
- `--multiple`: Show multiple imports
- `--unused`: Show unused imports
- `source`: Path(s) to Python files or directories to analyze

## Features

- Recursively scans directories for `.py` files
- Ignores common build/cache directories (`__pycache__`, `.tox`, `.git`, `.venv`)
- Shows line numbers and content for problematic imports
- Generates vim commands for quick navigation to issues
- Uses `pysyte.importers` for AST-based analysis

## Integration

Part of the larger pysyte library's code analysis toolkit. Depends on:
- `pysyte.importers`: Core import analysis functionality
- `pysyte.cli.main`: CLI framework
- `pysyte.types.paths`: Path handling utilities

## Development

This is a focused utility module within the pysyte ecosystem for maintaining clean import statements in Python codebases.