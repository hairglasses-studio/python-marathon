#!/usr/bin/env python3
"""Generate test_problem.py from exercism/problem-specifications canonical-data.json.

Usage:
    python scripts/generate_from_specs.py \
        --specs-dir problem-specifications \
        --slug leap \
        --output exercises/tier5_exercism_easy/039_leap/test_problem.py

Or preview without writing:
    python scripts/generate_from_specs.py --specs-dir problem-specifications --slug leap --preview
"""

from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path


def _python_value(val) -> str:
    """Convert a JSON value to a Python literal string."""
    if val is None:
        return "None"
    if isinstance(val, bool):
        return "True" if val else "False"
    if isinstance(val, str):
        return repr(val)
    if isinstance(val, (int, float)):
        return repr(val)
    if isinstance(val, list):
        items = ", ".join(_python_value(v) for v in val)
        return f"[{items}]"
    if isinstance(val, dict):
        items = ", ".join(f"{repr(k)}: {_python_value(v)}" for k, v in val.items())
        return f"{{{items}}}"
    return repr(val)


def _flatten_cases(cases: list[dict], prefix: str = "") -> list[dict]:
    """Flatten nested case groups into a flat list."""
    flat = []
    for case in cases:
        if "cases" in case:
            group_prefix = case.get("description", "")
            flat.extend(_flatten_cases(case["cases"], group_prefix))
        else:
            if prefix:
                case = dict(case)
                case["description"] = f"{prefix}: {case.get('description', '')}"
            flat.append(case)
    return flat


def generate_test(specs_dir: Path, slug: str) -> str:
    """Generate a test_problem.py from canonical-data.json."""
    data_file = specs_dir / "exercises" / slug / "canonical-data.json"
    if not data_file.exists():
        raise FileNotFoundError(f"No canonical data: {data_file}")

    data = json.loads(data_file.read_text())
    exercise = data.get("exercise", slug)
    cases = _flatten_cases(data.get("cases", []))

    # Detect the function name from the property field
    properties = {c.get("property") for c in cases if c.get("property")}
    func_name = slug.replace("-", "_")
    if len(properties) == 1:
        func_name = properties.pop()

    lines = [
        "# Tests — do not edit. Run via:",
        f"#   python marathon.py run NNN",
        "#",
        f"# Auto-generated from exercism/problem-specifications: {slug}",
        "",
        "from problem import *  # noqa: F401,F403",
        "",
        "",
    ]

    # Generate test functions
    for i, case in enumerate(cases):
        desc = case.get("description", f"case_{i}")
        safe_name = "".join(c if c.isalnum() or c == "_" else "_" for c in desc.lower())
        safe_name = safe_name.strip("_")[:60]
        prop = case.get("property", func_name)
        inputs = case.get("input", {})
        expected = case.get("expected", None)

        # Handle error expectations
        if isinstance(expected, dict) and "error" in expected:
            # Exercise expects an error
            args = ", ".join(f"{k}={_python_value(v)}" for k, v in inputs.items())
            lines.append(f"def test_{safe_name}():")
            lines.append(f"    import pytest")
            lines.append(f"    with pytest.raises((ValueError, Exception)):")
            lines.append(f"        {prop}({args})")
            lines.append("")
            lines.append("")
        else:
            args = ", ".join(f"{k}={_python_value(v)}" for k, v in inputs.items())
            lines.append(f"def test_{safe_name}():")
            lines.append(f"    assert {prop}({args}) == {_python_value(expected)}")
            lines.append("")
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description="Generate test_problem.py from canonical specs")
    p.add_argument("--specs-dir", required=True, help="Path to problem-specifications clone")
    p.add_argument("--slug", required=True, help="Exercise slug (e.g., leap)")
    p.add_argument("--output", help="Output file path (default: stdout)")
    p.add_argument("--preview", action="store_true", help="Print to stdout without writing")
    args = p.parse_args()

    specs_dir = Path(args.specs_dir)
    test_code = generate_test(specs_dir, args.slug)

    if args.preview or not args.output:
        print(test_code)
    else:
        out = Path(args.output)
        out.write_text(test_code)
        print(f"Written to {out}")


if __name__ == "__main__":
    main()
