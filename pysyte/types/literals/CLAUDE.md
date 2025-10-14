# literals

Python literal constants package for the pysyte library

## Purpose

The `pysyte.types.literals` package provides named constants for commonly used literal values in Python programming. It centralizes access to standard characters, numbers, control codes, and formatting sequences, making code more readable and maintainable.

## Package Structure

### Core Modules

- **ansi.py** - ANSI terminal color escape sequences and formatting
- **control.py** - Control character constants (ctrl+a, ctrl+b, etc.)
- **digits.py** - String representations of digit characters ('0'-'9')
- **nones.py** - Falsy/empty values for different types (None, "", 0, 0.0)
- **numbers.py** - Integer constants with text-to-number conversion
- **punctuation.py** - Common punctuation and special characters

### Test Directory

The `test/` subdirectory contains doctest files (`.test` extension) following local convention:
- Comprehensive test coverage for all modules
- Assertion-based validation of constants and functionality
- Documentation of expected behavior and usage patterns

## Key Features

### ANSI Colors (`ansi.py`)
Provides terminal color constants derived from ANSI escape sequences:
- Light and dark color variants (red, green, blue, etc.)
- `highlighted(colour, text)` function for colored terminal output
- Based on standard ANSI color table

### Number Processing (`numbers.py`)
Advanced number-to-text conversion with:
- Named constants for digits (one, two, three, etc.)
- Complex `name(n)` function supporting numbers up to quindecillions
- Bidirectional mapping between text and numeric values
- Handles compound numbers, thousands, millions, billions, etc.

### Character Constants
Organized character access for:
- **digits**: Both boolean-style (false="0", true="1") and numeric constants
- **punctuation**: All standard ASCII punctuation with descriptive names
- **control**: Control character representations

### Empty Value Constants (`nones.py`)
Type-specific empty/falsy values:
- `none = None`
- `string = ""`
- `integer = 0`
- `real = 0.0`

## Development Context

Part of the pysyte foundational library that "adds batteries to Python, bash, and other languages near them". The literals package supports:
- Text processing and parsing applications
- Terminal-based applications with colored output
- Code readability through named constants instead of magic values
- Cross-platform character and formatting handling

## Integration

This package integrates with the broader pysyte ecosystem:
- Used throughout pysyte for consistent character and number handling
- Supports the library's goal of enhancing Python's built-in capabilities
- Follows pysyte patterns for type organization under `pysyte.types.*`

## Usage

```python
from pysyte.types.literals import ansi, numbers, punctuation

# Terminal colors
print(ansi.highlighted(ansi.red, "Error message"))

# Number conversion
assert numbers.name(42) == "forty two"
assert numbers.forty_two == 42

# Character constants
separator = punctuation.comma + punctuation.space
```