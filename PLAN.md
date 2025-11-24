# trees Refactor Plan

## Mission Statement
Transform the monolithic `pysyte.types.paths` module into a modular `pysyte.types.trees` package, then rename back to `paths` for seamless integration.

## Refactor Strategy

### Phase 1: Complete Missing Components (Current Focus)
**Priority**: High - Restore basic functionality

#### 1.2 Missing Methods  
- [ ] **extend_by method** on FilePath - Used in test setup
  - Port from original paths.py
  - Maintain API compatibility
  - Add comprehensive testing

#### 1.3 API Completeness Audit
- [ ] Compare trees/ public API with original paths.py
- [ ] Identify all missing methods/classes/functions
- [ ] Create implementation checklist
- [ ] Prioritize by test failure impact

### Phase 2: Test Resolution
**Priority**: High - Stabilize the refactor

#### 2.1 Test Failure Analysis
- [ ] Run `tox -e devs` to get fast failure feedback
- [ ] Categorize failures by type:
  - Missing classes/methods
  - Import errors
  - API changes
  - Doctest failures

#### 2.2 Systematic Test Fixing
- [ ] Fix import-related failures first
- [ ] Address missing component failures
- [ ] Resolve API compatibility issues
- [ ] Ensure all doctests pass

#### 2.3 Test Coverage Validation
- [ ] Run `tox -e tests` for full coverage
- [ ] Verify no regression in other modules
- [ ] Check doctest coverage across trees/

### Phase 3: Quality Assurance
**Priority**: Medium - Ensure production readiness

#### 3.1 Code Quality Checks
- [ ] Run `tox -e formats` - ensure black/isort compliance
- [ ] Run `tox -e lints` - resolve all mypy/flake8 issues
- [ ] Review type annotations consistency
- [ ] Validate docstring completeness

#### 3.2 Performance Validation
- [ ] Compare performance with original paths.py
- [ ] Identify any performance regressions
- [ ] Optimize critical path operations
- [ ] Benchmark against existing usage patterns

#### 3.3 Documentation Review
- [ ] Update module-level docstrings
- [ ] Ensure API documentation completeness
- [ ] Validate example code in doctests
- [ ] Cross-reference with parent project docs

### Phase 4: Integration Preparation
**Priority**: Medium - Ready for main project merge

#### 4.1 Backward Compatibility
- [ ] Ensure all existing imports still work
- [ ] Validate entry point compatibility (kat, keys, imports, short_dir)
- [ ] Test with parent project test suite
- [ ] Create migration guide if needed

#### 4.2 Final Validation
- [ ] Full test suite passes in trees/ clone
- [ ] Integration testing with __dev__ clone
- [ ] Performance benchmarks meet requirements
- [ ] Documentation is complete and accurate

### Phase 5: Rename and Deploy
**Priority**: Low - Final integration step

#### 5.1 Package Rename
- [ ] Rename `trees/` back to `paths/`
- [ ] Update all internal imports
- [ ] Verify no references to old names
- [ ] Update documentation references

#### 5.2 Integration with Main Project
- [ ] Merge into __dev__ clone
- [ ] Coordinate with main development workflow
- [ ] Plan integration timeline for next minor release
- [ ] Update project roadmap

## Success Criteria

### Functional Requirements
- ✅ All circular import issues resolved
- ⏳ All tests pass (`tox -e tests`)
- ⏳ All code quality checks pass (`tox -e lints`)
- ⏳ No performance regressions
- ⏳ 100% API compatibility with original

### Integration Requirements  
- ⏳ Seamless integration with parent project
- ⏳ Entry points continue to function
- ⏳ No breaking changes for existing users
- ⏳ Ready for next minor release

## Risk Management

### Known Risks
1. **Test failures cascade** - Many failures may indicate deeper architectural issues
2. **Performance regression** - Modular structure might impact performance
3. **API compatibility** - Subtle behavior changes could break dependent code
4. **Integration complexity** - Merging back may reveal hidden dependencies

### Mitigation Strategies
1. **Incremental approach** - Fix tests in small batches
2. **Continuous benchmarking** - Monitor performance throughout
3. **Extensive testing** - Use both unit and integration tests
4. **Staged integration** - Test merge in isolation first

## Timeline Estimate

- **Phase 1**: 1-2 weeks (Missing components)
- **Phase 2**: 2-3 weeks (Test resolution)
- **Phase 3**: 1 week (Quality assurance)
- **Phase 4**: 1 week (Integration prep)
- **Phase 5**: 1 week (Rename and deploy)

**Total**: 6-8 weeks for complete refactor

## Next Immediate Actions

1. **Start with DotPath class** - High impact, referenced in multiple tests
2. **Implement extend_by method** - Required for test setup
3. **Run `tox -e devs`** - Get immediate feedback on critical failures
4. **Document findings** - Update this plan based on discoveries
