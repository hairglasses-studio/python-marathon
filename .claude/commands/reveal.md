---
description: Reveal the reference solution (double-gated)
argument-hint: "NNN"
---

Revealing the reference solution requires two confirmations:

1. **The harness** will prompt for approval because
   `Bash(python marathon.py reveal:*)` is in the `ask` permission list.
2. **`marathon.py` itself** will prompt for the learner to type
   `REVEAL $ARGUMENTS` on stdin.

Before running anything, ask the learner to confirm they actually want
to reveal. If they say yes, tell them to run this themselves from their
shell (not through you), since the confirmation prompt needs interactive
stdin that the Claude Code Bash tool cannot provide:

```
! python marathon.py reveal $ARGUMENTS
```

The `!` prefix runs it in their session and the output will land back in
the conversation.
