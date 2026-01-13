# Taste Discoveries - Session 2026-01-13

New taste rules discovered during today's code review session.

## Type Annotations

### Full Type Annotations Required
- Use full type annotations for all function arguments and returns
- Exception: When too annoying, use `# noqa` on the line
- CommandCode should auto-suggest missing type annotations

### Path Type Hierarchy (pysyte-specific)
**`StringPath` vs `Path` distinction**:
- `StringPath`: Top of hierarchy, includes ANY string (even "/not/a/path" or " ")
- `Path`: A string that's proven to be a real path (exists on filesystem)

**When to use which**:
- Use `StringPath` when: No idea what's coming back, could be any string
- Use `Path` when: You know/verified it's a real path (checked `.isfile()` or `.isdir()`)

**mypy edge case**: Sometimes you want `Path` but mypy can't follow your logic, so you must "downgrade" to `StringPath`. This is rare.

**Import pattern**: When `paths` already imported, use `paths.StringPath` or `paths.Path`

**Why it matters**: Type precision - be as specific as possible about what you actually have.

### Type Specificity
When guessing types from context, prefer the most specific type available.
- Example: `ImportVisitor` not just `Visitor`

## Code Organization

### Define Close to Use (YAGNI Locality)
**Rule**: Keep definitions as close as possible to where they're used.

**Don't move to module level until**:
- There's a **definite second caller** (not "might need it someday")

**Applies to**:
- Nested functions
- Constants
- Data structures (like `ignores = [...]`)

**Why it matters**:
1. **Flexibility**: Easier to move code around (one thing to move, not two)
2. **Forces questions**: Next dev has to ask "should I extract this?" rather than assuming
3. **Fewer dependencies**: Less to remember when refactoring

**Example**: `ignores = ["__pycache__", ...]` stays inside `find_sources()` until a second function needs it.

### Nested Functions - Nest Deeper
If a nested function is only called from one place in its parent, nest it further into that caller.

**Example**: 
```python
def parent():
    def helper():  # Only called from child()
        pass
    
    def child():
        helper()  # ← Should be nested inside child() instead
```

### Top-Level Scripts Should Be Thin
**Rule**: Top-level scripts (`__main__.py`) should **ONLY** handle shell interaction.

**Shell interaction includes**:
- Parsing arguments
- Printing output
- Main orchestration

**Move out to testable modules**:
- Business logic
- File operations
- Data processing
- Orchestration logic

**Why**: Can't easily test shell scripts. Business logic needs tests.

**Anti-pattern**: "utils.py" - use specific, meaningful module names instead.

## String Formatting

### Always Use F-Strings
- Always use f-strings (not `%` or `.format()`)
- Exception: Very few, very weird edge cases
- CommandCode should auto-suggest this change

**Example**:
```python
# Bad
"% 4d: %s" % (line_number, text)

# Good
f"{line_number:4d}: {text}"
```

## API Design

### Defaults Should Be Simple
**Rule**: Default behavior should be the simplest/most common case.

**Flags should ADD features, not remove them**.

**Anti-pattern**: Boolean flags that default to False and get passed as True are backwards.

**Example**:
```python
# Bad - flag turns ON the basic feature
thing.line(n)        # no line numbers
thing.line(n, True)  # WITH line numbers (backwards!)

# Good - default is simple, flag adds feature
thing.line(n)              # just the line (simple)
thing.numbered_line(n)     # line WITH number (separate method)
```

**Why it matters**: Principle of least surprise. Method names should promise what they deliver by default.

## Naming

### Names Should Suggest Correct Abstraction
If a function name sounds like it should be a method on a class, that's a code smell.

**Example**: `visitor_line()` sounds like `visitor.line()` - suggests either:
1. Should be a method on the visitor class, or
2. Should be renamed to not sound like a method (e.g., `format_line()`)

**Why it matters**: Names create expectations. Misleading names waste mental energy.

## Import Management

### Unused Imports Are a Tooling Problem
Don't manually fix unused imports - use automation:
```bash
python -m pysyte.imports -ume
```

This should be integrated into `tox -e formats` eventually.

## Classification of Issues

### Four Levels (not low/mid/high)

**Quick Wins**: Mechanical fixes, no design impact
- Missing type annotations
- F-string conversion
- Unused imports (via tooling)

**Documentish**: Documentation and testing
- Missing doctests
- Docstring formatting

**Tactical**: Code structure
- Long functions
- DRY violations
- Nested function placement

**Strategic**: Architecture
- Module organization
- Class design
- API design

## Historical Context Matters

When analyzing code issues, identify:
- **Python 2.x fossils**: Old workarounds no longer needed
- **Corporate contamination**: Enterprise patterns copied from work
- **Never-run code**: Missing imports indicate zero test coverage
- **Conceptual obsolescence**: Good code implementing outdated ideas

**Why it matters**: Understanding the "why" helps prioritize fixes and extract better rules.

## Confidence Levels

When documenting taste rules, include confidence level:
- 0.90+: Very confident, apply always
- 0.85: Confident, apply in most cases
- 0.70: Moderate confidence, consider context
- <0.70: Low confidence, needs more examples

## Next Rules to Investigate

Based on today's discoveries, areas to explore:
1. When to split modules vs keep together
2. Naming conventions for different types of modules
3. When nested functions are better than underscore-prefixed module functions
4. How to handle "almost generic" code (like `find_sources()`)
