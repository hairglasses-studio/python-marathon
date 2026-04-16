# python-marathon

Marathon-style Python interview prep — standalone pytest-checkable exercises ordered by increasing complexity, with a zero-dependency CLI runner that tracks progress and gates solution reveal.

Built as a rustlings-for-python with an opinionated interview-prep exercise bank.

## Getting started

### 1. Install Python

You need **Python 3.10 or newer** (the async exercises use features from 3.10+).

**macOS** — install via [Homebrew](https://brew.sh):
```bash
brew install python
```

**Linux (Debian/Ubuntu)**:
```bash
sudo apt update && sudo apt install python3 python3-venv python3-pip
```

**Linux (Arch/Manjaro)**:
```bash
sudo pacman -S python
```

**Windows** — download the installer from [python.org](https://www.python.org/downloads/) and check "Add python.exe to PATH" during install.

Verify it works:
```bash
python3 --version   # should print 3.10 or higher
```

> On Windows you may need to use `python` instead of `python3` everywhere below.

### 2. Clone the repo

```bash
git clone git@github.com:hairglasses/python-marathon.git
cd python-marathon
```

### 3. Set up the environment

The only dependency is **pytest**. Create a virtual environment inside the `exercises/` directory:

**Option A — with [uv](https://docs.astral.sh/uv/) (fastest)**:
```bash
cd exercises
uv venv .venv --python 3.10
VIRTUAL_ENV=.venv uv pip install pytest
```

**Option B — with plain pip** (use whichever `python3.10` your system provides):
```bash
cd exercises
python3.10 -m venv .venv
.venv/bin/pip install pytest      # Linux/macOS
# .venv\Scripts\pip install pytest  # Windows
```

### 4. Start drilling

```bash
# See where you are
python marathon.py status

# Start the first exercise
python marathon.py next
```

This opens exercise 001. Read the `README.md` inside the exercise folder, then edit `problem.py` until the tests pass. When you're done:

```bash
python marathon.py next        # auto-advances to the next unsolved exercise
```

That's the whole loop: **read the problem, write the code, run the tests, move on.**

No other dependencies. `marathon.py` is a single-file CLI (25 subcommands) that wraps pytest.

## The golden rule

**Don't look inside `.meta/` until you've passed the tests (or given up.)** Solution hiding on a local filesystem is an honor system — `cat .meta/solution.py` always works — but if you peek before trying, you'll waste the exercise. Use `marathon.py reveal NNN` instead, which gates the reveal behind a confirmation prompt and records that you revealed.

## Tiers (61 exercises)

| Tier | Count | Target time | Focus |
|------|-------|-------------|-------|
| `tier1_fluency/` | 9 | 5-12 min | Python fluency — FizzBuzz, dicts, decorators, context managers, generators |
| `tier2_patterns/` | 11 | 15-25 min | Interview primitives — DFS/topo sort, heapq, bisect, threading, retry |
| `tier3_canonical/` | 6 | 45 min | Full multi-gate problems — spreadsheet evaluator, multithreaded crawler, in-memory SQL, dependency graph, versioned KV store, tool-call retry |
| `tier4_async/` | 5 | 15-30 min | `asyncio` — gather + Semaphore, retry with backoff, Queue pipeline, async iterator protocol, tool-call loop with shared budget |
| `tier5_exercism_easy/` | 10 | 5-10 min | Exercism Python track — easy exercises |
| `tier5_exercism_medium/` | 20 | 10-20 min | Exercism Python track — medium exercises (anagram, binary-search, linked-list, etc.) |

## Commands

```bash
# Core workflow
python marathon.py status                # Progress, XP, streak, heatmap
python marathon.py next                  # Run next unsolved exercise
python marathon.py run NNN               # Run tests for exercise NNN
python marathon.py run --current         # Rerun last-run exercise
python marathon.py list [--tier N]       # List exercises with status
python marathon.py watch [NNN]           # Re-run on file save (polls mtime)
python marathon.py challenge [--tier N]  # Random unsolved exercise
python marathon.py kata NNN              # Re-solve from scratch

# Hints and solutions
python marathon.py hint NNN --level 1    # Show hint 1 of 3 (records usage)
python marathon.py reveal NNN            # Print solution (requires typing REVEAL NNN)
python marathon.py reset NNN             # Restore original stub, clear progress

# Collaboration
python marathon.py submit NNN [--git]    # Save solution to answers/ (--git auto-commits)
python marathon.py peer NNN --user NAME  # View peer's answer (gated on your own solve)
python marathon.py challenge-peer NNN --user NAME  # Create timed challenge

# Discovery and review
python marathon.py tag [--filter TOPIC]  # List/search tags across exercises
python marathon.py recommend             # Suggest next exercises by tag coverage
python marathon.py review                # SM-2 spaced repetition queue
python marathon.py badges                # Show earned achievements

# Export and import
python marathon.py export                # Export progress JSON to stdout
python marathon.py import-progress FILE  # Merge progress from another machine
python marathon.py export-obsidian --vault PATH  # Export to Obsidian markdown

# Admin
python marathon.py verify                # Run all reference solutions — health check
python marathon.py lint-exercises        # Validate exercise file layout
python marathon.py new --name SLUG       # Scaffold a new exercise
python marathon.py import --slugs S      # Import Exercism exercises
python marathon.py completion zsh        # Generate shell completion
```

Progress is cached in `.marathon_progress.json` (gitignored, per-user namespaced) — tracks status, hints used, first-solved timestamp per exercise.

Set your identity (for multi-user features):
```bash
echo "yourname" > exercises/.marathon_user
```

## Exercise anatomy

```
001_fizzbuzz/
  README.md                # Problem statement, I/O spec, target time, topic tags
  problem.py               # Stub — the only file you edit
  test_problem.py          # Pytest tests — never edit these
  .meta/
    stub.py                # Original stub snapshot (for reset)
    solution.py            # Reference solution
    hints.md               # 3 progressive hints
    notes.md               # Why it matters + pitfalls (optional)
```

Each `test_problem.py` can also be run directly with bare pytest:

```bash
pytest exercises/tier1_fluency/001_fizzbuzz/
```

## Adding new exercises

Two paths:

**Hand-written** (for new content): create a new numbered directory under the right tier, drop in the 7 files following the template above. See `exercises/tier4_async/` for examples — all 5 async exercises are hand-written and validated.

**From a Jupyter notebook**: `scripts/build_exercises.py` is a one-shot converter that reads scaffold/test/solution triplet cells and materializes exercise directories. See the docstring for the ExerciseSpec format. The script in this repo was originally run against notebooks in a private prep repo — adapt the `NOTEBOOKS` dict and `SPECS` list for your own source.

## Using with AI tutors

This repo supports **Claude Code**, **Codex CLI**, **Gemini CLI**, and **GitHub Copilot** as interactive tutors. All four follow the same contract: Socratic-first, never reveal solutions unprompted, only edit `problem.py`.

### Claude Code (full harness enforcement)

`.claude/settings.json` enforces deny rules — Claude cannot read solutions even if asked. 13 slash commands are available:

| Command | What it does |
|---------|-------------|
| `/status` | Show marathon progress across all tiers |
| `/list [--tier N]` | List all exercises with status and tier |
| `/next` | Start tutoring on the next unsolved exercise |
| `/run [NNN]` | Run tests; Socratic help on failure |
| `/hint [NNN] [level]` | Exercise-specific hint at level 1-3 (no spoilers) |
| `/reflect [NNN]` | Post-solve reflection: patterns, code review, interview follow-ups |
| `/review` | Spaced repetition: suggest exercises to revisit |
| `/reveal NNN` | Double-gated solution reveal (interactive confirmation) |
| `/reset NNN` | Restore `problem.py` to the original stub |
| `/verify` | Run all reference solutions against tests |
| `/submit NNN` | Commit your answer to the shared answers directory |
| `/peer NNN` | View partner's answer (gated on your own solve) |
| `/pull-questions` | Import new exercises from Exercism |

To get started:

```bash
claude                  # launch Claude Code from the repo root
/next                   # begin the first exercise
```

### Codex CLI / Gemini CLI

Both use behavioral tutor contracts via `AGENTS.md` (no harness-level deny rules). Use `marathon.py` subcommands directly instead of slash commands:

```bash
codex                   # or: gemini
# then ask: "run marathon.py next" or "help me with exercise 001"
```

### Recommended models ($20/mo plans)

| Tool | Default model | Plan |
|------|--------------|------|
| Claude Code | Sonnet 4.6 | Claude Pro ($20/mo) |
| Codex CLI | o3-mini | ChatGPT Plus ($20/mo) |
| Gemini CLI | Flash 2.5 | Free tier |

These defaults are set in `.claude/settings.json` and `.codex/config.toml`.

## Shell completion

Generate zsh tab-completion for all marathon.py subcommands:

```bash
# One-time setup
python marathon.py completion zsh > ~/.zfunc/_marathon

# Or install system-wide
sudo python marathon.py completion zsh > /usr/local/share/zsh/site-functions/_marathon
```

Bash completion is also available: `marathon.py completion bash > ~/.local/share/bash-completion/completions/marathon`.

A man page is available at `man/marathon.1` (generate with `make man`).

## Origin

Originally extracted from 4 Jupyter notebooks in a private interview-prep directory. The notebook-sourced exercises (tiers 1-3) were generated by `scripts/build_exercises.py`; Tier 4 async is hand-written content filling a gap in the source material. All Tier 4 reference solutions were validated against their own tests.

See `AGENTS.md` for repo conventions and development notes.

## License

MIT — see `LICENSE`.
