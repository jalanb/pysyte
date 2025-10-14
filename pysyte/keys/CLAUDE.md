# pysyte.keys

## Purpose

The `keys` package provides keyboard input utilities for capturing key presses in command-line applications.

## Architecture

This package is a thin wrapper around the `pysyte.oss.getch` module, providing a command-line interface for keyboard input operations.

### Core Components

- `__main__.py`: CLI script for interactive key capture
- `__init__.py`: Package initialization (empty)

## Usage

### Command Line Interface

The package can be run as a script to capture keyboard input:

```bash
python -m pysyte.keys [options]
```

#### Options

- `--codes`: Show raw key codes instead of interpreted keys
- `--prompt`: Display a custom prompt before capturing input
- `--string`: Show captured input as a string

#### Examples

```bash
# Capture a single key press
python -m pysyte.keys

# Show raw key codes
python -m pysyte.keys --codes

# Capture with custom prompt
python -m pysyte.keys --prompt "Press any key: "

# Capture as string
python -m pysyte.keys --string
```

## Dependencies

- `pysyte.cli.main`: Provides CLI framework (`run` function)
- `pysyte.oss.getch`: Core keyboard input functionality
  - `get_codes()`: Returns raw key codes
  - `get_string()`: Returns string representation
  - `get_key()`: Returns interpreted key

## Integration

This package integrates with the broader pysyte ecosystem:

- Uses the standard pysyte CLI framework for argument parsing
- Leverages OS-specific keyboard input handling from `pysyte.oss`
- Follows pysyte conventions for command-line tools

## Version

Current version: 0.1.1