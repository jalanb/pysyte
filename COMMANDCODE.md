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

## Development Workflow

### Tox Command Discipline
Always activate venv first: `source .venv/bin/activate`

**Command sequence** (never skip ahead on failures):
1. `tox -e formats` - Run early and often (should be on every save ideally)
2. `tox -e lints` - Run after "finished a section", often same as commit size
3. `tox -e devs` - Run while developing (fast, stops on first failure)
4. `tox -e tests` - Run when ready for commit (full suite, slower tests)

**Critical rule**: Do NOT move on from failures. If lints fails, fix it completely before trying devs.

### The Game Plan: Collaborative Code Analysis

**NOT a "fix-it-fast" session** - This is about extracting taste rules through systematic analysis.

#### Process for Each Lint Error
1. **Group similar errors** - Look for patterns across files/lines
2. **For each error/group, present**:
   - Minimal code context (just enough to show the issue)
   - Linter error message
   - Suggested fix
   - **Underlying rule/smell/principle** - Why does this matter?
3. **Discuss together** - Chat about the "why"
4. **User makes the fix** - Not CommandCode (keeps it real with typos!)
5. **Extract taste rule** - Document the pattern for future

#### What to Track
- **Running discoveries list** - Patterns found today in markdown
- **Classification by level** - Tag as quick/documentish/tactical/strategic
- **"Why it matters"** - The high-level principle, not just the rule
  - Expect more duplicates at this level than at the syntax level
  - Fewer personal rules than flake8/pylint have rules
- **Historical context** - Is this a Python 2.x fossil? Corporate import? Just a mistake?

#### Key Insight
The goal is building the taste system, not just passing lints. Fixes are secondary to understanding WHY things are wrong and documenting those patterns.

## Next Steps

Ready to start systematic analysis:
1. Run lints and group errors by pattern
2. Analyze each group for underlying principles
3. Document violations by level (quick/documentish/tactical/strategic)
4. Identify new rules to add to taste
5. User fixes code, we verify and move to next group

Focus on trees/ code first since it's current work, but may need to look at broader pysyte codebase to establish baseline patterns.
