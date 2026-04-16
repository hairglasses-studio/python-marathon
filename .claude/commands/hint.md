---
description: Get an exercise-specific hint without spoilers
argument-hint: "[NNN] [level]"
---

Generate a hint for the exercise specified by `$ARGUMENTS` (default: the
current exercise from `python marathon.py status`).

**First**, register the hint usage in the progress file by running
`python marathon.py hint NNN --level N` (from `exercises/`). This ensures
`.marathon_progress.json` tracks hint usage whether the learner uses
the CLI or Claude Code. Then proceed with generating your own hint below.

**Hint sources, in priority order:**
1. `README.md` — the problem statement
2. `problem.py` — the signature and any docstring
3. `test_problem.py` — the behavioral spec (especially for tier3)
4. `.meta/hints.md` — fall back only if you need calibration; for
   exercises 001-026 these are generic boilerplate, so treat them as a
   tone reference, not as content.

**Do NOT read `.meta/solution.py`** — it is denied by settings.json and
reading it defeats the entire point of hinting.

**Structured Socratic hint protocol:**

- **Level 1 (default):** You MUST respond with a **question**, not a statement.
  Ask what category of solution the learner is considering — nudge toward
  the right data structure, algorithm, or stdlib module. No code, no
  direct answers. Example: "What data structure gives you O(1) lookup
  by key?"

- **Level 2:** Give a **directional statement** — an outline of the approach
  in 3-5 bullets. Name the specific functions/classes the learner should
  use, but still no code. End with a question about the hardest sub-step.

- **Level 3:** Provide a **code fragment** of the hardest sub-step only
  (e.g. the recurrence, the dunder method, the async pattern). Leave the
  rest to the learner. End with a question about how to connect this
  fragment to the rest of their solution.

Every hint at every level MUST end with one question that pushes the
learner toward the next step they should take themselves.
