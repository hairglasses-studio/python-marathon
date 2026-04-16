# python-marathon — Agent Instructions

> Canonical instructions: AGENTS.md

Canonical instructions for LLM agents (Claude, Codex, Gemini, Copilot) working on this repo. `CLAUDE.md`, `GEMINI.md`, and `.github/copilot-instructions.md` are thin mirrors that point here.

## What this is

`python-marathon` is a rustlings-for-python style exercise runner for Python interview prep. Ordered, self-checkable exercises + a single-file CLI runner (`marathon.py`) that wraps pytest with progress tracking, hint gating, and solution reveal.

## Architecture

```
python-marathon/
  exercises/              # The exercise bank
    marathon.py           # CLI runner (zero non-pytest deps)
    conftest.py           # Shared pytest fixtures
    pytest.ini            # Pytest config — no testpaths (run per-exercise)
    manifest.json         # Exercise source metadata (openai-prep, exercism, etc.)
    answers/              # Per-user submitted solutions (committed to git)
    tier1_fluency/        # Beginner drills (9)
    tier2_patterns/       # Interview primitives (11)
    tier3_canonical/      # Full multi-gate problems (6)
    tier4_async/          # asyncio exercises (5, hand-written)
    tier5_exercism_easy/  # Exercism imports — easy (10+)
    tier5_exercism_medium/ # Exercism imports — medium
  .claude/                # Claude Code learning-mode configuration
    settings.json         # Permission rules (deny solutions, scope edits) + model config
    commands/             # Slash commands (13 total)
  .codex/                 # Codex CLI project config
    config.toml           # Model, sandbox, approval policy
  .gemini/                # Gemini CLI context bridge
    settings.json         # Context file list
  .github/
    copilot-instructions.md  # Copilot mirror → AGENTS.md
  scripts/
    build_exercises.py    # One-shot notebook → exercise converter
    import_exercism.py    # Exercism Python track importer
    backfill_manifest.py  # One-shot manifest generator
  README.md
  AGENTS.md               # This file (canonical)
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

Single file, no external deps, 38 subcommands. Uses `subprocess.run` to invoke pytest. Progress cached in `.marathon_progress.json` (gitignored, per-user namespaced). User identity from `.marathon_user` file. Commands:

- `status` — tier progress table, XP, streak, badges, activity heatmap
- `run NNN [--current]` — run tests for one exercise (supports 2D addressing: `tier2 3`)
- `next` — auto-find and run next unsolved
- `list [--tier N]` — flat list with status
- `watch [NNN]` — poll mtime, re-run on change
- `challenge [--tier N]` — pick a random unsolved exercise
- `kata NNN` — re-solve from scratch (backs up current, tracks repetitions)
- `hint NNN --level N` — print hint level N (1-3), records usage
- `reveal NNN` — print solution (gated on typing `REVEAL NNN`)
- `reset NNN` — restore problem.py from `.meta/stub.py`, clear progress
- `submit NNN [--git]` — copy passing solution to `answers/<user>/NNN/`, optionally git commit
- `peer NNN --user NAME` — view peer's solution (gated on own solve)
- `challenge-peer NNN --user NAME` — create a timed challenge
- `tag [--filter TOPIC]` — list tags or filter exercises by topic
- `recommend` — suggest next exercises by tag coverage
- `review` — SM-2 spaced repetition queue with next-review dates
- `badges` — show earned and available achievements
- `export` — dump progress JSON to stdout
- `import-progress FILE` — merge progress from another machine
- `export-obsidian --vault PATH` — export solved exercises to Obsidian markdown
- `new --name SLUG --tier T` — scaffold a new exercise directory
- `pattern` — show all patterns with solved/total counts
- `curated [NAME]` — list or show curated exercise tracks (openai-interview, async-mastery, etc.)
- `map NNN` — print prerequisite chain as a tree
- `notes NNN` — open personal notes in $EDITOR
- `diff NNN --user NAME` — unified diff of your answer vs peer's
- `leaderboard` — show all users' solve counts and XP
- `peer-status` — show open peer challenges and resolution
- `deps` — show optional dependency status; `--install PKG` to install
- `lsp NNN` — generate pyrightconfig.json for one exercise
- `doctor` — self-diagnostics for environment and data
- `shell NNN` — REPL with problem.py pre-imported
- `verify [--changed-only]` — run all reference solutions against tests
- `lint-exercises` — validate 7-file layout for all exercises
- `import --slugs S [--tier T] [--dry-run]` — import Exercism exercises
- `completion {bash,zsh}` — generate shell completion script

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

## Multi-agent tutor support

This repo supports Claude Code, Codex CLI, Gemini CLI, and GitHub Copilot as interactive tutors. The tutor contract is the same across all tools:

- **Do not read** `.meta/solution.py` or `.meta/stub.py` — these are the answers.
- **Only edit** `exercises/**/problem.py` — tests and the runner are read-only.
- **Socratic-first posture.** Ask guiding questions before writing code.
- **Run tests via** `python marathon.py run NNN`, not bare `pytest`.
- **Never reveal solutions unprompted.** Route through `marathon.py reveal NNN`.

### Claude Code (full harness enforcement)

`.claude/settings.json` enforces deny rules at the harness level — Claude literally cannot read solutions even if asked. 13 slash commands in `.claude/commands/` provide the skill surface (`/status`, `/next`, `/run`, `/hint`, `/reflect`, `/review`, `/reveal`, `/reset`, `/list`, `/verify`, `/submit`, `/peer`, `/pull-questions`). `CLAUDE.md` describes the tutor contract in the Learning Mode section.

### Codex CLI (behavioral + sandbox)

`.codex/config.toml` sets `sandbox_mode = "workspace-write"` and `approval_policy = "on-request"`. Codex has no file-path deny rules — solution hiding is enforced behaviorally via this AGENTS.md instruction. The agent should follow the same tutor contract as Claude. No slash commands — use `marathon.py` subcommands directly.

### Gemini CLI (behavioral + context bridge)

`.gemini/settings.json` injects `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as context. No deny rules or slash commands. Tutor contract is behavioral only.

