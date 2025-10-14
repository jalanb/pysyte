# pysyte CLI Module

## Purpose

The `pysyte.cli` module provides enhanced command-line interface utilities that simplify argument parsing and CLI program creation. It acts as a sophisticated wrapper around Python's standard `argparse` library, offering convenience methods and patterns for building robust CLI applications.

## Architecture

This module (`/opt/clones/github/jalanb/pysyse/__dev__/pysyte/cli/`) contains the core CLI infrastructure:

### Core Components

- **`main.py`**: The program runner that converts regular functions into CLI programs with proper exit handling
- **`arguments.py`**: Enhanced argument parser with convenience methods (`arg()`, `true()`, `int()`, `strings()`)
- **`app.py`**: Application lifecycle management with context handling and exit code management
- **`config.py`**: Configuration file loading from standard locations (XDG dirs, ~/.config, /etc)
- **`lines.py`**: Specialized parser for line-oriented CLI operations (line numbers, ranges, sed expressions)
- **`paths.py`**: CLI-specific path handling utilities
- **`streams.py`**: Stream handling for CLI input/output operations
- **`exits.py`**: Exit code management and standardization
- **`exceptions.py`**: Rich exception handling for CLI contexts

## Key Features

### Enhanced Argument Parsing
```python
parser = arguments.parser("My CLI tool")
parser.arg("f", "file", help="Input file")
parser.true("v", "verbose", help="Verbose output")
parser.int("n", "number", help="Number of items")
parser.strings("items", help="List of items")
```

### Program Runner
The `main.run()` function converts any callable into a CLI program:
- Automatic argument parsing integration
- Configuration file loading
- Proper exit code handling
- Exception management

### Line-Oriented Operations
Specialized support for tools that work with text lines:
- Line number options (`--at`, `--first`, `--last`)
- Line range handling
- sed-style expressions (`--substitute`, `--expression`)
- Width and number formatting

### Configuration Management
Automatic loading from standard config locations:
- `/etc/`
- XDG config directories
- `~/.config/`
- Project-specific locations

## Development Context

This CLI module is part of the `__dev__` clone of pysyte, serving as the main development branch for CLI-related enhancements. It provides the foundation for many pysyte utilities that need command-line interfaces.

The module follows pysyte's philosophy of "adding batteries" to Python by making common CLI patterns simpler and more consistent.

## Testing

Comprehensive test suite in `test/` directory includes:
- Unit tests for all major components
- Doctests with usage examples
- Integration tests for the full CLI pipeline

## Usage Patterns

### Basic CLI Program
```python
def main(args):
    print(f"Processing {args.file}")

def add_args(parser):
    parser.arg("f", "file", help="File to process")
    return parser

if __name__ == "__main__":
    main.run(main, add_args)
```

### Line-Oriented Tool
```python
from pysyte.cli.lines import add_args

def process_lines(args):
    # Use args.at, args.first, args.last, etc.
    pass

if __name__ == "__main__":
    main.run(process_lines, add_args)
```

This module is essential infrastructure for building consistent, user-friendly command-line tools within the pysyte ecosystem.