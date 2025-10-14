# pysyte.types.numbers

This package provides number handling utilities for the pysyte library.

## Purpose

The numbers package offers two main approaches to number conversion and handling:

1. **Flexible conversion functions** (`inty`, `floaty`, `as_int`, `as_float`) that can handle various input types
2. **Alternative number systems** like the "1, 2, many, lots" (OTML) system

## Modules

### `__init__.py`
Core number conversion utilities:

- `inty()` - Flexible integer conversion that falls back to `len()` for sequences
- `as_int()` - Strict integer conversion that raises `NAN` exception on failure
- `floaty()` - Flexible float conversion with length fallback
- `as_float()` - Strict float conversion
- `NAN` - Custom exception class for non-numeric values

**Key difference**: `inty("hello")` returns `5` (length), while `as_int("hello")` raises `NAN`.

### `lots.py`
Implementation of the "1, 2, many, lots" number system:

- `OTML` class - Represents numbers in categories: one, two, many (3-9), lots (10+)
- `otml()` - Factory function to create OTML instances
- Boolean properties: `is_one`, `is_two`, `is_many`, `is_lots`

## Usage Examples

```python
from pysyte.types import numbers

# Flexible conversion
assert numbers.inty(5) == 5
assert numbers.inty("hello") == 5  # length
assert numbers.inty([1, 2, 3]) == 3  # length

# Strict conversion
assert numbers.as_int("5") == 5
# numbers.as_int("hello")  # raises NAN

# OTML system
many = numbers.otml(7)
assert many.is_many
assert not many.is_lots
```

## Architecture

The package follows pysyte's philosophy of providing practical, batteries-included utilities. The dual approach (flexible vs strict conversion) gives developers choice based on their specific needs.

## Testing

Use standard pysyte testing conventions:
- Doctests embedded in modules
- Additional pytest tests in `test/` directory if present
- Run doctests: `python -m doctest numbers/__init__.py numbers/lots.py`