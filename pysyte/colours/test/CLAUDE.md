# pysyte.colours.test

This directory contains the test suite for the `pysyte.colours` module, following pysyte's hybrid testing architecture.

## Test Structure

The test directory uses pysyte's three-tier testing approach:

### Doctest Files (`.test`)
Narrative-driven tests that serve as both documentation and validation:
- **`ansi_escapes.test`**: Tests ANSI escape sequence generation and text coloring
- **`colour_names.test`**: Tests color name definitions and groupings
- **`colour_numbers.test`**: Tests color format conversions (HTML hex, ANSI codes, RGB)
- **`texts.test`**: Tests high-level text coloring API and `ColouredTail` fluent interface
- **`x11_colour_names.test`**: Tests X11 color name parsing from system files

### Extended Doctests (`.tests`)
More comprehensive doctest files for edge cases:
- **`colour_numbers.tests`**: Extended testing of color conversion edge cases and boundary conditions

### Pytest Unit Tests (`test_*.py`)
Traditional unit tests for comprehensive coverage:
- **`test_ansi_escapes.py`**: Unit tests for ANSI escape functions, emphasis, foreground/background colors

## Running Tests

From the project root (`/opt/clones/github/jalanb/pysyse/__dev__/`):

```bash
# Run all colours tests
py.test pysyte/colours/test/

# Run specific test file
py.test pysyte/colours/test/test_ansi_escapes.py

# Run with tox (includes doctests)
tox -e devs    # Fast development tests
tox -e tests   # Full test suite with coverage
```

## Test Coverage Areas

### ANSI Escape Sequences
- Basic color codes (foreground/background)
- Text emphasis (bold, italic)
- 256-color support
- Bash prompt escape sequences

### Color Conversions
- HTML hex to ANSI code mapping
- RGB to ANSI conversions
- CGA color set validation
- Edge cases and boundary conditions

### High-Level Text API
- `ColouredTail` fluent interface chaining
- Color name method generation
- Text concatenation and formatting
- Integration with terminal output

### X11 Color Integration
- System `rgb.txt` file parsing
- Fallback to basic 8 colors
- Color name resolution

## Integration Context

These tests validate the colours module's integration with:
- Terminal output systems
- Command-line applications using pysyte.cli
- Bash prompt generation
- Screen management functionality

## Development Notes

- Doctest files use narrative structure to demonstrate API usage
- Unit tests focus on edge cases and error conditions
- Color output is tested via ANSI escape sequence validation
- Tests account for different terminal capabilities and system configurations