### GitHub Copilot

`.github/copilot-instructions.md` mirrors the tutor contract from AGENTS.md.

### Standalone CLI (no LLM required)

`marathon.py` provides full feature parity for non-LLM workflows with 25 subcommands (run `marathon.py --help` for the full list). The only features that require an LLM are: synthesized hints (beyond `.meta/hints.md`), Socratic failure analysis, post-solve reflection, and tutoring orientation.

## Recommended models

This repo is tuned for **$20/mo subscription plans**, not API billing:

| Tool | Default model | Plan | Why |
|------|--------------|------|-----|
| Claude Code | Sonnet 4.6 | Claude Pro ($20/mo) | Unlimited rate, excellent at code tutoring |
| Codex CLI | o3-mini | ChatGPT Plus ($20/mo) | Budget reasoning model, included in Plus |
| Gemini CLI | Flash 2.5 | Free tier | 250 req/day free, adequate for Tier 1-2 |

These defaults are set in `.claude/settings.json` and `.codex/config.toml`. Users with API access can override to Opus/GPT-4o for Tier 3-4 exercises where deeper reasoning helps.

All exercises now have exercise-specific `.meta/hints.md` (3 progressive levels each) and substantive `.meta/notes.md` (why it matters, gotchas, interview follow-ups).

## Sensitivity rules

- **No personal paths or identifiers** in exercise content. A scrub pass was done on the initial commit to remove interviewer names and overly-specific framing. When adding new content, keep the tone generic — refer to "interview prep" rather than any specific company/panel/date.
- **No `.env` files** — nothing here needs secrets.
- **Mirror conventions**: `AGENTS.md` is canonical; `CLAUDE.md` and `GEMINI.md` are thin mirrors. Don't duplicate content across them.

## Repo status

- Created: 2026-04-15
- Origin: extracted from a private interview-prep directory on the day before a senior Python interview; the exercise bank and harness are generic and reusable.
- Current exercise count: 61 (9 tier1 + 11 tier2 + 6 tier3 + 5 tier4 + 10 tier5-easy + 20 tier5-medium)
- All exercise reference solutions validated against tests under Python 3.10
- Multi-agent support: Claude Code (full harness), Codex CLI, Gemini CLI, GitHub Copilot
- Multi-user support: per-user progress, answer submission, peer review gating
