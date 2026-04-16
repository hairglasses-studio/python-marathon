# Marathon Exercise Bank

Standalone pytest-checkable Python exercises designed to be marathoned in order of increasing complexity. Rustlings-for-Python, focused on the patterns that show up in senior-level Python interviews.

## The 90-second pitch

```bash
cd exercises
python marathon.py status          # see where you are
python marathon.py next             # run the next unsolved exercise
# edit tier1_fluency/001_fizzbuzz/problem.py until the tests pass
python marathon.py next             # auto-advance to 002
```

## Golden rule

**Do not look inside `.meta/` until you have passed the tests (or given up).** Local hiding is an honor system — `cat .meta/solution.py` always works — but if you peek before trying, you'll waste the exercise. Use `marathon.py reveal NNN` instead, which gates the reveal behind a confirmation.

## Tiers (31 exercises total)

| Tier | Count | Target time | Focus |
|------|-------|-------------|-------|
| `tier1_fluency/` | 9 | 5-12 min each | Python fluency — FizzBuzz, dicts, decorators, context managers, generators |
| `tier2_patterns/` | 11 | 15-25 min each | Interview primitives — DFS/topo sort, heapq, bisect, threading, retry |
| `tier3_canonical/` | 6 | 45 min each | Full 4-gate problems — spreadsheet, crawler, SQL, warm-ups 1/2/3 |
| `tier4_async/` | 5 | 15-30 min each | asyncio — gather + Semaphore, retry, Queue pipeline, async iterator, tool-call loop |

Tier 3 canonical problems are each full multi-gate exercises (not split by gate). Tier 4 async is hand-written content filling a gap in the source material — every async exercise was validated by running its own reference solution against its tests.

## marathon.py commands

```bash
python marathon.py status                 # Tier progress table + next unsolved
python marathon.py list --tier 1          # List Tier 1 exercises with status
python marathon.py run 001                # Run tests for exercise 001
python marathon.py run --current          # Rerun last-run exercise
python marathon.py next                   # Run the next unsolved exercise
python marathon.py watch [NNN]            # Re-run on file save (polls mtime)
python marathon.py hint 001 --level 1     # Show hint 1 of 3 (records usage)
python marathon.py reveal 001             # Print solution (requires confirm)
python marathon.py reset 001              # Restore original stub, clear progress
```

Progress is cached in `.marathon_progress.json` (gitignored) — tracks status, hints used, first-solved timestamp.

## How each exercise is laid out

```
001_fizzbuzz/
  README.md                # Problem statement, I/O spec, target time, tags
  problem.py               # Stub — the only file you edit
  test_problem.py          # Pytest tests — never edit these
  .meta/
    stub.py                # Original stub (used by `reset`)
    solution.py            # Reference solution
    hints.md               # 3 progressive hints
    notes.md               # Why this matters + pitfalls (optional)
```

Each test file is runnable directly with pytest (`pytest tier1_fluency/001_fizzbuzz/`) if you prefer skipping marathon.py.

## Running without marathon.py

Plain pytest works on a single exercise directory:

```bash
pytest tier1_fluency/001_fizzbuzz/        # Single exercise
```

**Do not run bare `pytest` from the `exercises/` root** — every test file does `from problem import *`, so they collide when pytest discovers multiple exercise directories at once. Always pass an explicit exercise path, or use `marathon.py run NNN` which handles this for you.

## Origin

Tiers 1-3 were bootstrapped from private Jupyter notebooks via `scripts/build_exercises.py` — each exercise's `README.md` retains the source cell range as metadata. Tier 4 async is new hand-written content; all 5 reference solutions were validated against their own tests before being committed.
