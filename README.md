# pysyte

**pysyte** - A foundational Python library that "adds batteries to Python, bash, and other languages near them"

> **Note**: This directory also contains `README.rst` for PyPI/setuptools compatibility. This `README.md` focuses on development workflow and practices.

## Development Workflow

### Quick Start Commands

```bash
# Development workflow using tox
tox -e formats    # Reformat code with black and isort
tox -e lints      # Lint code with black, isort, flake8, mypy
tox -e devs       # Run developer tests, stopping on first failure
tox -e tests      # Run full test suite with coverage
```

### Version Management

```bash
tox -e patch      # Bump patch version
tox -e minor      # Bump minor version  
tox -e major      # Bump major version
```

All tox commands are defined in `[tool.tox]` sections of pyproject.toml - check there for current options and exact command syntax.

## Code Quality Standards

**Established practices for all development:**

- **Formatting**: Maintain 100% black/isort compliance (`tox -e formats`)
- **Linting**: Pass all checks (`tox -e lints`: black, blackdoc, isort, flake8, mypy)
- **Testing**: Target >90% test coverage, comprehensive doctests for public APIs
- **Type Hints**: Minimize mypy ignore statements, use proper type annotations
- **Documentation**: Standardized docstring formats, examples in doctests

### Testing Strategy

- **`tox -e devs`**: Fast feedback during development (`--exitfirst`, skip slow tests)
- **`tox -e tests`**: Comprehensive coverage for CI/CD (full test suite)
- **Doctests**: Embedded in `.test` and `.tests` files throughout codebase
- **Coverage**: Branch coverage tracking with parallel execution support


## Testing Files

- We use pytest with doctests enabled
- Test patterns: `**/*.py`,`**/*.test`, `**/*.tests`, `test_*.py`
 - `**/*.py`: doctests in docstrings of that show examples of use
 - `**/*.test`: doctests with a story to tell
 - `**/*.tests`: doctests that got long and boring
 - `test_*.py`: traditional unit tests

## Code Quality

- **Formatting**: Black with single quotes (`-S`)
- **Import sorting**: isort with black profile
- **Linting**: flake8 with bugbear, comprehensions, eradicate
- **Type checking**: mypy with strict optional checking
- **Line length**: 88 characters

## Development Notes

This clone is part of a multi-clone development strategy:
- `__main__`: Main branch for stable releases
 - Version bumps happen in `__main__` after PR merges 
 - following the pattern `vX.Y.{PR_NUMBER}`.
- `__dev__`: Active development
- `__pypi__`: PyPI publishing branch
 - Major and minor bumps are done by hand here
 - and uploaded to pypi
- `trees/`: Current major refactor branch (paths → trees → paths)
 - blocking `v0.9` release
- Other feature branches as needed

## Project Structure

### Entry Points (Console Scripts)
- `kat`: File and directory catalog management
- `keys`: Keyboard and key handling utilities
- `imports`: Python import analysis and management
- `short_dir`: Directory path abbreviation

### Core Modules
- **ai/**: AI and language model integration
- **bash/**: Shell and screen utilities
- **cli/**: Command-line application framework
- **colours/**: ANSI escape codes and color handling
- **config/**: Configuration management
- **types/**: Extended type system (paths, strings, lists, etc.)
- **unix/**: Unix-specific utilities

## Development Context

For comprehensive project context, workflow details, and AI-specific information, see:
- `CLAUDE.md` - Project context and established workflows
- `PLAN.md` - Strategic planning and development roadmap
- `pyproject.toml` - Tool configurations and version info

### Clone Integration Process
```
__dev__ → PR → __main__ → pull/rebase → other clones
```

**Established Practice:**
- All development happens in `__dev__` clone or feature branches
- Changes merge to `__main__` via pull requests
- Merge to `__main__` triggers version bump
- Other clones pull and rebase from `__main__`
- `__pypi__` clone handles publishing to PyPI
