# CommandCode.ai Context for pysyte/trees

## Project Archaeological Context

This codebase is **~10 years old** with multiple historical layers:
- Started 2018 (Python 3.6 era)
- Based on earlier "dotsite" project (Python 2.x era)
- Contains code from various sources over the years
- **Corporate code smuggling**: bits copied from work projects with their own styles/assumptions
- My "good code" philosophy revises every 3-5 years → expect multiple style generations

## Current Mission: Systematic Code Quality Review

We're about to **rip this code to shit** to find all the ways it violates coding standards.

### Goals
1. **Extract implicit rules** - Find patterns that reveal unstated preferences
2. **Discover unknown rules** - Rules I don't even know I have
3. **Document violations** - Where code breaks stated standards
4. **Adopt community practices** - Modern Python patterns worth adding

### What We're Looking For
- **Python version fossils** - 2.x workarounds, pre-3.6 patterns, pre-3.9 type hints
- **Corporate contamination** - Enterprise verbosity, unnecessary abstractions, defensive coding
- **Style inconsistency** - Different eras, different sources, different standards
- **Conceptual obsolescence** - Good implementations of ideas that shouldn't exist anymore

## Issue Classification System

We use **4 levels** (not low/mid/high):

### Quick Wins (Fix Immediately)
Mechanical fixes, no design impact, high priority:
- Default arguments → singledispatch
- `+=` → `.append()`/`.extend()`
- Blank lines inside functions → delete
- Missing type annotations → add
- `**bold**` → `__bold__` in markdown

### Documentish (Documentation & Testing)
- Missing doctests (critical - these ARE the unit tests)
- Missing docstrings
- Docstring formatting issues
- Module-level narrative doctests
- English explanations where needed

### Tactical (Code Structure)
Mid-level refactors, do when touching files:
- Long functions → break up
- Repeated values → extract names (DRY)
- Corporate verbosity → simplify
- Function-level refactoring

### Strategic (Architecture)
High-level design, document but fix LAST:
- `pysyte.path.Path` → `pathlib.Path` (example: do at very end)
- Entire obsolete modules
- Core abstractions from old Python eras
- "Why does this exist?" questions

## Priority Strategy

1. **Fix quick wins first** - Everywhere, easy, high ROI
2. **Add documentish** - Doctests are the only unit tests
3. **Tactical as you go** - When touching a file for quick fixes
4. **Document strategic issues** - Note them, plan them, DON'T FIX YET

Don't get stuck redesigning architecture when we should be fixing default args.
Don't waste time fixing default args in code about to be deleted.

## Project Constraints

### Pre-1.0 Freedom
- **Version <1.0** → Everything is up for grabs
- **Zero external users** → No API stability needed
- **Only constraint**: My other projects (but I control those)
- **Goal**: Quality over compatibility
- Ship 1.0 when it's actually good, not "good enough for 2018"

### Testing Reality
- **Light on tests** - Other projects are the integration test suite
- **Personal use** - Lower quality bar than production
- **Doctests critical** - They're the ONLY unit tests
- May need cross-project searches: `grep -r "from pysyte" ~/projects/`

### De-corporatizing Mission
From taste: "Primary mission: bring old code up to those same standards (includes code review, modernization, and **de-corporatizing old code**)."

Strip out:
- Enterprise bloat
- Unnecessary abstractions
- Defensive over-engineering
- Return to KISS/DRY/YAGNI

## Key Architectural Context

### Current Refactor Status
- Working on Phase 1 of 5-phase plan (see PLAN.md)
- Circular imports FIXED
- Basic structure working
- Missing: DotPath class, extend_by method, other functionality
- Eventually: rename trees/ back to paths/

### Historical Design Decisions
- `pysyte.path.Path` based on "Jason Orendorff's Path" (pre-pathlib era)
- This is a **strategic** issue - will be one of FINAL changes
- Many patterns exist due to Python 2.x/early 3.x limitations

## Next Steps

Ready to start systematic teardown:
1. Analyze sample code for implicit patterns
2. Check against stated taste rules
3. Document violations by level (quick/documentish/tactical/strategic)
4. Identify new rules to add to taste
5. Create prioritized fix list

Focus on trees/ code first since it's current work, but may need to look at broader pysyte codebase to establish baseline patterns.
