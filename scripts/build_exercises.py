#!/usr/bin/env python3
"""build_exercises.py — one-shot converter from notebook cells to exercise dirs.

HISTORICAL. This script was originally run against Jupyter notebooks in a
private interview-prep directory to bootstrap the 26 notebook-sourced
exercises now checked into `exercises/`. Those notebooks are NOT in this
repo — the script is kept as a reference for how to add more exercises
from your own Jupyter material.

To adapt for your own notebooks:
1. Place notebooks adjacent to this script or update the `ROOT` path.
2. Edit the `SPECS` list to map notebook cell indices to target tiers/slugs.
3. Each spec needs: tier, slug, title, notebook path, md/scaffold/test/solution
   cell indices, topic tags, target minutes.
4. Use `prelude_cell` if your exercise has a separate "shapes" cell with
   dataclasses or exceptions that both the stub and solution need.

Reads notebooks that follow the scaffold/test/solution triplet pattern:
the scaffold cell contains a typed signature + `raise NotImplementedError`,
the test cell contains loose `assert` statements, and the solution cell
contains the reference implementation.

Test cells are wrapped in a single `def test_all():` function — losing
per-case granularity, but pytest still reports the failing assert line.
"""

from __future__ import annotations

import json
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXERCISES = ROOT / "exercises"


@dataclass
class ExerciseSpec:
    tier: str
    slug: str
    title: str
    notebook: str
    md_cell: int
    scaffold_cell: int
    test_cell: int
    solution_cell: int
    topic_tags: list[str]
    target_minutes: int
    prelude_cell: int | None = None  # extra "shapes" cell prepended to problem + solution


NOTEBOOKS: dict[str, dict] = {}


def load_notebook(path: str) -> dict:
    if path not in NOTEBOOKS:
        with (ROOT / path).open() as f:
            NOTEBOOKS[path] = json.load(f)
    return NOTEBOOKS[path]


def cell_source(notebook_path: str, idx: int) -> str:
    nb = load_notebook(notebook_path)
    return "".join(nb["cells"][idx]["source"])


def extract_problem_statement(md_source: str) -> str:
    """Keep everything after the heading line, trim to the first '---' or EOF."""
    lines = md_source.split("\n")
    out = []
    for line in lines:
        if line.strip() == "---":
            break
        out.append(line)
    return "\n".join(out).strip()


def wrap_tests_in_function(test_source: str) -> str:
    # Wrap the whole test cell in one pytest function — pytest captures stdout
    # so leftover print() noise is only visible on failures, which is fine.
    body = textwrap.indent(test_source.strip(), "    ")
    return "def test_all():\n" + body + "\n"


def strip_solution_label(code: str) -> str:
    # Strip a leading "# Reference solution" comment or solution-marker docstring.
    lines = code.split("\n")
    while lines and (
        lines[0].strip().startswith("# Reference solution")
        or lines[0].strip().startswith("# Reference")
        or re.match(r'^\s*"""[^"]*(solution|REFERENCE)[^"]*"""', lines[0], re.I)
    ):
        lines = lines[1:]
    return "\n".join(lines).lstrip()


def strip_exercise_label(code: str) -> str:
    # Strip a leading triple-quoted docstring that contains "EXERCISE".
    m = re.match(r'^\s*"""[^"]*(EXERCISE|exercise)[^"]*"""\s*\n', code, re.S)
    if m:
        code = code[m.end():]
    return code.lstrip("\n")


