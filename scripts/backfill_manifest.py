#!/usr/bin/env python3
"""One-shot: generate exercises/manifest.json from existing exercise dirs."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXERCISES = ROOT / "exercises"
MANIFEST = EXERCISES / "manifest.json"
EX_RE = re.compile(r"^(\d{3})_")
TIER_DIRS = [
    "tier1_fluency",
    "tier2_patterns",
    "tier3_canonical",
    "tier4_async",
    "tier5_exercism_easy",
    "tier5_exercism_medium",
]


def main() -> None:
    manifest: dict[str, dict] = {}
    for tier in TIER_DIRS:
        tier_dir = EXERCISES / tier
        if not tier_dir.is_dir():
            continue
        for child in sorted(tier_dir.iterdir()):
            if not child.is_dir():
                continue
            m = EX_RE.match(child.name)
            if not m:
                continue
            ex_id = m.group(1)
            num = int(ex_id)
            if num <= 26:
                source = "openai-prep"
            elif num <= 31:
                source = "hand-written"
            else:
                source = "unknown"
            manifest[ex_id] = {
                "slug": child.name,
                "tier": tier,
                "source": source,
                "source_id": None,
                "source_url": None,
            }

    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {len(manifest)} entries to {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
