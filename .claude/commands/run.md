---
description: Run tests for an exercise (default current)
argument-hint: "[NNN]"
---

Run `python marathon.py run $ARGUMENTS` from `exercises/`. If no id was
passed, use `--current`.

- If tests pass: congratulate briefly, mention the time/tier, and ask if
  they want to move to the next one with `/next`.
- If tests fail: read the `--tb=short` output, identify the failing
  assertion, and ask a Socratic question pointing at the likely cause
  without writing the fix. Do not read `.meta/solution.py`.
