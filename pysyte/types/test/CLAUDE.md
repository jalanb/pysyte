# pysyte/types/test

Test directory for the `pysyte.types` package - the foundational type system extensions in pysyte.

## Testing Structure

This directory follows the local Python testing convention with three types of test files:

### Doctest Files
- `*.test` - Primary doctests for each module (dictionaries, lines, lists, numbers, paths, proxies, times)
- `*.tests` - Extended doctests for edge cases and longer examples (when `.test` files get "too long and boring")

### Unit Tests
- `test_*.py` - PyTest unit tests providing comprehensive test coverage
- Focus on edge cases, error conditions, and integration scenarios not covered by doctests

## Key Modules Tested

- **paths** - Extended path classes and utilities (largest test suite with `paths.test` and `test_paths.py`)
- **dictionaries** - Dictionary handling utilities and extensions
- **lines** - Text line processing utilities
- **lists** - List manipulation and extension utilities
- **numbers** - Numeric type extensions
- **proxies** - Proxy object implementations
- **times** - Time/datetime utilities
- **literals** - Python literal type extensions

## Testing Coverage

The dual testing approach (doctests + unit tests) ensures:
- Documentation stays current via executable examples in `.test` files
- Edge cases and error conditions are thoroughly tested in `test_*.py` files
- Real-world usage patterns are validated through integrated test scenarios

## Running Tests

From the project root (`/opt/clones/github/jalanb/pysyse/__dev__/`):
- Doctests: Run via module imports and doctest execution
- Unit tests: Run with pytest or unittest discovery

This test directory validates the core type extensions that many other pysyte modules depend on.