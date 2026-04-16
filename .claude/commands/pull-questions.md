---
description: Import exercises from Exercism or other sources
argument-hint: "[slugs]"
---

Import new exercises into the marathon bank. Requires the Exercism Python
track to be cloned locally.

1. Check if `~/hairglasses-studio/python-marathon/exercism-python` exists.
   If not, clone it: `git clone https://github.com/exercism/python.git exercism-python`
   (into the repo root, it's gitignored).

2. If $ARGUMENTS contains comma-separated slugs, use those.
   Otherwise, list available Exercism exercises that haven't been imported
   yet (compare against `exercises/manifest.json`) and let the learner pick.

3. Run `python scripts/import_exercism.py --exercism-dir exercism-python --slugs <slugs> --dry-run`
   to preview what will be created.

4. After confirmation, run without `--dry-run`.

5. Run `/verify` on the newly imported exercises to confirm they pass.

6. Report what was added: exercise IDs, names, tier placement.
