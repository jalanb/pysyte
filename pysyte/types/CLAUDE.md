# pysyte.types

Core type extensions and utilities package for the pysyte library.

## Package Overview

The `pysyte.types` package provides foundational type system extensions that "add batteries" to Python's built-in types. This package contains enhanced classes, utilities, and algorithms for common data types, serving as the foundation for many other pysyte modules.

## Core Modules

### Path Handling
- **`paths.py`** - Extended path classes and utilities built on top of `path.Path`, including custom exceptions and path assertions (34KB, the largest module)

### Collections & Data Structures
- **`dictionaries.py`** - Dictionary manipulation utilities including case-insensitive lookup and dictionary swapping
- **`lists.py`** - List operations and search algorithms, particularly binary search implementations
- **`lines.py`** - Text line processing utilities

### Type Conversion & Validation
- **`methods.py`** - Method handling and introspection utilities
- **`proxies.py`** - Proxy object implementations

### Basic Types
- **`colours.py`** - Color handling utilities (lightweight)
- **`nothing.py`** - Utilities for handling null/empty values
- **`times.py`** - Time and datetime utilities

## Sub-packages

### `numbers/`
Number handling utilities with flexible and strict conversion approaches:
- Flexible conversion functions (`inty`, `floaty`) that fall back to `len()`
- Strict conversion functions (`as_int`, `as_float`) that raise exceptions
- Alternative number systems like "1, 2, many, lots" (OTML)

### `lists/`
Specialized list operations and search algorithms:
- Generic directed search with customizable averaging strategies
- Binary search implementations
- Context managers for comparison and averaging functions

### `literals/`
Python literal constants providing named access to commonly used values:
- ANSI terminal color sequences
- Control characters and punctuation
- Number-to-text conversion (up to quindecillions)
- Type-specific empty values

## Architecture

The package follows pysyte's batteries-included philosophy:
- **Practical utilities**: Real-world data type manipulation needs
- **Type extensions**: Enhanced versions of built-in Python types
- **Dual approaches**: Often provides both flexible and strict variants
- **Consistent patterns**: Similar interfaces across modules

## Testing Structure

Follows local testing conventions:
- **`test/`** directory with comprehensive coverage
- **`.test` files** - Primary doctests for each module
- **`.tests` files** - Extended doctests for edge cases
- **`test_*.py` files** - PyTest unit tests for complex scenarios

## Integration Context

Part of the `__dev__` clone of pysyte (main development branch). This package:
- Serves as foundation for other pysyte modules
- Provides core type system that many utilities depend on
- Currently being refactored as part of the "trees" branch initiative (paths → trees → paths)

## Development

The types package is central to pysyte's core functionality. Changes here impact many dependent modules, so testing is critical before any modifications.