def write_exercise(spec: ExerciseSpec) -> Path:
    tier_dir = EXERCISES / spec.tier
    ex_dir = tier_dir / spec.slug
    meta_dir = ex_dir / ".meta"
    meta_dir.mkdir(parents=True, exist_ok=True)

    md_src = cell_source(spec.notebook, spec.md_cell)
    scaffold_src = cell_source(spec.notebook, spec.scaffold_cell)
    test_src = cell_source(spec.notebook, spec.test_cell)
    solution_src = cell_source(spec.notebook, spec.solution_cell)

    statement = extract_problem_statement(md_src)
    scaffold_clean = strip_exercise_label(scaffold_src)
    solution_clean = strip_solution_label(solution_src)
    tests_clean = test_src.strip()

    if spec.prelude_cell is not None:
        prelude = strip_exercise_label(cell_source(spec.notebook, spec.prelude_cell))

        def _merge_future_imports(prelude: str, body: str) -> str:
            # __future__ imports must be at the top — strip them from body when merging
            body_lines = body.split("\n")
            cleaned = [ln for ln in body_lines if not ln.lstrip().startswith("from __future__")]
            return prelude.rstrip() + "\n\n\n" + "\n".join(cleaned).lstrip()

        scaffold_clean = _merge_future_imports(prelude, scaffold_clean)
        solution_clean = _merge_future_imports(prelude, solution_clean)

    # problem.py — the scaffold as-is
    (ex_dir / "problem.py").write_text(scaffold_clean)
    # .meta/stub.py — snapshot for reset
    (meta_dir / "stub.py").write_text(scaffold_clean)
    # .meta/solution.py — reference
    (meta_dir / "solution.py").write_text(solution_clean)

    # test_problem.py — wrap the test cell
    test_wrapped = wrap_tests_in_function(tests_clean)
    test_file = (
        "# Tests — do not edit. Run via:\n"
        "#   python marathon.py run NNN\n"
        "#   pytest " + str(ex_dir.relative_to(EXERCISES)) + "/\n\n"
        "from problem import *  # noqa: F401,F403\n\n" + test_wrapped
    )
    (ex_dir / "test_problem.py").write_text(test_file)

    # README.md
    readme = (
        f"# {spec.title}\n\n"
        f"**Tier:** {spec.tier}  \n"
        f"**Target time:** {spec.target_minutes} minutes  \n"
        f"**Topics:** {', '.join(spec.topic_tags)}  \n"
        f"**Source:** `{spec.notebook}` cells {spec.md_cell}-{spec.solution_cell}\n\n"
        f"## Problem\n\n{statement}\n\n"
        f"## How to run\n\n"
        f"```bash\n"
        f"python marathon.py run {spec.slug.split('_')[0]}\n"
        f"```\n\n"
        f"Edit `problem.py`. When `test_problem.py` passes, move on.\n"
    )
    (ex_dir / "README.md").write_text(readme)

    # .meta/hints.md — empty template
    hints_template = (
        f"# Hints for {spec.title}\n\n"
        "## Hint 1\n\nThink about the core data structure or pattern first. "
        "What's the right Python primitive for this problem?\n\n"
        "## Hint 2\n\nSketch the control flow on paper before typing. "
        "What's the happy path? What edge cases matter?\n\n"
        "## Hint 3\n\nIf still stuck, review the Python stdlib module most relevant "
        "to this problem — it often has the exact primitive you need.\n"
    )
    (meta_dir / "hints.md").write_text(hints_template)

    # .meta/notes.md — minimal placeholder
    (meta_dir / "notes.md").write_text(
        f"# Notes for {spec.title}\n\n"
        f"Referenced in `{spec.notebook}`. See the original notebook for the full "
        f"explanation and context around this exercise.\n"
    )

    return ex_dir


# === Exercise specs ==========================================================

