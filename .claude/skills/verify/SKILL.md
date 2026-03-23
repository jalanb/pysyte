---
name: verify
description: Run lints and fast tests to verify work is correct before marking a task done. Use before completing any feature or fix.
---

Run lints then fast tests in the project root:

```bash
.venv/bin/tox -e lints && .venv/bin/tox -e devs
```

Report any failures clearly. Do not mark work as complete until both pass.
