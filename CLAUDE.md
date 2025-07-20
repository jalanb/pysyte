# pysyte __dev__ clone

## Project Overview

pysyte

A foundational Python library that adds batteries to Python, bash, and other languages near them

- **License**: MIT License
- **Python Requirements**: 3.13+

## Development Environment

Development workflow and commands are documented in README.md.

## Project Structure

Project structure, dependencies, entry points, and detailed testing information are documented in README.md.

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

### Clone Coordination
- **trees/**: Major refactor branch (paths → trees → paths)
- **Feature branches**: Regular rebase with `__main__`, clean git history
- **Version consistency**: Maintained across all clones via workflow discipline
- **Clone sync process**: Entirely manual, ad hoc, and as needed (no automation currently)
