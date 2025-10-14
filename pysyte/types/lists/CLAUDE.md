# pysyte.types.lists

## Module Overview

This module provides specialized list operations and search algorithms, particularly focusing on binary search implementations with customizable comparison and averaging strategies.

## Key Components

### Search Algorithms

- **`directed_search()`**: Generic directed search function that accepts a customizable averaging picker
- **`binary_search()`**: Standard binary search implementation using integer average picker
- **Comparison functions**: `upper_choice()`, `lower_choice()`, `binary_choice()`, `binary_chooser()`

### Context Managers

- **`Chooser`**: Context manager for comparison functions
- **`Picker`**: Context manager for averaging/picking functions with call support

### Utility Functions

- **`average()`**: Integer floor division averaging for binary search
- **`fax()`**: `max(0, x)` lambda for positive constraint
- **`fix()`**: `min(0, x)` lambda for negative constraint
- **`applied()`**: Function application helper

## Architecture

The module uses a functional approach with dataclass-based context managers. The `directed_search()` function is generic and accepts different averaging strategies via the `Picker` interface, allowing for customizable search behaviors.

## Testing

The module includes doctests demonstrating:
- Basic binary search usage
- Edge case handling (element not found)
- Random data validation
- Function composition examples

Run doctests with:
```bash
python search.py
```

## Part of pysyte.types

This module is part of the broader `pysyte.types` package, providing specialized list operations that complement other type utilities in the pysyte library.