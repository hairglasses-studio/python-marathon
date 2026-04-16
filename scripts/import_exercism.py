#!/usr/bin/env python3
"""Import exercises from the Exercism Python track into marathon format.

Usage:
    python scripts/import_exercism.py \\
        --exercism-dir exercism-python \\
        --slugs two-fer,hello-world,bob \\
        --tier tier5_exercism_easy \\
        --dry-run

Expects a local clone of https://github.com/exercism/python.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXERCISES = ROOT / "exercises"
MANIFEST = EXERCISES / "manifest.json"
EX_RE = re.compile(r"^(\d{3})_")


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text())
    return {}


def save_manifest(data: dict) -> None:
    MANIFEST.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def max_exercise_id(manifest: dict) -> int:
    if not manifest:
        return 0
    return max(int(k) for k in manifest)


def slug_to_module(slug: str) -> str:
    """Exercism slug to Python module name: 'two-fer' -> 'two_fer'."""
    return slug.replace("-", "_")


def import_exercise(
    exercism_dir: Path,
    slug: str,
    tier: str,
    next_id: int,
    dry_run: bool,
) -> dict | None:
    """Import one Exercism exercise. Returns manifest entry or None on error."""
    src = exercism_dir / "exercises" / "practice" / slug
    if not src.is_dir():
        print(f"  SKIP {slug}: not found at {src}")
        return None

    module = slug_to_module(slug)
    ex_id = f"{next_id:03d}"
    marathon_slug = f"{ex_id}_{module}"
    dest = EXERCISES / tier / marathon_slug

    # Find source files
    stub_file = src / f"{module}.py"
    test_file = src / f"{module}_test.py"
    solution_file = src / ".meta" / "example.py"
    config_file = src / ".meta" / "config.json"

    if not stub_file.exists():
        print(f"  SKIP {slug}: no stub at {stub_file.name}")
        return None
    if not test_file.exists():
        print(f"  SKIP {slug}: no test at {test_file.name}")
        return None
    if not solution_file.exists():
        print(f"  SKIP {slug}: no solution at .meta/example.py")
        return None

    # Read config for metadata
    config = {}
    if config_file.exists():
        config = json.loads(config_file.read_text())
    blurb = config.get("blurb", slug.replace("-", " ").title())
    difficulty = config.get("difficulty", 0)

    # Read and transform files
    stub_text = stub_file.read_text()
    solution_text = solution_file.read_text()
    test_text = test_file.read_text()

    # Rewrite imports in test file: from <module> import -> from problem import
    test_text = re.sub(
        rf"from\s+{re.escape(module)}\s+import",
        "from problem import",
        test_text,
    )
    # Also handle: import <module>
    test_text = re.sub(
        rf"^import\s+{re.escape(module)}\b",
        "import problem",
        test_text,
        flags=re.MULTILINE,
    )

    # Remove unittest.main() calls — marathon.py uses pytest
    test_text = re.sub(
        r'\nif __name__\s*==\s*["\']__main__["\']\s*:\s*\n\s*unittest\.main\(\)\s*\n?',
        "\n",
        test_text,
    )

    # Generate README
    title = slug.replace("-", " ").title()
    readme = textwrap.dedent(f"""\
        # {title}

        **Tier:** {tier}
        **Target time:** {"10" if difficulty <= 3 else "20" if difficulty <= 6 else "30"} minutes
        **Topics:** exercism, {slug}
        **Source:** exercism/python — {slug}
        **Difficulty:** {difficulty}/10

        ## Problem

        {blurb}

        ## How to run

            python marathon.py run {ex_id}
    """)

    # Generate hints placeholder
    hints = textwrap.dedent(f"""\
        # Hints for {title}

        ## Hint 1

        Read the problem statement carefully and identify the inputs and outputs.

        ## Hint 2

        Think about edge cases — what happens with empty input or boundary values?

        ## Hint 3

        Check the test file for the exact expected behavior and work backward.
    """)

    # Generate notes placeholder
    notes = textwrap.dedent(f"""\
        # Notes for {title}

        ## Why this matters

        This exercise covers fundamental Python concepts tested in interviews.

        ## Source

        Imported from the Exercism Python track ({slug}).
    """)

    if dry_run:
        print(f"  DRY-RUN {ex_id} {marathon_slug} <- exercism:{slug} (difficulty {difficulty})")
        return {
            "slug": marathon_slug,
            "tier": tier,
            "source": "exercism",
            "source_id": slug,
            "source_url": f"https://exercism.org/tracks/python/exercises/{slug}",
            "exercism_difficulty": difficulty,
        }

    # Write files
    dest.mkdir(parents=True, exist_ok=True)
    meta = dest / ".meta"
    meta.mkdir(exist_ok=True)

    (dest / "problem.py").write_text(stub_text)
    (dest / "test_problem.py").write_text(test_text)
    (dest / "README.md").write_text(readme)
    (meta / "stub.py").write_text(stub_text)
    (meta / "solution.py").write_text(solution_text)
    (meta / "hints.md").write_text(hints)
    (meta / "notes.md").write_text(notes)

    print(f"  IMPORTED {ex_id} {marathon_slug} <- exercism:{slug}")
    return {
        "slug": marathon_slug,
        "tier": tier,
        "source": "exercism",
        "source_id": slug,
        "source_url": f"https://exercism.org/tracks/python/exercises/{slug}",
        "exercism_difficulty": difficulty,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Import Exercism exercises into marathon")
    p.add_argument("--exercism-dir", required=True, help="Path to cloned exercism/python repo")
    p.add_argument("--slugs", required=True, help="Comma-separated exercise slugs")
    p.add_argument("--tier", default="tier5_exercism_easy", help="Target tier directory")
    p.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = p.parse_args()

    exercism_dir = Path(args.exercism_dir)
    if not exercism_dir.is_dir():
        print(f"Exercism dir not found: {exercism_dir}")
        return

    slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
    manifest = load_manifest()
    next_id = max_exercise_id(manifest) + 1

    # Check for already-imported slugs
    existing_sources = {v.get("source_id") for v in manifest.values()}
    new_slugs = []
    for slug in slugs:
        if slug in existing_sources:
            print(f"  SKIP {slug}: already imported")
        else:
            new_slugs.append(slug)

    if not new_slugs:
        print("Nothing to import.")
        return

    # Ensure tier dir exists
    tier_dir = EXERCISES / args.tier
    if not args.dry_run:
        tier_dir.mkdir(exist_ok=True)

    print(f"\nImporting {len(new_slugs)} exercises into {args.tier}:\n")
    imported = 0
    for slug in new_slugs:
        entry = import_exercise(exercism_dir, slug, args.tier, next_id, args.dry_run)
        if entry:
            manifest[f"{next_id:03d}"] = entry
            next_id += 1
            imported += 1

    if not args.dry_run and imported > 0:
        save_manifest(manifest)
        print(f"\nDone. Imported {imported} exercises (IDs up to {next_id - 1:03d}).")
        print(f"Manifest updated: {MANIFEST.relative_to(ROOT)}")
    elif args.dry_run:
        print(f"\nDry run complete. Would import {imported} exercises.")
    else:
        print("\nNo exercises imported.")


if __name__ == "__main__":
    main()
