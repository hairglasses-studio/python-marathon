---
description: Suggest exercises to revisit for spaced repetition
---

Help the learner identify exercises worth revisiting for long-term retention.

1. Run `python marathon.py status` and read `.marathon_progress.json`
   (at `exercises/.marathon_progress.json`) to get per-exercise data.
2. From the passed exercises, identify candidates for review using these
   heuristics (in priority order):
   - **High hint usage**: exercises where `hints_used` >= 2 suggest the
     learner needed significant help and may not retain the pattern.
   - **Revealed**: exercises marked `revealed: true` were solved by
     looking at the answer — prime candidates for a clean redo.
   - **Oldest solves**: exercises solved earliest (by `first_solved`)
     are most likely to have faded from memory.
3. Suggest 1-3 exercises to revisit. For each, state:
   - The exercise name and tier
   - Why it's a good candidate ("you used 2 hints", "solved 5 days ago")
   - Whether to `/reset NNN` and rework from scratch, or just review
     mentally ("could you solve this again without hints?")
4. If fewer than 3 exercises have been solved, skip review and suggest
   continuing with `/next` instead.