SPECS: list[ExerciseSpec] = [
    # ----- Tier 1 — from openai-python-refresher.ipynb -----
    ExerciseSpec(
        tier="tier1_fluency",
        slug="001_fizzbuzz",
        title="FizzBuzz",
        notebook="openai-python-refresher.ipynb",
        md_cell=16, scaffold_cell=17, test_cell=18, solution_cell=19,
        topic_tags=["control-flow", "modulo"],
        target_minutes=5,
    ),
    ExerciseSpec(
        tier="tier1_fluency",
        slug="002_word_frequency",
        title="Word Frequency Counter",
        notebook="openai-python-refresher.ipynb",
        md_cell=29, scaffold_cell=30, test_cell=31, solution_cell=32,
        topic_tags=["dict", "string", "counting"],
        target_minutes=10,
    ),
    ExerciseSpec(
        tier="tier1_fluency",
        slug="003_windowed_generator",
        title="Windowed Generator",
        notebook="openai-python-refresher.ipynb",
        md_cell=40, scaffold_cell=41, test_cell=42, solution_cell=43,
        topic_tags=["generator", "deque", "typing"],
        target_minutes=10,
    ),
    ExerciseSpec(
        tier="tier1_fluency",
        slug="004_counted_decorator",
        title="Call-Counter Decorator",
        notebook="openai-python-refresher.ipynb",
        md_cell=51, scaffold_cell=52, test_cell=53, solution_cell=54,
        topic_tags=["decorator", "closure", "functools.wraps"],
        target_minutes=10,
    ),
    ExerciseSpec(
        tier="tier1_fluency",
        slug="005_int_range",
        title="IntRange Class",
        notebook="openai-python-refresher.ipynb",
        md_cell=66, scaffold_cell=67, test_cell=68, solution_cell=69,
        topic_tags=["OOP", "dunders", "iteration-protocol"],
        target_minutes=12,
    ),
    ExerciseSpec(
        tier="tier1_fluency",
        slug="006_config_parser",
        title="Typed Config Parser",
        notebook="openai-python-refresher.ipynb",
        md_cell=75, scaffold_cell=76, test_cell=77, solution_cell=78,
        topic_tags=["exception-hierarchy", "string-parsing"],
        target_minutes=12,
    ),
    ExerciseSpec(
        tier="tier1_fluency",
        slug="007_topn_tracker",
        title="Top-N Tracker",
        notebook="openai-python-refresher.ipynb",
        md_cell=95, scaffold_cell=96, test_cell=97, solution_cell=98,
        topic_tags=["heapq", "min-heap"],
        target_minutes=12,
    ),
    ExerciseSpec(
        tier="tier1_fluency",
        slug="008_temp_attr_context",
        title="Temporary Attribute Override",
        notebook="openai-python-refresher.ipynb",
        md_cell=104, scaffold_cell=105, test_cell=106, solution_cell=107,
        topic_tags=["context-manager", "contextlib", "sentinel"],
        target_minutes=10,
    ),
    ExerciseSpec(
        tier="tier1_fluency",
        slug="009_parallel_sum",
        title="Parallel Sum with ThreadPoolExecutor",
        notebook="openai-python-refresher.ipynb",
        md_cell=117, scaffold_cell=118, test_cell=119, solution_cell=120,
        topic_tags=["threading", "ThreadPoolExecutor", "chunking"],
        target_minutes=12,
    ),

    # ----- Tier 2 — from openai-primitives-refresher.ipynb -----
    ExerciseSpec(
        tier="tier2_patterns",
        slug="010_dfs_traversal",
        title="Depth-First Search (Pre-order)",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=6, scaffold_cell=7, test_cell=8, solution_cell=9,
        topic_tags=["graph", "DFS", "recursion"],
        target_minutes=15,
    ),
    ExerciseSpec(
        tier="tier2_patterns",
        slug="011_topo_sort_kahn",
        title="Topological Sort (Kahn's Algorithm)",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=10, scaffold_cell=11, test_cell=12, solution_cell=13,
        topic_tags=["graph", "BFS", "in-degree"],
        target_minutes=20,
    ),
    ExerciseSpec(
        tier="tier2_patterns",
        slug="012_three_color_cycle",
        title="Three-Color Cycle Detection",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=14, scaffold_cell=15, test_cell=16, solution_cell=17,
        topic_tags=["graph", "DFS", "state-coloring"],
        target_minutes=20,
    ),
    ExerciseSpec(
        tier="tier2_patterns",
        slug="013_transitive_dependents",
        title="Transitive Dependents (Cache Invalidation)",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=18, scaffold_cell=19, test_cell=20, solution_cell=21,
        topic_tags=["graph", "reverse-BFS", "defaultdict"],
        target_minutes=20,
    ),
    ExerciseSpec(
        tier="tier2_patterns",
        slug="014_content_addressed_cache",
        title="Content-Addressed Cache",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=25, scaffold_cell=26, test_cell=27, solution_cell=28,
        topic_tags=["hashlib", "caching", "sha256"],
        target_minutes=20,
    ),
    ExerciseSpec(
        tier="tier2_patterns",
        slug="015_time_travel_ledger",
        title="Time-Travel KV Ledger",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=35, scaffold_cell=36, test_cell=37, solution_cell=38,
        topic_tags=["bisect", "defaultdict", "cumulative-sum"],
        target_minutes=20,
    ),
    ExerciseSpec(
        tier="tier2_patterns",
        slug="016_per_key_locking",
        title="Per-Key Locking (KeyedLocker)",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=44, scaffold_cell=45, test_cell=46, solution_cell=47,
        topic_tags=["threading", "Lock", "contextmanager"],
        target_minutes=20,
    ),
    ExerciseSpec(
        tier="tier2_patterns",
        slug="017_budget_retry",
        title="Budget-Aware Retry with Exponential Backoff",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=61, scaffold_cell=62, test_cell=63, solution_cell=64,
        topic_tags=["retry", "backoff", "jitter", "exceptions"],
        target_minutes=25,
    ),
    ExerciseSpec(
        tier="tier2_patterns",
        slug="018_gpu_credit_manager",
        title="GPU Credit Manager with Expiry",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=71, scaffold_cell=72, test_cell=73, solution_cell=74,
        topic_tags=["heapq", "expiry", "lazy-eviction"],
        target_minutes=25,
    ),
    ExerciseSpec(
        tier="tier2_patterns",
        slug="019_path_normalize",
        title="Stack-Based Path Normalization",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=75, scaffold_cell=76, test_cell=77, solution_cell=78,
        topic_tags=["stack", "string-processing"],
        target_minutes=20,
    ),
    ExerciseSpec(
        tier="tier2_patterns",
        slug="020_resumable_iterator",
        title="Resumable List Iterator",
        notebook="openai-primitives-refresher.ipynb",
        md_cell=79, scaffold_cell=80, test_cell=81, solution_cell=82,
        topic_tags=["iteration-protocol", "state-serialization"],
        target_minutes=20,
    ),

    # ----- Tier 3 — from openai-extra-problems.ipynb -----
    ExerciseSpec(
        tier="tier3_canonical",
        slug="021_spreadsheet_formula",
        title="Spreadsheet Formula Evaluator",
        notebook="openai-extra-problems.ipynb",
        md_cell=1, scaffold_cell=2, test_cell=3, solution_cell=4,
        topic_tags=["graph", "DAG", "lazy-eval", "regex"],
        target_minutes=45,
    ),
    ExerciseSpec(
        tier="tier3_canonical",
        slug="022_multithreaded_crawler",
        title="Multithreaded Web Crawler",
        notebook="openai-extra-problems.ipynb",
        md_cell=5, scaffold_cell=6, test_cell=7, solution_cell=8,
        topic_tags=["threading", "BFS", "ThreadPoolExecutor", "graceful-shutdown"],
        target_minutes=45,
    ),
    ExerciseSpec(
        tier="tier3_canonical",
        slug="023_in_memory_sql",
        title="In-Memory SQL Database",
        notebook="openai-extra-problems.ipynb",
        md_cell=9, scaffold_cell=10, test_cell=11, solution_cell=12,
        topic_tags=["data-modeling", "filtering", "sorting", "Callable"],
        target_minutes=45,
    ),

    # ----- Tier 3 — Canonical warm-ups from openai-devprod-2026-04-16.ipynb -----
    # These are the 3 high-value 4-gate warm-up problems mirroring real OpenAI coding rounds.
    ExerciseSpec(
        tier="tier3_canonical",
        slug="024_dep_graph_warmup",
        title="Dependency Graph with Incremental Invalidation (Warm-up 1)",
        notebook="openai-devprod-2026-04-16.ipynb",
        md_cell=14, scaffold_cell=15, test_cell=16, solution_cell=17,
        topic_tags=["graph", "hashing", "threading", "invalidation", "4-gate"],
        target_minutes=45,
    ),
    ExerciseSpec(
        tier="tier3_canonical",
        slug="025_versioned_kv_warmup",
        title="Versioned Key-Value Store (Warm-up 2)",
        notebook="openai-devprod-2026-04-16.ipynb",
        md_cell=18, scaffold_cell=19, test_cell=20, solution_cell=21,
        topic_tags=["bisect", "time-travel", "snapshot-isolation", "threading", "4-gate"],
        target_minutes=45,
    ),
    ExerciseSpec(
        tier="tier3_canonical",
        slug="026_tool_retry_warmup",
        title="Tool-Call Loop with Retry + Budget (Warm-up 3)",
        notebook="openai-devprod-2026-04-16.ipynb",
        md_cell=22, scaffold_cell=24, test_cell=25, solution_cell=26,
        prelude_cell=23,  # shapes (dataclasses + exceptions)
        topic_tags=["retry", "backoff", "dataclass", "exception-hierarchy", "4-gate"],
        target_minutes=45,
    ),
]


def main() -> None:
    for spec in SPECS:
        path = write_exercise(spec)
        print(f"✓ {spec.tier}/{spec.slug}  →  {path}")
    print(f"\nTotal: {len(SPECS)} exercises materialized")


if __name__ == "__main__":
    main()
