# Contributing to python-marathon

## Adding a new exercise

### Quick way (scaffold generator)

```bash
cd exercises
python marathon.py new --name "sliding_window_max" --tier tier2_patterns \
  --tags "deque,sliding-window" --target-minutes 20
```

This creates the full 7-file directory and updates `manifest.json`. Then edit:
1. `problem.py` — typed signature + `raise NotImplementedError("fill me in")`
2. `test_problem.py` — pytest cases ordered trivial -> edge -> adversarial
3. `.meta/solution.py` — reference answer
4. `README.md` — problem statement, I/O spec, target time
5. `.meta/hints.md` — 3 progressive hints (`## Hint 1`, `## Hint 2`, `## Hint 3`)
6. `.meta/notes.md` — why it matters, pitfalls, interview follow-ups

### Validate your exercise

```bash
# Temporarily swap in your solution to verify tests pass
cp .meta/solution.py problem.py
python marathon.py run NNN
python marathon.py reset NNN

# Run the linter
python marathon.py lint-exercises
```

### Importing from Exercism

```bash
# Clone Exercism Python track (one-time)
git clone --depth 1 https://github.com/exercism/python.git exercism-python

# Import specific exercises
python marathon.py import --exercism-dir ../exercism-python \
  --slugs anagram,binary-search --tier tier5_exercism_medium

# Verify imported exercises
python marathon.py verify
```

### Generating tests from problem-specifications

```bash
# Clone problem-specifications (one-time)
git clone --depth 1 https://github.com/exercism/problem-specifications.git

# Generate test file
python scripts/generate_from_specs.py --specs-dir problem-specifications \
  --slug leap --output exercises/tier5_exercism_easy/039_leap/test_problem.py
```

## Exercise format

Every exercise follows the 7-file layout:

```
NNN_slug/
  README.md           # Problem statement
  problem.py          # Stub — the only file the learner edits
  test_problem.py     # Pytest tests — `from problem import *`
  .meta/
    stub.py           # Original stub snapshot (for reset)
    solution.py       # Reference solution
    hints.md          # 3 progressive hints
    notes.md          # Why it matters + pitfalls
```

## Conventions

- **Numbering**: globally monotone 3-digit IDs (001, 002, ..., 061, ...)
- **Test style**: one `def test_all():` or individual `def test_*()` functions
- **Imports**: always `from problem import *` in test files
- **Deterministic**: no random seeds beyond `conftest.py`'s `random.seed(42)` fixture
- **No bare pytest**: use `marathon.py run NNN` (namespace isolation)

## Running the full test suite

```bash
python marathon.py verify     # Runs all 61+ reference solutions
python marathon.py lint-exercises  # Validates file layout
python marathon.py verify --changed-only  # Only exercises with changed files
```

## Pre-commit hook

Install the pre-commit hook to verify changed exercises before every commit:

```bash
cp scripts/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

This runs `marathon.py verify --changed-only` automatically.

## Multi-user workflow

```bash
echo "yourname" > exercises/.marathon_user
python marathon.py submit NNN --git    # Commit solution
python marathon.py peer NNN --user NAME  # View peer's answer (gated)
```
