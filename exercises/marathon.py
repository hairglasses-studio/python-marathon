#!/usr/bin/env python3
"""marathon.py — interview prep exercise runner.

Usage:
    python marathon.py status                 # Progress + next unsolved
    python marathon.py run 001                # Run tests for exercise 001
    python marathon.py run --current          # Rerun last-run exercise
    python marathon.py next                   # Run next unsolved
    python marathon.py watch [NNN]            # Re-run on file save
    python marathon.py hint 001 --level 1     # Show hint level 1-3
    python marathon.py reveal 001             # Print solution (gated)
    python marathon.py reset 001              # Restore stub, clear progress
    python marathon.py list [--tier N]        # List all exercises
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROGRESS_FILE = ROOT / ".marathon_progress.json"
USER_FILE = ROOT / ".marathon_user"
ANSWERS_DIR = ROOT / "answers"
TIER_DIRS = [
    "tier1_fluency",
    "tier2_patterns",
    "tier3_canonical",
    "tier4_async",
    "tier5_exercism_easy",
    "tier5_exercism_medium",
]
EX_RE = re.compile(r"^(\d{3})_")


def _whoami() -> str:
    """Read the local user identity from .marathon_user."""
    if USER_FILE.exists():
        name = USER_FILE.read_text().strip().lower()
        if name:
            return name
    return "default"


def _pytest_cmd() -> list[str]:
    """Prefer local .venv/bin/python -m pytest, fall back to `pytest` in PATH."""
    venv_py = ROOT / ".venv" / "bin" / "python"
    if venv_py.exists():
        return [str(venv_py), "-m", "pytest"]
    return ["pytest"]

MARK = {"passed": "✓", "failed": "✗", "untouched": "·", "revealed": "!"}


def list_exercises() -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    for tier in TIER_DIRS:
        tier_dir = ROOT / tier
        if not tier_dir.is_dir():
            continue
        for child in sorted(tier_dir.iterdir()):
            if not child.is_dir():
                continue
            m = EX_RE.match(child.name)
            if m:
                out.append((m.group(1), child))
    return out


def find_exercise(ex_id: str) -> Path | None:
    for eid, path in list_exercises():
        if eid == ex_id:
            return path
    return None


def _load_progress_raw() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {}


def _save_progress_raw(data: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True))


def load_progress() -> dict:
    """Load progress scoped to the current user, migrating old flat format."""
    data = _load_progress_raw()
    user = _whoami()
    # Migrate old flat format: if keys look like exercise IDs, wrap under "default"
    if data and all(k.isdigit() or k.startswith("_") for k in data):
        data = {"default": data}
        _save_progress_raw(data)
    return data.get(user, {})


def save_progress(prog: dict) -> None:
    """Save progress scoped to the current user."""
    data = _load_progress_raw()
    if data and all(k.isdigit() or k.startswith("_") for k in data):
        data = {"default": data}
    data[_whoami()] = prog
    _save_progress_raw(data)


def tier_of(path: Path) -> str:
    return path.parent.name


def _run_pytest(path: Path) -> int:
    cmd = _pytest_cmd() + [str(path), "-q", "--tb=short", "--no-header"]
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode


def _record_run(ex_id: str, passed: bool) -> None:
    prog = load_progress()
    entry = prog.get(ex_id, {})
    entry["status"] = "passed" if passed else "failed"
    now = datetime.now(timezone.utc).isoformat()
    if passed and "first_solved" not in entry:
        entry["first_solved"] = now
    entry["last_run"] = now
    prog[ex_id] = entry
    prog["_last_run"] = ex_id
    save_progress(prog)


def _run_exercise(ex_id: str, path: Path) -> int:
    print(f"\n▶ Running {path.name}...\n")
    rc = _run_pytest(path)
    _record_run(ex_id, rc == 0)
    if rc == 0:
        print(f"\n✓ {path.name} passed")
    else:
        print(f"\n✗ {path.name} failed — fix and rerun")
    return rc


def cmd_status(args: argparse.Namespace) -> int:
    exs = list_exercises()
    prog = load_progress()
    if not exs:
        print("No exercises found under tier dirs — did the converter run?")
        return 0

    total_passed = 0
    by_tier: dict[str, list[tuple[str, Path]]] = {}
    for eid, path in exs:
        by_tier.setdefault(tier_of(path), []).append((eid, path))

    for tier in TIER_DIRS:
        items = by_tier.get(tier, [])
        if not items:
            continue
        passed = sum(1 for eid, _ in items if prog.get(eid, {}).get("status") == "passed")
        total_passed += passed
        print(f"\n[{tier}]  {passed}/{len(items)}")
        for eid, path in items:
            status = prog.get(eid, {}).get("status", "untouched")
            marker = MARK.get(status, "?")
            hints = prog.get(eid, {}).get("hints_used", 0)
            hint_tag = f" (hints: {hints})" if hints else ""
            print(f"  {marker} {eid}  {path.name}{hint_tag}")

    print(f"\nTotal: {total_passed}/{len(exs)} passed")
    for eid, path in exs:
        if prog.get(eid, {}).get("status") != "passed":
            print(f"Next unsolved: {eid}  ({path.name})")
            break
    else:
        print("All clear — you're done!")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    ex_id = args.id
    if ex_id is None and args.current:
        ex_id = load_progress().get("_last_run")
        if not ex_id:
            print("No recent run. Use: marathon.py run NNN")
            return 1
    if ex_id is None:
        print("Usage: marathon.py run NNN  (or --current)")
        return 1
    path = find_exercise(ex_id)
    if not path:
        print(f"Exercise {ex_id} not found")
        return 1
    return _run_exercise(ex_id, path)


def cmd_next(args: argparse.Namespace) -> int:
    prog = load_progress()
    for eid, path in list_exercises():
        if prog.get(eid, {}).get("status") != "passed":
            return _run_exercise(eid, path)
    print("All exercises passed — you're done!")
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    ex_id = args.id
    prog = load_progress()
    if ex_id is None:
        ex_id = prog.get("_last_run")
    if ex_id is None:
        for eid, _ in list_exercises():
            if prog.get(eid, {}).get("status") != "passed":
                ex_id = eid
                break
    path = find_exercise(ex_id) if ex_id else None
    if not path:
        print("No exercise to watch — pass an id or run one first")
        return 1

    watched = [p for p in (path / "problem.py", path / "test_problem.py") if p.exists()]
    if not watched:
        print(f"Nothing to watch in {path}")
        return 1

    print(f"Watching {path.name} (Ctrl-C to stop)...")
    _run_exercise(ex_id, path)
    mtimes = {p: p.stat().st_mtime for p in watched}
    try:
        while True:
            time.sleep(1)
            changed = False
            for p in watched:
                m = p.stat().st_mtime
                if m != mtimes[p]:
                    mtimes[p] = m
                    changed = True
            if changed:
                print(f"\n--- re-running {path.name} ---")
                _run_exercise(ex_id, path)
    except KeyboardInterrupt:
        print("\nstopped watching")
        return 0


def cmd_hint(args: argparse.Namespace) -> int:
    path = find_exercise(args.id)
    if not path:
        print(f"Exercise {args.id} not found")
        return 1
    hints = path / ".meta" / "hints.md"
    if not hints.exists():
        print(f"No hints for {path.name}")
        return 1
    text = hints.read_text()
    parts = re.split(r"^## Hint (\d+)\s*$", text, flags=re.M)
    hint_map: dict[int, str] = {}
    for i in range(1, len(parts), 2):
        hint_map[int(parts[i])] = parts[i + 1].strip()
    if args.level not in hint_map:
        print(f"Hint level {args.level} not available. Available: {sorted(hint_map)}")
        return 1
    print(f"\n=== Hint {args.level} for {path.name} ===\n")
    print(hint_map[args.level])
    print()
    prog = load_progress()
    entry = prog.setdefault(args.id, {})
    entry["hints_used"] = max(entry.get("hints_used", 0), args.level)
    save_progress(prog)
    return 0


def cmd_reveal(args: argparse.Namespace) -> int:
    path = find_exercise(args.id)
    if not path:
        print(f"Exercise {args.id} not found")
        return 1
    solution = path / ".meta" / "solution.py"
    if not solution.exists():
        print(f"No solution file at {solution}")
        return 1
    print(f"⚠ This will print the reference solution for {path.name}.")
    print(f"Type 'REVEAL {args.id}' to confirm:")
    try:
        confirm = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\ncancelled")
        return 1
    if confirm != f"REVEAL {args.id}":
        print("cancelled (confirmation did not match)")
        return 1
    print(f"\n=== Solution for {path.name} ===\n")
    print(solution.read_text())
    prog = load_progress()
    entry = prog.setdefault(args.id, {})
    entry["revealed"] = True
    save_progress(prog)
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    path = find_exercise(args.id)
    if not path:
        print(f"Exercise {args.id} not found")
        return 1
    stub = path / ".meta" / "stub.py"
    problem = path / "problem.py"
    if not stub.exists():
        print(f"No stub snapshot at {stub} — can't reset")
        return 1
    shutil.copy(stub, problem)
    prog = load_progress()
    prog.pop(args.id, None)
    save_progress(prog)
    print(f"Reset {path.name} — progress cleared")
    return 0


def cmd_submit(args: argparse.Namespace) -> int:
    """Copy your passing solution to the shared answers directory."""
    ex_id = args.id
    path = find_exercise(ex_id)
    if not path:
        print(f"Exercise {ex_id} not found")
        return 1
    prog = load_progress()
    if prog.get(ex_id, {}).get("status") != "passed":
        print(f"Exercise {ex_id} hasn't been passed yet. Solve it first.")
        return 1
    user = _whoami()
    if user == "default":
        print("Set your identity first: echo 'yourname' > .marathon_user")
        return 1
    dest_dir = ANSWERS_DIR / user / ex_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    problem = path / "problem.py"
    dest = dest_dir / "solution.py"
    shutil.copy(problem, dest)
    rel = dest.relative_to(ROOT)
    print(f"✓ Saved to {rel}")
    if getattr(args, "git", False):
        subprocess.run(["git", "add", str(dest)], cwd=ROOT.parent)
        msg = f"answer({user}): {ex_id} {path.name}"
        result = subprocess.run(["git", "commit", "-m", msg], cwd=ROOT.parent)
        if result.returncode == 0:
            print(f"✓ Committed: {msg}")
        else:
            print("✗ git commit failed")
            return 1
    else:
        print(f"  git add {rel} && git commit -m 'answer({user}): {ex_id} {path.name}'")
    return 0


def cmd_peer(args: argparse.Namespace) -> int:
    """Show another user's answer, gated on your own solve."""
    ex_id = args.id
    peer = args.user
    path = find_exercise(ex_id)
    if not path:
        print(f"Exercise {ex_id} not found")
        return 1
    me = _whoami()
    if me == "default":
        print("Set your identity first: echo 'yourname' > .marathon_user")
        return 1
    if me == peer:
        print("That's you — check answers/{me}/{ex_id}/ instead")
        return 1
    prog = load_progress()
    if prog.get(ex_id, {}).get("status") != "passed":
        print(f"You haven't solved {ex_id} yet. Solve it first, then come back.")
        return 1
    peer_solution = ANSWERS_DIR / peer / ex_id / "solution.py"
    if not peer_solution.exists():
        print(f"{peer} hasn't submitted an answer for {ex_id} yet.")
        return 1
    print(f"\n=== {peer}'s solution for {path.name} ===\n")
    print(peer_solution.read_text())
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    exs = list_exercises()
    prog = load_progress()
    for eid, path in exs:
        tier = tier_of(path)
        if args.tier is not None and f"tier{args.tier}" not in tier:
            continue
        status = prog.get(eid, {}).get("status", "untouched")
        print(f"{eid}  [{tier:16s}]  {status:10s}  {path.name}")
    return 0



