# pysyte.unix

Unix filesystem abstractions and utilities for the pysyte library.

## Package Overview

The `pysyte.unix` package provides abstractions for working with Unix filesystem concepts, particularly the foundational principle that Unix presents the filesystem as "one rooted tree of directories" rather than separate drive letters like DOS/Windows.

## Core Module

### `root.py`
The primary module implementing Unix filesystem concepts:

- **`UnixDirectory`** - Extends `pysyte.types.paths.DirectPath` for Unix-specific directory handling
- **`upath()`** - Factory function for creating `UnixDirectory` instances (for consistency with `path()`)
- **`root`** - Pre-instantiated `UnixDirectory` object representing the filesystem root (`/`)

The module emphasizes the Unix philosophy where all storage (disk partitions, removable media, network shares) appears as part of a single tree through mounting, rather than as separate trees with drive letters.

## Architecture

Built on the pysyte type system:
- Inherits from `pysyte.types.paths.DirectPath` for core path functionality
- Uses `pysyte.config.types.ModuleConfiguration` for module configuration
- Follows pysyte's batteries-included philosophy for filesystem operations

## Testing

Located in `test/` directory following project conventions:

- **`root.test`** - Doctests validating Unix filesystem root functionality
- Tests ensure the root directory object behaves correctly (`root.root.isdir()`)
- Validates module documentation and API examples

## Integration Context

Part of the `__dev__` clone of pysyte (main development branch). This package:
- Provides Unix-specific filesystem abstractions
- Complements the broader `pysyte.types.paths` module with Unix concepts
- Supports cross-platform path handling within the pysyte ecosystem

## Usage

```python
from pysyte.unix import root, upath

# Access filesystem root
assert root.root.isdir()

# Create Unix directory objects
home = upath("/home")
tmp = upath("/tmp")
```

The package focuses specifically on Unix filesystem semantics and should be used when working with Unix-style filesystem operations within the pysyte library.