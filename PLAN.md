# pysyte Development Plan

## Project Roadmap

### Current Status
- **Phase**: Active development in `__dev__` clone
- **Target**: Stabilize for next minor release
- **Version info**: See pyproject.toml

### Strategic Goals

#### 1. Version Roadmap Strategy
- **v0.9**: Complete `trees/` refactor integration as primary milestone
- **v1.0**: Integrate DevOps code donated by WWTS + major cleanup + comprehensive doctests
- Patches: Bug fixes and minor improvements as needed

#### 2. GitHub Actions Integration
- Plan automated version consistency across all clones
- Automate PyPI publishing for major/minor releases
- Implement "upload this patch" mechanism for selective patch publishing
- Learn and expand GitHub Actions usage

#### 3. PyPI Publishing Improvements
- Streamline `__pypi__` clone workflow
- Automate build and upload process
- Implement pre-release testing
- Ensure package metadata accuracy

#### 4. Documentation and Testing Expansion
- Expand doctest coverage across all modules (critical for v1.0)
- Plan comprehensive testing strategy for DevOps code integration
- Improve test isolation and parallelization

## Entry Point Development Plans

### kat (pysyte.kat.__main__)
**Current Focus**: A better `cat`
- Add filtering and search capabilities  
- Improve output formatting options
- Consider integration with other tools

### keys (pysyte.keys.__main__)
**Current Focus**: UX for key bindings
- Consider vim-mode support

### imports (pysyte.imports.__main__)
**Current Focus**: Python import analysis and management
- Implement import optimization suggestions

### short_dir (pysyte.short_dir.__main__)
**Current Focus**: Directory path abbreviation
- Expand customizable abbreviation rules
- Examine enhanced shell integration
- Consider betterprompt integration features
 - Consider a new scipt to provide a prompt with all it needs
 - We are doing far too much in bash in "prompt.sh"

## Technical Debt and Improvements


### Module Reorganization
- Monitor `trees/` refactor progress
- Plan migration strategy for breaking changes
- Coordinate with other clone development
- Ensure backward compatibility where possible

### Dependencies Management
- Minimize dependency footprint
- Maintain Python 3.13 compatibility, till 3.14 is out
- examine the effects of upgrading the code through all the steps pyupgrade allows
  - and capturing on a single branch
  - and we re-do that for every version bump
   - make an "upgrades" branch, go through pyupgrade step-by-step
   - then merge that back into __main__
   - this needs more questions

## Release Planning

### v0.9 (Next Minor Release)
**Primary Goal**: Complete `trees/` refactor integration
- Finalize paths → trees → paths migration
- Entry point feature completions
 - we must ask questions about `python -m pysyte`
- Significant API improvements
 - and this
 - although I think we need to expand doctest coverage of what we have
 - then write the API improvements as doctests first failing tests
 - doctests are the best way to document the API to callers
  - hence also the best way to look at that API
  - and plan changes to it

### v1.0 (Major Release)
**Primary Goal**: Production-ready foundation with DevOps integration
- Integrate DevOps code donated by WWTS
- Major cleanup and refactoring
- Comprehensive doctest coverage across all modules
- API stabilization
- Full production readiness certification

### Patch Releases (as needed)
- Bug fixes from current development
- Documentation improvements
- Minor feature enhancements


## Development Priorities

1. **Immediate**: Complete `trees/` refactor (DotPath, extend_by, missing functionality)
2. **Short-term**: Stabilize trees integration for v0.9 release
3. **Medium-term**: Plan DevOps code integration strategy
4. **Long-term**: Prepare comprehensive v1.0 with full doctest coverage
