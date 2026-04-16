---
description: Submit your passing solution to the shared answers directory
argument-hint: "NNN"
---

Submit the learner's solution for exercise $ARGUMENTS.

1. Run `python marathon.py submit $ARGUMENTS` from `exercises/`.
2. If it succeeds, run `git add` on the new file and `git commit` with
   message format: `answer(<user>): NNN <slug>`.
3. Print the commit hash. Do NOT push — let the learner decide when to push.
4. If it fails (exercise not solved, no identity set), relay the error
   message and help them fix it.
