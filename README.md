# pysyte trees/ clone

pysyte adds batteries to

* python
* bash
* other languages near them

## Development Workflow

This clone contains a major refactor of `pysyte.types.paths` as `pysyte.types.trees`.

### Development Commands

We have a venv set up in project root:
```bash
source .venv/bin/activate
```

Development commands (run from project root):
```bash
tox -e formats    # Reformat code with black and isort
tox -e lints      # Lint code with black, isort, flake8, mypy
tox -e devs       # Run developer tests, stopping on first failure
tox -e tests      # Run full test suite with coverage
```

### Project Requirements

- **Python**: 3.13+
- **Testing**: pytest with doctests (`**/*.test`, `**/*.tests`)
- **Code Quality**: Black formatting, mypy type checking, 88-char line length

## Code Quality Standards

**Established practices for all development:**
- Maintain 100% black/isort compliance (`tox -e formats`)
- Pass all linting checks (`tox -e lints`: black, blackdoc, isort, flake8, mypy)
- Target >90% test coverage
- Minimize mypy ignore statements
- Use standardized docstring formats
- All public APIs should have comprehensive doctests

## Badges

[![PyPi Package](https://badge.fury.io/py/pysyte.svg)](https://pypi.python.org/pypi/pysyte) [![Black Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Test Coverage](https://codecov.io/gh/jalanb/pysyte/branch/__main__/graph/badge.svg)](https://codecov.io/gh/jalanb/pysyte)
