---
name: peer
description: View a study partner's submitted answer (gated on your own solve)
argument_hint: "NNN [--user NAME]"
---

Run `python marathon.py peer NNN --user NAME` from `exercises/`.
If `--user` not provided, infer the other user (mitch->austin, austin->mitch).
If gated, encourage solving first. If shown, offer Socratic comparison.
