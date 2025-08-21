# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**pysyte** is a foundational Python library that "adds batteries to Python, bash, and other languages near them". This is the `__dev__` clone, which is the primary development branch for active work.

- **License**: MIT License
- **Python Requirements**: 3.13+
- **Version**: 0.8.79 (see fred.toml)

## Development Commands

All development is managed through tox commands defined in `fred.toml`:

```bash
# Code formatting and style
tox -e formats    # Reformat code with black (-S for single quotes) and isort
tox -e lints      # Run all linters: black, blackdoc, isort, flake8, mypy

# Testing
tox -e devs       # Fast development tests (--exitfirst, skip slow tests)
tox -e tests      # Full test suite with coverage reporting
tox -e pudb       # Run tests with pudb debugger

# Version management
tox -e patch      # Bump patch version using bumpver
tox -e minor      # Bump minor version
tox -e major      # Bump major version
```

## Testing Architecture

The project uses a unique testing approach with multiple file patterns:
- `**/*.py`: Doctests in docstrings for usage examples
- `**/*.test`: Doctest files with narrative/story structure  
- `**/*.tests`: Longer doctest files for comprehensive testing
- `test_*.py`: Traditional pytest unit tests

All tests run through pytest with doctest integration. Current count: 554 `.test`/.tests` files across the project.

## Code Quality Standards

- **Formatting**: Black with single quotes (`-S` flag), 88 character line length
- **Import sorting**: isort with black profile
- **Linting**: flake8 with bugbear, comprehensions, eradicate plugins
- **Type checking**: mypy with strict optional checking
- **Coverage**: Branch coverage with parallel execution support

## Project Architecture

### Core Module Structure
- **ai/**: AI and language model integration (may be deprecated)
- **bash/**: Shell utilities and screen management
- **cli/**: Command-line application framework  
- **colours/**: ANSI escape codes and color handling
- **config/**: Configuration management with XDG support
- **devops/**: Development operations utilities
- **types/**: Extended type system (paths, strings, lists, etc.)
  - **types/paths.py**: Core path handling (being refactored to trees/)
  - **types/trees/**: New path system under development
- **unix/**: Unix-specific utilities

### Entry Points (Console Scripts)
- `kat`: Enhanced `cat` command
- `keys`: Frontend for `pysyte.oss.getch`
- `imports`: Import analysis and management
- `short_dir`: Directory path shortening for prompts

## Development Context

### Multi-Clone Strategy
This is part of a coordinated multi-clone development approach:
- **`__dev__`**: Active development (this clone)
- **`__main__`**: Stable main branch with version bumps after PR merges
- **`__pypi__`**: PyPI publishing branch
- **`trees/`**: Major refactor branch (paths → trees → paths)

### Version Strategy
- Pattern: `vX.Y.{PR_NUMBER}` 
- Patch bumps happen in `__main__` after each PR merge
- Major/minor bumps handled manually in `__pypi__` clone

### Current Development Focus
- **Primary blocker**: Complete `trees/` refactor for v0.9 release
- **Target**: Stabilize trees integration and path system migration
- **Next major**: v1.0 with DevOps code integration and comprehensive doctest coverage

## Testing Notes

- Coverage targeting >90% with branch coverage
- Parallel test execution supported
- Fast feedback loop with `tox -e devs` for development
- Comprehensive CI/CD testing with `tox -e tests`
- Doctest-driven API development recommended

## Dependencies

Core runtime dependencies include bidict, boltons, deprecated, inflect, path.py==7.7.1, pym, pyyaml, rich, stackprinter, textual, yamlreader.

## Integration Workflow

Development follows the pattern:
```
__dev__ → PR → __main__ → pull/rebase → other clones
```

All development happens in `__dev__` or feature branches, merges to `__main__` via PRs, and other clones sync from `__main__`.