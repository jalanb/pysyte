
# trees

This is a major refactor of `pysyte.types.paths` as `pysyte.types.trees`

## Parent Project Context

This clone is part of the **pysyte** project, a foundational Python library that "adds batteries to Python, bash, and other languages near them."

Development workflow and project requirements are documented in README.md.

## Refactor Status

### Current Status
- **Circular imports FIXED** - The main blocker has been resolved using TYPE_CHECKING and lazy imports
- **Basic structure working** - imports succeed, modular structure is functional
- **Many tests failing** - Missing classes (DotPath), methods (extend_by), and other functionality
- **Incomplete migration** - Not all functionality has been moved/implemented in the new structure

### What's Working
- `from pysyte.types import paths` - imports successfully
- `from pysyte.types.trees.*` - all tree modules import without circular dependency errors
- Basic path creation and manipulation

### What's Broken/Missing
- `DotPath` class - referenced in tests but doesn't exist
- `extend_by` method on FilePath - used in test setup
- Various other methods and functionality that haven't been migrated yet
- Complete Public API should be covered by doctests

## Integration with Main Project

This refactor is part of the broader pysyte development strategy:
- Development happens in this `trees/` clone
- Integration planned for next minor release (v0.9.0)
- Will coordinate with `__dev__` clone for final integration
- Must maintain compatibility with existing entry points

## Next Steps
When we are finished we shall rename "trees" to "paths"

**Don't panic about test failures** - this is expected during a major refactor!

