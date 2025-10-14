# short_dir

A command-line utility for shortening directory paths by replacing environment variables and symlinks with their abbreviated forms.

## Purpose

This module provides intelligent path abbreviation by:
- Replacing `$HOME` with `~`
- Using symlinks in home directory to create shorter path representations
- Finding the shortest possible representation of a given directory path

## Usage

Run as a script to abbreviate directory paths:

```bash
python -m pysyte.short_dir [directories...]
```

### Options
- `-o, --only_home`: Only replace $HOME with ~, skip other abbreviations
- `-x, --exclude`: Exclude specific environment symbols from replacement
- `-v, --version`: Show version information

### Examples
```bash
# Abbreviate current directory
python -m pysyte.short_dir

# Abbreviate specific directories
python -m pysyte.short_dir /usr/local/bin ~/Documents/projects

# Only use home abbreviation
python -m pysyte.short_dir --only_home /Users/username/projects
```

## Implementation

The module analyzes paths by:
1. Finding symlinks in the home directory that point to subdirectories
2. Checking environment variables that contain directory paths
3. Selecting the shortest possible representation
4. Falling back to simple `$HOME` → `~` replacement

## Key Functions

- `script()`: Main entry point that processes directories and outputs abbreviated paths
- `sub_script()`: Core logic for finding shortest path representation
- `replace_links()`: Handles symlink-based abbreviations
- `replace_home()`: Converts `$HOME` to `~`
- `shortest()`: Selects the shortest path from available options

## Integration

Part of the pysyte foundational library's path manipulation utilities. Works with:
- `pysyte.types.paths`: For path object operations
- `pysyte.cli.main`: For command-line interface framework