def cmd_verify(args: argparse.Namespace) -> int:
    """Run all reference solutions against tests silently."""
    exs = list_exercises()
    passed = failed = 0
    failures: list[str] = []
    for eid, path in exs:
        solution = path / ".meta" / "solution.py"
        problem = path / "problem.py"
        if not solution.exists():
            continue
        backup = problem.read_bytes()
        shutil.copy(solution, problem)
        cmd = _pytest_cmd() + [str(path), "-q", "--tb=line", "--no-header"]
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        problem.write_bytes(backup)
        if result.returncode == 0:
            print(f"PASS {path.name}")
            passed += 1
        else:
            print(f"FAIL {path.name}")
            failed += 1
            failures.append(f"{path.name}: {result.stdout.strip().splitlines()[-1] if result.stdout.strip() else result.stderr.strip()}")
    print()
    print(f"--- Passed: {passed}  Failed: {failed} ---")
    for f in failures:
        print(f"  ✗ {f}")
    return 1 if failed else 0


def cmd_review(args: argparse.Namespace) -> int:
    """Suggest exercises to revisit based on hint usage and solve age."""
    prog = load_progress()
    if not prog:
        print("No progress data yet. Solve some exercises first.")
        return 0
    now = datetime.now(timezone.utc)
    scored: list[tuple[float, str, list[str]]] = []
    for eid, entry in sorted(prog.items()):
        if eid.startswith("_"):
            continue
        if entry.get("status") != "passed":
            continue
        reasons: list[str] = []
        score = 0.0
        hints = entry.get("hints_used", 0)
        if hints >= 2:
            score += hints * 2
            reasons.append(f"used {hints} hints")
        if entry.get("revealed"):
            score += 3
            reasons.append("revealed")
        first = entry.get("first_solved")
        if first:
            try:
                solved_dt = datetime.fromisoformat(first)
                days = (now - solved_dt).days
                freshness = max(0, 14 - days)
                score += freshness
                if days <= 3:
                    reasons.append("solved recently — reinforce")
                elif days >= 14:
                    reasons.append(f"solved {days}d ago — may have faded")
            except (ValueError, TypeError):
                pass
        if score > 0 and reasons:
            scored.append((score, eid, reasons))
    scored.sort(reverse=True)
    if not scored:
        print("Nothing to review — keep solving!")
        return 0
    print("\nExercises to revisit:\n")
    for score, eid, reasons in scored[:3]:
        path = find_exercise(eid)
        name = path.name if path else eid
        print(f"  {eid}  {name}  ({', '.join(reasons)})")
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    """Import exercises from Exercism."""
    script = ROOT.parent / "scripts" / "import_exercism.py"
    if not script.exists():
        print(f"Import script not found: {script}")
        return 1
    cmd = [sys.executable, str(script),
           "--exercism-dir", args.exercism_dir,
           "--slugs", args.slugs,
           "--tier", args.tier]
    if args.dry_run:
        cmd.append("--dry-run")
    return subprocess.run(cmd).returncode


