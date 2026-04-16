---
description: Get an exercise-specific hint without spoilers
argument-hint: "[NNN] [level]"
---

Generate a hint for the exercise specified by `$ARGUMENTS` (default: the
current exercise from `python marathon.py status`).

**Hint sources, in priority order:**
1. `README.md` — the problem statement
2. `problem.py` — the signature and any docstring
3. `test_problem.py` — the behavioral spec (especially for tier3)
4. `.meta/hints.md` — fall back only if you need calibration; for
   exercises 001-026 these are generic boilerplate, so treat them as a
   tone reference, not as content.

**Do NOT read `.meta/solution.py`** — it is denied by settings.json and
reading it defeats the entire point of hinting.

**Hint levels:**
- Level 1 (default): a nudge toward the right *category* of solution
  (data structure, algorithm, stdlib module) — no code.
- Level 2: an outline of the approach in 3-5 bullets — still no code,
  but name the specific functions/classes the learner should use.
- Level 3: a code sketch of the hardest sub-step (e.g. the recurrence,
  the dunder method), with the rest left to the learner.

End every hint with one question that pushes the learner toward the
next step they should take themselves.
