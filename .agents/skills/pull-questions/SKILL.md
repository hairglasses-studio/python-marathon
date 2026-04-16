---
name: pull-questions
description: Import exercises from Exercism or other sources
argument_hint: "[slugs]"
---

Check if `exercism-python/` clone exists in repo root. If not, clone it.
Run `python marathon.py import --exercism-dir ../exercism-python --slugs SLUGS --dry-run` first.
After confirmation, run without `--dry-run`. Verify imported exercises pass.
