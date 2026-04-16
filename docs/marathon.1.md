% MARATHON(1) python-marathon | Marathon Exercise Runner
% python-marathon contributors
% April 2026

# NAME

marathon - Python interview prep exercise runner

# SYNOPSIS

**python marathon.py** *command* [*options*]

# DESCRIPTION

Marathon is a rustlings-for-python style exercise runner for Python interview
prep. It wraps pytest with progress tracking, hint gating, solution reveal,
multi-user answer sharing, and Exercism exercise importing.

Exercises live in numbered directories under tier folders. Each exercise has a
stub (*problem.py*), tests (*test_problem.py*), and reference solution
(*.meta/solution.py*). The learner edits *problem.py* until the tests pass.

# COMMANDS

**status**
:   Show per-tier progress table and the next unsolved exercise.

**list** [**--tier** *N*]
:   List all exercises with tier, status, and name. Filter by tier number.

**run** *NNN* [**--current**]
:   Run pytest on exercise *NNN*. Use **--current** to rerun the last exercise.

**next**
:   Find and run the next unsolved exercise.

**watch** [*NNN*]
:   Watch *problem.py* for changes and rerun tests automatically. Polls every
    second. Falls back to last-run or next unsolved if no ID given.

**hint** *NNN* **--level** *N*
:   Show hint at level 1-3 for exercise *NNN*. Records usage in progress.

**reveal** *NNN*
:   Print the reference solution. Requires typing `REVEAL NNN` to confirm.

**reset** *NNN*
:   Restore *problem.py* to its original stub and clear progress for the exercise.

**submit** *NNN* [**--git**]
:   Copy your passing *problem.py* to *answers/<user>/NNN/solution.py*. With
    **--git**, also runs *git add* and *git commit*.

**peer** *NNN* **--user** *NAME*
:   View another user's submitted answer. Gated: you must have solved the
    exercise yourself first.

**verify**
:   Run all reference solutions against their tests silently. Reports a
    pass/fail summary. Does not modify learner progress.

**review**
:   Suggest 1-3 exercises to revisit based on hint usage, reveal history, and
    time since first solve.

**import** **--slugs** *S* [**--exercism-dir** *PATH*] [**--tier** *T*] [**--dry-run**]
:   Import exercises from a cloned Exercism Python track. Converts stubs, tests,
    and solutions to marathon format. Assigns monotone IDs.

**completion** {**bash**,**zsh**}
:   Generate a shell completion script. Pipe to a file:
    `marathon.py completion zsh > ~/.zfunc/_marathon`

# ENVIRONMENT

**.marathon_user**
:   Plain text file in *exercises/* containing the user's name (e.g., `mitch`).
    Used to namespace progress and answer submission. Gitignored.

**.marathon_progress.json**
:   JSON progress cache in *exercises/*. Namespaced by user. Gitignored.
    Tracks status, hints used, first-solved timestamp, and reveal history.

# EXERCISE FORMAT

Each exercise directory contains:

    NNN_slug/
      README.md           Problem statement
      problem.py          Stub (learner edits this)
      test_problem.py     Pytest tests (read-only)
      .meta/
        stub.py           Original stub snapshot
        solution.py       Reference solution
        hints.md          3 progressive hints
        notes.md          Why it matters + pitfalls

# SEE ALSO

**pytest**(1), **exercism**(1)

The full documentation is in the repository README.md.
