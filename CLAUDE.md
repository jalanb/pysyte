# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Always use `.venv/bin/tox`, not bare `tox`. If `.venv/bin/tox` is missing, the dev environment needs setting up — run `python -m pip install '.[dev]'` from the activated venv. Do not choose a Python version or create the venv automatically; that is the user's decision.

```bash
.venv/bin/tox -e formats    # Reformat: black + isort
.venv/bin/tox -e lints      # Lint: black, blackdoc, isort, flake8, mypy
.venv/bin/tox -e devs       # Fast tests: --exitfirst, skip slow, random order
.venv/bin/tox -e tests      # Full test suite with coverage
```

Run a single test:
```bash
py.test pysyte/types/paths.py                          # doctests in module
py.test pysyte/types/test/test_paths.py                # unit tests
py.test --doctest-glob=*.test pysyte/types/paths.test  # .test file
```

## Architecture

pysyte is a utility library. Code lives under `pysyte/` as flat modules or small packages.

### Key packages

- **`types/`** — Extended types: `paths.py` (Path subclass, the core workhorse), `strings.py`, `lists.py`, `lines.py`, `dictionaries.py`, `numbers/`, `literals/`
- **`cli/`** — CLI framework: `app.py`, `arguments.py`, `config.py`, `streams.py`
- **`bash/`** — Shell integration: `shell.py`, `screen.py`
- **`colours/`** — ANSI/colour handling
- **`config/`** — Config management with XDG support
- **`ai/`** — AI/LLM integration
- **`oss/`** — OS-specific (darwin, linux, getch)

### Testing conventions

Three test forms, all discovered by pytest:
- `*.test` — doctest narrative (story-telling examples)
- `*.tests` — doctest bulk
- `test_*.py` — traditional pytest unit tests

Write failing doctests first when improving public APIs.

## Branching

- `__main__`: Primary — version bumped here after each PR merge (`vX.Y.{PR_NUMBER}`)
- `__dev__`: Active development (this clone)
- `__pypi__`: PyPI publishing
- `trees/`: Ongoing paths→trees refactor (blocking `v0.9`)

## PR Workflow

All PRs target `__main__`. Use `merge_to_main()` from `~/jab/src/bash/git/hub.sh` — it pushes the branch, creates the PR, merges it, checks out `__main__`, and bumps the patch version to match the PR number.

## Code Style

- black with single quotes (`-S`), 88-char lines
- isort with black profile
- flake8 ignores: E731, E203, W503
- mypy: `check_untyped_defs = true`, `strict_optional = true`
- No emojis in `*.md` files
