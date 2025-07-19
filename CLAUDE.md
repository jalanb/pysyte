
# trees

This is a major refactor of `pysyte.types.paths` as `pysyte.types.trees`


## Current Status
- **Circular imports FIXED** - The main blocker has been resolved using TYPE_CHECKING and lazy imports
- **Basic structure working** - imports succeed, modular structure is functional
- **Many tests failing** - Missing classes (DotPath), methods (extend_by), and other functionality
- **Incomplete migration** - Not all functionality has been moved/implemented in the new structure

## What's Working
- `from pysyte.types import paths` - imports successfully
- `from pysyte.types.trees.*` - all tree modules import without circular dependency errors
- Basic path creation and manipulation

## What's Broken/Missing
- `DotPath` class - referenced in tests but doesn't exist
- `extend_by` method on FilePath - used in test setup
- Various other methods and functionality that haven't been migrated yet
- Complete Public API should be covered by doctests

## Next Steps
When we are finished we shall rename "trees" to "paths"

**Don't panic about test failures** - this is expected during a major refactor!