def cmd_completion(args: argparse.Namespace) -> int:
    """Generate shell completion script."""
    try:
        import shtab
        parser = build_parser()
        print(shtab.complete(parser, args.shell))
        return 0
    except ImportError:
        print("shtab not installed. Run: pip install shtab", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="marathon", description="Interview prep exercise runner")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="Show tier progress + next unsolved")
    pr = sub.add_parser("run", help="Run tests for an exercise")
    pr.add_argument("id", nargs="?", default=None)
    pr.add_argument("--current", action="store_true")
    sub.add_parser("next", help="Run the next unsolved exercise")
    pw = sub.add_parser("watch", help="Watch mode (polls file mtimes)")
    pw.add_argument("id", nargs="?", default=None)
    ph = sub.add_parser("hint", help="Show a hint")
    ph.add_argument("id")
    ph.add_argument("--level", type=int, default=1)
    prv = sub.add_parser("reveal", help="Reveal the reference solution (gated)")
    prv.add_argument("id")
    prs = sub.add_parser("reset", help="Reset an exercise to its original stub")
    prs.add_argument("id")
    pl = sub.add_parser("list", help="List all exercises")
    pl.add_argument("--tier", type=int, default=None)
    ps = sub.add_parser("submit", help="Save your passing solution to answers/")
    ps.add_argument("id")
    ps.add_argument("--git", action="store_true", help="Auto git-add and commit")
    pp = sub.add_parser("peer", help="View another user's answer (gated)")
    pp.add_argument("id")
    pp.add_argument("--user", required=True, help="Peer username to view")
    sub.add_parser("verify", help="Run all reference solutions against tests")
    sub.add_parser("review", help="Suggest exercises to revisit (spaced repetition)")
    pi = sub.add_parser("import", help="Import exercises from Exercism")
    pi.add_argument("--exercism-dir", default="exercism-python", help="Path to cloned exercism/python")
    pi.add_argument("--slugs", required=True, help="Comma-separated exercise slugs")
    pi.add_argument("--tier", default="tier5_exercism_easy", help="Target tier directory")
    pi.add_argument("--dry-run", action="store_true", help="Preview without writing")
    pc = sub.add_parser("completion", help="Generate shell completion script")
    pc.add_argument("shell", choices=["bash", "zsh"], help="Shell type")
    return p


def main() -> int:
    args = build_parser().parse_args()
    cmds = {
        "status": cmd_status,
        "run": cmd_run,
        "next": cmd_next,
        "watch": cmd_watch,
        "hint": cmd_hint,
        "reveal": cmd_reveal,
        "reset": cmd_reset,
        "list": cmd_list,
        "submit": cmd_submit,
        "peer": cmd_peer,
        "verify": cmd_verify,
        "review": cmd_review,
        "import": cmd_import,
        "completion": cmd_completion,
    }
    return cmds[args.cmd](args) or 0


if __name__ == "__main__":
    sys.exit(main())
