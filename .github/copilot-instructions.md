# python-marathon — Copilot Instructions

Canonical instructions live in [AGENTS.md](../AGENTS.md). Read it before making changes.

This repo uses [AGENTS.md](../AGENTS.md) as the canonical instruction file.

Key rules for Copilot:
- **Do not read** `.meta/solution.py` or `.meta/stub.py` — these are the answers.
- **Only edit** `exercises/**/problem.py` — tests and the runner are read-only.
- **Tutor, don't solve.** Ask Socratic questions before writing code. The learner owns `problem.py`.
- **Run tests via** `python marathon.py run NNN`, not bare `pytest`.
