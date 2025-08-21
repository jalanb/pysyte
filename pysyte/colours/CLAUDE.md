# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Module Overview

The `pysyte.colours` module provides ANSI terminal color and text formatting functionality for Python applications. It is part of the larger pysyte project, a foundational Python library.

## Architecture

The module is organized into several focused components:

### Core Components

- **`ansi_escapes.py`**: Low-level ANSI escape sequence generation for terminal formatting (bold, colors, prompts)
- **`colour_names.py`**: Color name definitions and groupings (basic, RGB, CYM, CGA color sets)
- **`colour_numbers.py`**: Color format conversions between HTML hex, ANSI codes, and RGB values
- **`texts.py`**: High-level text coloring API with fluent interface via `ColouredTail` class
- **`x11_colour_names.py`**: X11 color name parsing from system `rgb.txt` files

### Key Design Patterns

- **Fluent Interface**: `ColouredTail` class allows chaining color operations: `text("hello").red().bold()`
- **Multiple Color Formats**: Supports 16-color, 256-color, HTML hex, and RGB representations
- **Dynamic Attribute Generation**: Color names from CGA set automatically become methods on `ColouredTail`
- **Fallback Strategy**: X11 color names fall back to basic 8 colors if system files unavailable

## Development Commands

All commands should be run from the project root (`/opt/clones/github/jalanb/pysyse/__dev__/`):

```bash
# Code formatting
tox -e formats    # Apply black (-S for single quotes) and isort formatting

# Linting and type checking  
tox -e lints      # Run black, blackdoc, isort, flake8, mypy

# Testing
tox -e devs       # Fast development tests (--exitfirst, skip slow tests)
tox -e tests      # Full test suite with coverage
tox -e pudb       # Run tests with pudb debugger

# Run single test file
py.test pysyte/colours/test/test_ansi_escapes.py
```

## Testing Architecture

The module uses pysyte's hybrid testing approach:

- **`.test` files**: Doctest files with narrative structure for API documentation
- **`test_*.py` files**: Traditional pytest unit tests for edge cases and comprehensive coverage
- **Inline doctests**: Usage examples in module docstrings

## Key APIs

### Text Coloring
```python
from pysyte.colours import texts
# Basic usage
red_text = texts.red("error message")
# Fluent chaining  
colored = texts.colour("green", "success").colour("bold", "!")
```

### ANSI Escapes
```python
from pysyte.colours import ansi_escapes
# Direct escape sequences
bold_on = ansi_escapes.bold()
color_off = ansi_escapes.no_colour()
```

### Color Conversions
```python
from pysyte.colours import colour_numbers
# Convert between formats
ansi_code = colour_numbers.html_to_ansi("#FF0000")  # red
html_color = colour_numbers.ansi_to_html(9)         # light red
```

## Integration Context

This colours module integrates with:
- **`pysyte.bash.screen`**: Terminal screen management
- **`pysyte.cli`**: Command-line application styling
- **`pysyte.types.strings`**: Extended string type system

## Development Notes

- Color constants follow CGA ordering (red, green, yellow, blue, magenta, cyan)
- 256-color support uses standard xterm color cube mapping
- Prompt functions add bash escape sequences for readline compatibility
- X11 integration reads system `rgb.txt` files for extended color names