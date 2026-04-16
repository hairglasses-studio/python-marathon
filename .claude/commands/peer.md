---
description: View a study partner's submitted answer (gated on your own solve)
argument-hint: "NNN [--user NAME]"
---

View another user's submitted answer for exercise $ARGUMENTS.

1. Run `python marathon.py peer $ARGUMENTS` from `exercises/`.
   If `--user` was not provided, check `exercises/answers/` for other
   user directories and use the first one that isn't the current user.
2. If the gate passes (you've solved it, they've submitted), display their
   solution and offer brief Socratic comparison: what's similar, what's
   different, any interesting trade-offs.
3. If the gate fails, relay the message (haven't solved yet / peer hasn't
   submitted) without trying to bypass.
