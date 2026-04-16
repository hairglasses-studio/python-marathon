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

No other dependencies. `marathon.py` is a single ~280-line file that wraps pytest.

## The golden rule

**Don't look inside `.meta/` until you've passed the tests (or given up.)** Solution hiding on a local filesystem is an honor system — `cat .meta/solution.py` always works — but if you peek before trying, you'll waste the exercise. Use `marathon.py reveal NNN` instead, which gates the reveal behind a confirmation prompt and records that you revealed.

## Tiers (31 exercises total)

| Tier | Count | Target time | Focus |
|------|-------|-------------|-------|
| `tier1_fluency/` | 9 | 5-12 min | Python fluency — FizzBuzz, dicts, decorators, context managers, generators |
| `tier2_patterns/` | 11 | 15-25 min | Interview primitives — DFS/topo sort, heapq, bisect, threading, retry |
| `tier3_canonical/` | 6 | 45 min | Full multi-gate problems — spreadsheet evaluator, multithreaded crawler, in-memory SQL, dependency graph, versioned KV store, tool-call retry |
| `tier4_async/` | 5 | 15-30 min | `asyncio` — gather + Semaphore, retry with backoff, Queue pipeline, async iterator protocol, tool-call loop with shared budget |

## Commands

```bash
python marathon.py status                # Tier progress table + next unsolved
python marathon.py list [--tier N]       # List exercises with status
python marathon.py run NNN               # Run tests for exercise NNN
python marathon.py run --current         # Rerun last-run exercise
python marathon.py next                  # Run the next unsolved exercise
python marathon.py watch [NNN]           # Re-run on file save (polls mtime)
python marathon.py hint NNN --level 1    # Show hint 1 of 3 (records usage)
python marathon.py reveal NNN            # Print solution (requires typing REVEAL NNN)
python marathon.py reset NNN             # Restore original stub, clear progress
```

Progress is cached in `.marathon_progress.json` (gitignored) — tracks status, hints used, first-solved timestamp per exercise.

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

## Using with Claude Code

This repo ships with a `.claude/` configuration that turns Claude Code into an interactive tutor. When you launch a Claude Code session from the repo root, the harness enforces learning-mode rules automatically:

- **Solution hiding is technically enforced.** `.claude/settings.json` denies `Read` on `.meta/solution.py` and `.meta/stub.py`, so Claude cannot peek at answers even if you ask it to.
- **Write scope is locked to `problem.py`.** Claude can only edit the stub files you're meant to work on — tests, the runner, and `.meta/` are read-only.
- **Socratic tutor posture.** Claude is instructed to ask guiding questions before writing code, and to generate exercise-specific hints from the problem spec rather than giving away the answer.

Nine slash commands are available inside Claude Code:

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

To get started:

```bash
claude                  # launch Claude Code from the repo root
/next                   # begin the first exercise
```

## Origin

Originally extracted from 4 Jupyter notebooks in a private interview-prep directory. The notebook-sourced exercises (tiers 1-3) were generated by `scripts/build_exercises.py`; Tier 4 async is hand-written content filling a gap in the source material. All Tier 4 reference solutions were validated against their own tests.

See `AGENTS.md` for repo conventions and development notes.

## License

MIT — see `LICENSE`.
