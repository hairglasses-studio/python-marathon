---
description: Silently run all reference solutions against tests
---

Run every reference solution against its tests to verify the exercise
bank is healthy. Work from `exercises/`.

For each exercise directory found by `marathon.py list`:
1. Back up `problem.py` to `problem.py.bak`
2. Copy `.meta/solution.py` to `problem.py`
3. Run `python marathon.py run NNN` silently (capture output)
4. Restore `problem.py` from `problem.py.bak` and delete the backup

Collect results and print a summary table:
- PASS / FAIL per exercise
- Total passed / total failed
- For any failures, show the captured pytest output

Do not modify progress state — this is a verification run, not a
learner session. If all exercises pass, report the count and Python
version. If any fail, flag them loudly.
