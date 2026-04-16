% MARATHON(1) python-marathon | Marathon Exercise Runner
% python-marathon contributors
% April 2026

# NAME

marathon - Python interview prep exercise runner (25 subcommands)

# SYNOPSIS

**python marathon.py** *command* [*options*]

# DESCRIPTION

Marathon is a rustlings-for-python style exercise runner for Python interview
prep. It wraps pytest with progress tracking, SM-2 spaced repetition, badge
achievements, multi-user answer sharing, and Exercism exercise importing.

Exercises live in numbered directories under tier folders. Each exercise has a
stub (*problem.py*), tests (*test_problem.py*), and reference solution
(*.meta/solution.py*). The learner edits *problem.py* until the tests pass.

# CORE WORKFLOW

**status**
:   Show per-tier progress, XP level, streak count, earned badges, and a
    12-week activity heatmap.

**next**
:   Find and run the next unsolved exercise.

**run** *NNN* [**--current**]
:   Run pytest on exercise *NNN*. Use **--current** to rerun the last exercise.
    Supports 2D addressing: `run "tier2 3"` runs the 3rd tier2 exercise.

**list** [**--tier** *N*]
:   List all exercises with tier, status, and name. Filter by tier number.

**watch** [*NNN*]
:   Watch *problem.py* for changes and rerun tests automatically. Polls every
    second.

**challenge** [**--tier** *N*]
:   Pick a random unsolved exercise, optionally filtered by tier.

**kata** *NNN*
:   Re-solve an exercise from scratch. Backs up current solution, restores the
    stub, and tracks repetition count.

# HINTS AND SOLUTIONS

**hint** *NNN* **--level** *N*
:   Show hint at level 1-3 for exercise *NNN*. Records usage in progress.

**reveal** *NNN*
:   Print the reference solution. Requires typing `REVEAL NNN` to confirm.

**reset** *NNN*
:   Restore *problem.py* to its original stub and clear progress.

# COLLABORATION

**submit** *NNN* [**--git**]
:   Copy your passing *problem.py* to *answers/<user>/NNN/solution.py*. With
    **--git**, also runs *git add* and *git commit*.

**peer** *NNN* **--user** *NAME*
:   View another user's submitted answer. Gated: you must have solved the
    exercise yourself first.

**challenge-peer** *NNN* **--user** *NAME*
:   Create a timed challenge with a peer. Stored in *answers/challenges.json*.

# DISCOVERY AND REVIEW

**tag** [**--filter** *TOPIC*]
:   Without **--filter**: list all tags with exercise counts. With **--filter**:
    show exercises matching the topic tag.

**recommend**
:   Suggest next exercises based on tag coverage (most new tags first).

**review**
:   SM-2 spaced repetition queue. Shows exercises due for review with easiness
    factors and overdue status.

**badges**
:   Show all earned and available badges with descriptions.

# EXPORT AND IMPORT

**export**
:   Dump progress JSON to stdout for backup or cross-machine sync.

**import-progress** *FILE*
:   Merge progress from a JSON file. Takes max status, unions badges, preserves
    SR fields.

**export-obsidian** **--vault** *PATH*
:   Export solved exercises to an Obsidian vault as markdown notes with YAML
    frontmatter.

# ADMIN

**verify**
:   Run all reference solutions against their tests silently. Reports pass/fail
    summary. Does not modify learner progress.

**lint-exercises**
:   Validate all exercises have the required 7-file layout, correct test
    imports, and stub content.

**new** **--name** *SLUG* [**--tier** *T*] [**--tags** *T1,T2*] [**--target-minutes** *N*]
:   Scaffold a new exercise directory with all 7 files and add a manifest entry.

**import** **--slugs** *S* [**--exercism-dir** *PATH*] [**--tier** *T*] [**--dry-run**]
:   Import exercises from a cloned Exercism Python track.

**completion** {**bash**,**zsh**}
:   Generate a shell completion script.

# ENVIRONMENT

**.marathon_user**
:   Plain text file in *exercises/* containing the user's name (e.g., `mitch`).
    Used to namespace progress and answer submission. Gitignored.

**.marathon_progress.json**
:   JSON progress cache in *exercises/*. Per-user namespaced. Tracks status,
    hints used, first-solved timestamp, solve duration, SM-2 scheduling fields,
    streak, badges, and kata count. Gitignored.

**manifest.json**
:   Exercise metadata in *exercises/*. Maps exercise IDs to slug, tier, source,
    tags, difficulty, and target minutes.

**badges.json**
:   Badge specifications in *exercises/*. Defines 16 achievements with slugs,
    names, and descriptions.

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
