# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**pysyte** is a foundational Python library that "adds batteries to Python, bash, and other languages near them". This is the `__dev__` clone used for active development.

- **License**: MIT License
- **Python Requirements**: 3.13+
- **Version**: 0.8.79 (managed via bumpver)

## Development Commands

### Essential Development Workflow
```bash
# Code formatting and style
tox -e formats    # Auto-format with black and isort
tox -e lints      # Check code quality (black, isort, flake8, mypy)

# Testing
tox -e devs       # Fast development tests (--exitfirst, skip slow tests)
tox -e tests      # Full test suite with coverage
tox -e pudb       # Run tests with pudb debugger

# Version management
tox -e patch      # Bump patch version
tox -e minor      # Bump minor version
tox -e major      # Bump major version
```

### Single Test Execution
```bash
# Run specific test file
python -m pytest pysyte/path/to/module.test

# Run doctests in a specific module
python -m pytest --doctest-modules pysyte/path/to/module.py

# Run with pudb debugger
python -m pytest --pudb pysyte/path/to/test
```

## Code Architecture

### Package Structure
- **ai/**: AI and language model integration
- **bash/**: Shell utilities and screen management
- **cli/**: Command-line application framework
- **colours/**: ANSI escape codes and color handling
- **config/**: Configuration management utilities
- **devops/**: Development operations and deployment tools
- **types/**: Extended type system (paths, strings, lists, numbers, etc.)
- **unix/**: Unix-specific utilities and system integration

### Key Architectural Patterns

**Testing Strategy**: Uses a unique `.test` and `.tests` file approach:
- **465** `.test` files + **17** `.tests` files throughout the codebase
- `.test` files contain narrative doctests that tell a story
- `.tests` files contain comprehensive but verbose doctests
- Traditional `test_*.py` files for unit tests
- All discoverable via pytest with `--doctest-glob` patterns

**Type System Extension**: The `types/` package extends Python's type system:
- `paths.py`: Path manipulation (34KB, core module)
- `strings.py`: String utilities and extensions
- `lists/`: List processing and functional operations
- `numbers/`: Numeric type extensions
- `literals/`: Literal value handling

**Import System**: Custom import utilities in `importers.py` for dynamic module loading and dependency management.

### Multi-Clone Development Strategy

This is the `__dev__` clone in a multi-clone workflow:
- `__main__`: Stable branch for releases (version bumps after PR merges)
- `__dev__`: Active development (this clone)
- `__pypi__`: PyPI publishing branch
- `trees/`: Major refactor branch (paths → trees → paths)

**Integration Process**: `__dev__ → PR → __main__ → pull/rebase → other clones`

## Code Quality Standards

**Required before commits:**
- 100% black/isort compliance (`tox -e formats`)
- Pass all linting (`tox -e lints`)
- Target >90% test coverage
- Comprehensive doctests for public APIs

**Code Style:**
- Black formatting with single quotes (`-S` flag)
- 88 character line length
- isort with black profile
- Type hints with mypy strict optional checking
- No emojis in *.md files

### Pre-commit Hooks
- check-docstring-first, check-executables-have-shebangs
- check-merge-conflict, check-yaml, trailing-whitespace
- pylint integration

## Console Scripts

The package provides these entry points:
- `kat`: Enhanced `cat` command
- `keys`: Frontend for `pysyte.oss.getch`
- `imports`: Show unused and duplicate imports
- `short_dir`: Shortens directory paths for prompts

## Development Notes

- **Branch naming**: Simple descriptive names, no prefixes/suffixes, no "/" characters
- **Version consistency**: Maintained across clones via manual workflow discipline
- **Testing philosophy**: Write failing doctests first for API improvements
- **Dependencies**: Uses bidict, boltons, path.py==7.7.1, rich, textual, and others
- **Python compatibility**: Requires 3.13+ (as of current development)

When making changes, always run `tox -e devs` for fast feedback during development, then `tox -e lints` before committing to ensure code quality standards.