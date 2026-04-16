---
description: Post-solve reflection on a completed exercise
argument-hint: "[NNN]"
---

Help the learner consolidate what they learned from a completed exercise.

1. Determine the exercise: use `$ARGUMENTS` if provided, otherwise the
   current exercise from `python marathon.py status`.
2. Read the exercise's `README.md` (for topic tags and context), the
   learner's `problem.py` (their solution), and `.meta/notes.md` (if it
   exists and has substantive content).
   **Never read `.meta/solution.py`.**
3. Walk the learner through these reflection prompts:
   - **Pattern recognition**: "What data structure / algorithm / design
     pattern did this exercise test? Where does this show up in
     production systems?"
   - **Code review**: "Looking at your solution, what would you change
     if this needed to handle 10x the input size, or run in production?"
   - **Interview follow-ups**: "An interviewer who just watched you solve
     this might ask: [2-3 concrete follow-up questions tailored to the
     exercise]."
4. Keep each prompt to 1-2 sentences — the learner should do the
   thinking, not read a wall of text.
