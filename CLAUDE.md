# pysyte 

`pysyte` provides "more batteries" for Python.

`pysyte` is available from [pypi](pypi.org), and is an open source project, written in Python

## Affordances

The `pysyte` project offers several key capabilities:

  1. Enhanced path handling and filesystem operations
  2. CLI application framework with argument parsing
  3. Extended type utilities (dictionaries, lists, strings)
  4. System interaction tools for cross-platform OS operations
  5. AI integration with various providers
  6. Terminal text styling with ANSI colors
  7. Import utilities for dynamic module loading
  8. Command-line tools like 'kat' and 'rePATH'

### Examples

```doctest
>>> from pysyte.trees.paths import path
>>> here = path(__file__)
>>> assert 'pysyte' in here.parents
>>> there = path(path)
>>> assert 'trees' in there.parents

>>> from pysyte.colours import colour_names as names
>>> assert "light cyan" in names.cga()
```

## Build & Test Commands

Run all tests
```shell
$ tox -e tests
```

Run all linters
```shell
$ tox -e lints
```

## Code Style Guidelines
- Black formatting (`-S` flag to skip string normalization)
- Line length: 88 characters
- All code should have tests (unit tests or doctests)
- Docstrings should include doctests, as examples
- Type hints recommended 
- Follow PEP 8 guidelines
- Single line imports (isort with force_single_line)
- Custom exceptions should be defined as needed
- Tests in `test/` subdirectories with naming conventions:
  - Unit tests: `test_*.py` files
  - Doctests: `*.test` or `*.tests` files
- Exceptions should be handled explicitly with appropriate error reporting

# See also

- `.clawed/CLAUDE.md`
