# python-marathon — Agent Instructions

Canonical instructions for LLM agents (Claude, Codex, Gemini, Copilot) working on this repo. `CLAUDE.md`, `GEMINI.md`, and `.github/copilot-instructions.md` are thin mirrors that point here.

## What this is

`python-marathon` is a rustlings-for-python style exercise runner for Python interview prep. Ordered, self-checkable exercises + a single-file CLI runner (`marathon.py`) that wraps pytest with progress tracking, hint gating, and solution reveal.

## Architecture

```
python-marathon/
  exercises/              # The exercise bank
    marathon.py           # CLI runner (~280 lines, zero non-pytest deps)
    conftest.py           # Shared pytest fixtures
    pytest.ini            # Pytest config — no testpaths (run per-exercise)
    README.md             # User-facing marathon guide
    tier1_fluency/        # Beginner drills (9)
    tier2_patterns/       # Interview primitives (11)
    tier3_canonical/      # Full multi-gate problems (6)
    tier4_async/          # asyncio exercises (5, hand-written)
  .claude/                # Claude Code learning-mode configuration
    settings.json         # Permission rules (deny solutions, scope edits)
    commands/             # Slash commands (/status, /next, /run, /hint, /reveal, /reset)
  scripts/
    build_exercises.py    # One-shot notebook → exercise converter
  README.md
  AGENTS.md               # This file
  LICENSE                 # MIT
```

## Build and test

No build step — this is pure Python. Setup a dev environment:

```bash
cd exercises
uv venv .venv --python 3.10
VIRTUAL_ENV=.venv uv pip install pytest
```

Or with plain pip:

```bash
cd exercises
python3.10 -m venv .venv
.venv/bin/pip install pytest
```

`marathon.py` auto-detects `exercises/.venv/bin/python` and uses it for pytest subprocess calls. If no venv exists, it falls back to `pytest` in PATH.

## Conventions

### Exercise directory shape

Every exercise follows the same 7-file layout:

```
NNN_slug/
  README.md                # Problem statement (pulled from source markdown if converted)
  problem.py               # Stub — only file the learner edits
  test_problem.py          # Pytest tests, never edited
  .meta/
    stub.py                # Snapshot of original stub for marathon.py reset
    solution.py            # Reference solution
    hints.md               # 3 progressive hints under ## Hint 1, 2, 3
    notes.md               # Why it matters + pitfalls (optional)
```

**The `from problem import *` pattern** is used in every test file. Each exercise directory has no `__init__.py`, so pytest's default import mode prepends the exercise dir to `sys.path`, making `from problem import X` resolve to the local `problem.py`.

**Caveat:** this means you cannot run `pytest` from the `exercises/` root — every test file imports from a module called `problem`, so they collide. Use `marathon.py run NNN` (which passes an explicit exercise path) or invoke pytest on one exercise directory at a time.

### marathon.py design

Single file, no external deps. Uses `subprocess.run` to invoke pytest. Progress cached in `.marathon_progress.json` (gitignored). Commands:

- `status` — tier progress table + next unsolved
- `list [--tier N]` — flat list with status
- `run NNN [--current]` — run tests for one exercise
- `next` — auto-find and run next unsolved
- `watch [NNN]` — poll mtime, re-run on change (no watchdog dep)
- `hint NNN --level N` — print hint level N (1-3), records usage
- `reveal NNN` — print solution (gated on typing `REVEAL NNN`)
- `reset NNN` — restore problem.py from `.meta/stub.py`, clear progress

### Adding a new exercise

Hand-written path:

1. Create a new numbered directory under the right tier
2. Write `problem.py` with a typed signature + 1-line docstring + `raise NotImplementedError("fill me in")`
3. Write `test_problem.py` — pytest cases ordered trivial → edge → adversarial. Use `from problem import *` at the top.
4. Write `.meta/solution.py` — reference answer
5. `cp problem.py .meta/stub.py` — snapshot for `marathon.py reset`
6. Write `README.md` — problem statement, I/O spec, target time, topic tags
7. Write `.meta/hints.md` — 3 sections `## Hint 1`, `## Hint 2`, `## Hint 3` (progressive: nudge → approach → near-solution)
8. Write `.meta/notes.md` — optional but useful
9. **Validate your reference solution passes your tests** — temporarily copy `.meta/solution.py` to `problem.py`, run `python marathon.py run NNN`, verify pass, then `marathon.py reset NNN`

