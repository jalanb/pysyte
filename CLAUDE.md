# pysyte __dev__ clone

## Project Overview

pysyte

A foundational Python library that adds batteries to Python, bash, and other languages near them

- **License**: MIT License
- **Python Requirements**: 3.13+

## Development Environment

Development workflow and commands are documented in README.md.

## Project Structure

### Core Dependencies
- bidict, boltons, deprecated, inflect>=2.1.0
- path.py==7.7.1, pym, pyyaml, rich
- stackprinter, textual, yamlreader

### Main Modules
- **ai/**: AI and language model integration
- **bash/**: Shell and screen utilities
- **cli/**: Command-line application framework
- **colours/**: ANSI escape codes and color handling
- **config/**: Configuration management
- **devops/**: Development operations utilities
- **types/**: Extended type system (paths, strings, lists, etc.)
- **unix/**: Unix-specific utilities

### Entry Points (Console Scripts)

Although primarily designed to be used like `from pysyte import`, we did add some scripts over the years:

- `kat`: and enhanced `cat`
- `keys`: frontend for `pysyte.oss.getch`
- `imports`: used by a script that show unused and duplicate imports
- `short_dir`: Shortens a directory path for my prompt


## Testing

- We use pytest with doctests enabled
- Coverage reporting with branch coverage
- Supports parallel test execution

## Development Workflow

### Branching Strategy

**Special Branches:**
- `__main__`: Primary branch (used instead of "master")
- `__dev__`: Main development branch for changes not big enough for their own branch
- `__pypi__`: PyPI publishing branch - uploads to pypi happen from here

**Feature Branches:**
- Use simple, descriptive names (no prefixes/suffixes)
- No "/" characters in branch names
- Examples: `trees`, `vim-mode`, `config-refactor`

### Testing Context
- Uses pytest with doctests embedded in `.test` and `.tests` files
- Branch coverage tracking with parallel execution support
- Two main testing modes: fast development feedback vs comprehensive CI/CD

### Clone Coordination
- **trees/**: Major refactor branch (paths → trees → paths)
- **Feature branches**: Regular rebase with `__main__`, clean git history
- **Version consistency**: Maintained across all clones via workflow discipline
