# python-marathon Roadmap

## Done

### Exercise bank
- [x] 31 original exercises across 4 tiers (openai-prep + hand-written async)
- [x] 10 Exercism Python track exercises imported (tier5_exercism_easy, 032-041)
- [x] `exercises/manifest.json` — source metadata for all exercises
- [x] `scripts/import_exercism.py` — Exercism import pipeline with dry-run, slug selection, auto-renumber
- [x] `scripts/backfill_manifest.py` — one-shot manifest generator
- [x] All 41 exercises verified passing under Python 3.10.11

### Multi-user collaborative learning
- [x] Per-user identity via `.marathon_user` file
- [x] Namespaced `.marathon_progress.json` (with old-format migration guard)
- [x] `marathon.py submit NNN [--git]` — save passing solution to `answers/<user>/NNN/`
- [x] `marathon.py peer NNN --user NAME` — view peer's answer (gated on own solve)
- [x] `answers/` directory tracked in git, per-user subdirectories (merge-conflict-free)
- [x] Claude Code deny rules on `answers/**` (same honor system as solutions)

### Multi-agent tutor support
- [x] Claude Code — full harness (`.claude/settings.json` deny rules + 13 slash commands)
- [x] Codex CLI — `.codex/config.toml` (behavioral tutor contract, workspace-write sandbox)
- [x] Gemini CLI — `.gemini/settings.json` (context bridge with AGENTS.md)
- [x] GitHub Copilot — `.github/copilot-instructions.md` (thin mirror)
- [x] AGENTS.md canonical header + multi-agent documentation

### Budget model configuration
- [x] Claude Code: Sonnet 4.6 project default (Claude Pro $20/mo)
- [x] Codex CLI: o3-mini at medium reasoning (ChatGPT Plus $20/mo)
- [x] Gemini CLI: Flash 2.5 free tier documented
- [x] Model recommendations in AGENTS.md and README

### Standalone CLI (no LLM required)
- [x] `marathon.py verify` — run all reference solutions against tests
- [x] `marathon.py review` — algorithmic spaced-repetition suggestions
- [x] `marathon.py import` — Exercism import wired as subcommand
- [x] `marathon.py completion {bash,zsh}` — via shtab
- [x] Man page (`docs/marathon.1.md` + `make man` via pandoc)
- [x] Zsh completion file (`completions/_marathon`, 197 lines)
- [x] Makefile with `man`, `verify`, `completion` targets

### Developer experience
- [x] `.python-version` pinned to 3.10
- [x] Getting-started README for beginners (Python install, clone, venv, workflow)
- [x] `exercism-python/` clone gitignored

---

## Next up

### More Exercism exercises
- [ ] Import medium-difficulty batch into `tier5_exercism_medium/` (anagram, binary-search, linked-list, matrix, robot-name, etc.)
- [ ] Curate a "top 30" Exercism list ordered by interview relevance
- [ ] Backfill hand-written `.meta/hints.md` for imported exercises (current ones are placeholder templates)

### Exercise source expansion
- [ ] LeetScrape integration — generate stubs + pytest from LeetCode (needs session cookie, `scripts/import_leetcode.py`)
- [ ] leetcode-prep-mcp — MCP tool for fetching LeetCode problems dynamically
- [ ] Exercism problem-specifications — generate exercises from canonical JSON test data (language-agnostic source, `scripts/generate_from_specs.py`)

### CLI enhancements
- [ ] `marathon.py stats` — per-user analytics (solve rate, avg hints, time-to-solve distribution)
- [ ] `marathon.py diff NNN --user NAME` — side-by-side diff of your answer vs peer's
- [ ] `marathon.py tag --list` / `marathon.py tag --filter TOPIC` — exercise tagging and search from manifest.json
- [ ] Rich terminal output (optional `rich` dep for colored tables, progress bars)
- [ ] `marathon.py watch` improvements — inotify support on Linux (optional `watchdog` dep)

### Collaborative features
- [ ] Progress dashboard — combined view of both users' status in `marathon.py status --all`
- [ ] Peer notification — flag when partner submits a new answer you can now view
- [ ] Shared exercise notes — `answers/<user>/NNN/notes.md` for post-solve commentary

### Agent tutor improvements
- [ ] Codex skill surface — `.agents/skills/` repo-local skills as Codex equivalent to Claude slash commands
- [ ] Gemini tool support — when Gemini CLI adds tool/command support, mirror the Claude skill surface
- [ ] Exercise-aware model switching — auto-suggest upgrading to Opus/GPT-4o for Tier 3-4 exercises
- [ ] Tutor memory — persist per-exercise learner context across sessions (what they struggled with, approaches tried)

### Quality and testing
- [ ] CI — GitHub Actions workflow: `marathon.py verify` on every push
- [ ] Pre-commit hook — run `marathon.py verify` on changed exercise dirs only
- [ ] Exercise linter — validate all exercises have the required 7-file layout
- [ ] Test the import pipeline against the full 193-exercise Exercism catalog

### Documentation
- [ ] Contributing guide for adding new exercises
- [ ] Exercise difficulty calibration (compare target times to actual solve data)
- [ ] Video walkthrough for Austin's onboarding