### Notebook-sourced exercises

`scripts/build_exercises.py` reads Jupyter notebooks and materializes exercise directories. Expects a pattern of 3 adjacent cells: scaffold (stub with `raise NotImplementedError`), tests (loose asserts), and solution (reference). Supports an optional `prelude_cell` for problems with a separate "shapes" cell (dataclasses/exceptions).

The converter is currently hard-coded against 4 specific notebooks from a private prep directory. To adapt for your own notebooks, edit the `SPECS` list with your cell indices. A future refactor could move this to a YAML config.

### Test conventions

- One `def test_all():` per exercise (the converter wraps notebook test cells into this single function; hand-written exercises follow the same pattern for consistency)
- Deterministic — no `hypothesis`, no property-based testing, no random seeds beyond `conftest.py`'s `random.seed(42)` fixture
- Tests should fail cleanly when the stub's `raise NotImplementedError` fires (pytest's `--tb=short` output tells the learner exactly where the stub is)

### Solution hiding

**Reality check:** on a local filesystem, solutions are socially hidden only. `cat .meta/solution.py` always works. The `.meta/` convention + `marathon.py reveal` confirmation gate makes the reveal *intentional*, not *accidental* — that's the goal.

If you're adding exercises to a public repo, **don't check in solutions to the public branch** if you want meaningful hiding. Instead: keep `.meta/solution.py` in a private branch/repo and distribute only the stub + tests.

## Claude Code learning mode

The `.claude/` directory configures Claude Code as an interactive tutor when launched from this repo. The configuration has three layers:

1. **`.claude/settings.json`** — permission rules that deny reading `.meta/solution.py` and `.meta/stub.py`, restrict edits to `exercises/**/problem.py` only, pre-allow `marathon.py` commands, and put `reveal` behind an explicit approval gate.

2. **`.claude/commands/`** — nine slash commands (`/status`, `/list`, `/next`, `/run`, `/hint`, `/reflect`, `/review`, `/reveal`, `/reset`) that wrap `marathon.py` subcommands with tutor-appropriate behavior. `/reflect` adds post-solve deepening; `/review` provides spaced-repetition suggestions.

3. **`CLAUDE.md`** — a "Learning Mode" section describing the tutor contract: Socratic-first posture, generate exercise-specific hints, never reveal solutions unprompted.

All 31 exercises now have exercise-specific `.meta/hints.md` (3 progressive levels each) and substantive `.meta/notes.md` (why it matters, gotchas, interview follow-ups). The `/hint` command also registers usage in `.marathon_progress.json` via the CLI before synthesizing its own response.

**If you're adding a non-Claude agent integration** (Codex, Gemini, Copilot): follow the same principle — deny access to `.meta/solution.py`, scope edits to `problem.py`, and instruct the agent to tutor rather than solve. The `.claude/` configuration is Claude-harness-specific, but the philosophy applies to any agent.

## Sensitivity rules

- **No personal paths or identifiers** in exercise content. A scrub pass was done on the initial commit to remove interviewer names and overly-specific framing. When adding new content, keep the tone generic — refer to "interview prep" rather than any specific company/panel/date.
- **No `.env` files** — nothing here needs secrets.
- **Mirror conventions**: `AGENTS.md` is canonical; `CLAUDE.md` and `GEMINI.md` are thin mirrors. Don't duplicate content across them.

## Repo status

- Created: 2026-04-15
- Origin: extracted from a private interview-prep directory on the day before a senior Python interview; the exercise bank and harness are generic and reusable.
- Current exercise count: 31 (9 tier1 + 11 tier2 + 6 tier3 + 5 tier4)
- All Tier 4 async solutions validated against their own tests
