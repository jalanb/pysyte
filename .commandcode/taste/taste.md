# Taste (Continuously Learned by CommandCode.ai)

# Code Style
- Follow KISS (Keep It Simple, Stupid), DRY (Don't Repeat Yourself), and YAGNI (You Aren't Gonna Need It) principles. Confidence: 0.85

# Python
See [python/taste.md](python/taste.md)
# Project Context
- Primary languages are Python and bash. Confidence: 0.70
- Prefer to work from parent jalanb/ directory using relative paths to subprojects, rather than cd'ing into subproject directories. Confidence: 0.85
- Primary mission: Help jalanb write new code to his standards and bring old code up to those same standards (includes code review, modernization, and de-corporatizing old code). Confidence: 0.85
- For pre-1.0 projects: prioritize code quality over backward compatibility. Everything is up for grabs until 1.0 release. Confidence: 0.85
- Use COMMANDCODE.md as the context file for CommandCode.ai (similar to CLAUDE.md for Claude, AGENTS.md for ChatGPT). Confidence: 0.85

# Workflow
See [workflow/taste.md](workflow/taste.md)
# Markdown
- Use `__bold__` instead of `**bold**` for emphasis in markdown files (see jalanb/library/howto/markdown.md lines 17-18). Confidence: 0.85

# Focus
- Specialize in source code work rather than execution/devops as team grows. Confidence: 0.70

# Terminology
- Use "tactical" and "strategic" instead of "low/mid/high" when discussing code issues and priorities. Confidence: 0.85

# Bash
- For bashrcs/**/*.sh files (which are sourced, not executed), use shebang `#!/usr/bin/env bat` instead of `#!/usr/bin/env bash`. Confidence: 0.70
- Add docstrings to all bash functions using format: `local __doc__="""description here"""` as first line of function. Confidence: 0.85
- All local variables should have a trailing underscore (e.g., `local tmpfile_=$(mktemp)`). Confidence: 0.85
- Prefix internal/helper functions with underscore (e.g., `_fred_step()`) to indicate they're not meant to be called directly by users, only internally. Confidence: 0.85

