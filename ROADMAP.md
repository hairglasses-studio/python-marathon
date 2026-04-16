# python-marathon Roadmap

## Done

### Exercise bank
- [x] 31 original exercises across 4 tiers (openai-prep + hand-written async)
- [x] 10 Exercism Python track exercises imported (tier5_exercism_easy, 032-041)
- [x] `exercises/manifest.json` — source metadata for all exercises
- [x] `scripts/import_exercism.py` — Exercism import pipeline with dry-run, slug selection, auto-renumber
- [x] `scripts/backfill_manifest.py` — one-shot manifest generator
- [x] All 41 exercises verified passing under Python 3.10.11
- [x] 20 medium Exercism exercises imported (tier5_exercism_medium, 042-061); 61 total

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

### Gamification and progress
- [x] Solve-time recording (`solve_duration_seconds` stored in progress JSON on pass)
- [x] Streak tracking (`streak_days` + `last_active_date` in `_meta`)
- [x] Badge system (14 badges in `badges.json`; `marathon.py badges`)
- [x] XP and level system (tier-weighted; bonus XP; 50 levels; shown in `status`)
- [x] Activity heatmap (GitHub-style 7×12 Unicode block grid in `status`)
- [x] SM-2 spaced repetition (`sr_ef`, `sr_n`, `sr_interval` per exercise; `review` queue)
- [x] Random challenge picker (`marathon.py challenge [--tier N]`)
- [x] Kata/repeat mode (`marathon.py kata NNN`; tracks `kata_count`)
- [x] Manifest enrichment: `tags`, `difficulty`, `target_minutes` on all 41 original exercises
- [x] `marathon.py tag` — show all tags with exercise counts; `--filter TOPIC`
- [x] `marathon.py recommend` — tag-coverage-based recommendation

### Progress and export
- [x] Progress export/import (`marathon.py export` / `import-progress FILE`)
- [x] Obsidian vault export (`marathon.py export-obsidian --vault PATH`)
- [x] `marathon.py challenge-peer NNN --user PEER` + `answers/challenges.json`
- [x] Two-dimensional exercise addressing (`"tier2 3"` format in `_resolve_exercise_id`)
- [x] Incremental test gates (`@pytest.mark.incremental` in `conftest.py`)
- [x] Exercise scaffold generator (`marathon.py new --name SLUG --tier T`)

### CI and quality
- [x] `marathon.py lint-exercises` — validate 7-file layout, test imports, stub content
- [x] `.github/workflows/verify.yml` — `lint-exercises` + `verify` on push/PR; Python 3.10/3.11/3.12 matrix

### Source tooling
- [x] `scripts/generate_from_specs.py` — auto-generate `test_problem.py` from Exercism `canonical-data.json`

### Docs and agent surfaces
- [x] CONTRIBUTING.md
- [x] `.agents/skills/` repo-local SKILL.md files for Codex CLI

---

## P0 — Bug Fixes (code exists but is broken)

- [x] **SM-2 loop completion** — `_sm2_update()` now called in `_record_run()` on every pass; SR intervals evolve through solve cycles
- [x] **Manifest backfill for 042-061** — all 20 medium Exercism exercises now have `difficulty`, `tags`, and `target_minutes`
- [ ] **Hints backfill for Exercism exercises (032-061)** — all 30 Exercism exercises have generic 3-line boilerplate hints; replace with substantive 3-level authored hints (can use LLM-assisted generation from README + test content)
- [x] **Tier5-clear badges** — `badges.json` now has tier5-easy-clear and tier5-medium-clear (16 badges total)
- [ ] **Peer challenge resolution** — `challenge-peer` creates the JSON record but there is no auto-compare, notification, or resolution flow; add `marathon.py peer-status` to show open challenges and winner when both solve

---

## P1 — High impact, minimal effort

### Rich terminal output
- [ ] Optional `rich` dep with graceful degradation (`try: import rich; HAS_RICH = True except: HAS_RICH = False`)
- [ ] `rich.table.Table` for `marathon.py status` — colored tier progress
- [ ] `rich.progress.Progress` for `marathon.py verify` — progress bar during long runs
- [ ] `rich.syntax.Syntax` for displaying `problem.py` stubs and hints with highlighting
- [ ] `rich.panel.Panel` for exercise introductions in `marathon.py next`
- [ ] Ref: [textualize/rich](https://github.com/textualize/rich) (~50k stars)

### `# MARATHON: NOT DONE` sentinel
- [x] If `problem.py` contains `# MARATHON: NOT DONE`, prevent `next` from auto-advancing even if tests pass
- [x] Print: "Tests pass but exercise is marked NOT DONE. Remove the sentinel when satisfied."
- [x] Source: rustlings `// I AM NOT DONE` pattern

### Keystroke commands in `watch` mode
- [ ] Use stdlib `termios`/`select` raw-mode stdin alongside the mtime poll loop
- [ ] Keys: `h` = show hint level 1, `l` = print exercise list, `r` = force rerun, `n` = skip to next, `q` = quit, `?` = key reference
- [ ] Zero new deps; source: rustlings watch mode interactive keys

### `marathon.py shell NNN` — REPL mode
- [x] Drop into `code.interact()` (stdlib) with `problem.py` pre-imported
- [x] Banner shows exercise ID and name
- [x] Zero deps

### `marathon.py doctor` — self-diagnostics
- [x] Checks: Python version, pytest, .venv, .marathon_user, progress JSON, manifest integrity, disk/manifest sync, badges
- [x] Zero deps; source: `rustup doctor`, `brew doctor`

### `marathon.py deps` — optional dependency table
- [x] Print feature→package table with installed/missing status for 7 optional deps
- [x] `marathon.py deps --install rich radon` — runs pip install for named packages
- [x] Makes the implicit optional-dep system explicit and self-documenting

### `marathon.py stats [NNN]` + shields.io badge
- [x] `marathon.py stats --json` — emit JSON with solved/total/pct/xp/level/streak/badges
- [x] `marathon.py stats` — human-readable progress summary
- [ ] CI step writes JSON to gist; shields.io endpoint badge in README
- [ ] `marathon.py stats NNN` — per-exercise aggregate from peer answers

### Progress schema versioning + migration
- [x] `_schema_version` field in progress JSON root (currently v2)
- [x] `marathon.py migrate` — apply incremental migrations (v0→v1 flat→namespaced, v1→v2 SM-2 field init)
- [x] Source: Anki card format versioning

### Self-report quality rating on review
- [ ] After a review solve, prompt: "How well did you remember this? [0=forgot 1=hard 2=ok 3=easy] "
- [ ] Single keypress via `termios` raw mode; map to SM-2/FSRS quality scale
- [ ] More accurate than inferring quality from hints alone; source: Anki grade 0-5 UX

---

## P2 — Medium effort (optional deps or moderate work)

### Code quality scoring
- [ ] Optional `radon` dep for cyclomatic complexity (CC) + maintainability index (MI)
- [ ] Display after each passing run: `Complexity: A (CC=3) | Maintainability: B (MI=68)`
- [ ] Composite "session score" combining tests, complexity, hints, time
- [ ] Ref: [radon](https://pypi.org/project/radon/), [xenon](https://pypi.org/project/xenon/)

### Performance benchmarking
- [ ] `marathon.py bench NNN` — `timeit`-based comparison against reference solution
- [ ] `.meta/bench_inputs.py` defines large inputs + threshold ratio
- [ ] Report: `Your solution: 2.3ms | Reference: 1.8ms | Ratio: 1.28x`
- [ ] Optional `big_O` dep for empirical complexity class detection
- [ ] Ref: [big_O](https://github.com/pberkes/big_O), [bigocheck](https://github.com/adwantg/bigocheck)

### Solution diff view
- [ ] `marathon.py diff NNN [--user NAME]` — side-by-side diff of your answer vs peer's using `difflib.unified_diff`
- [ ] Gate: you must have solved + peer must have submitted
- [ ] Enhancement: AST-normalized diff — normalize variable names before diffing; source: [exercism/python-representer](https://github.com/exercism/python-representer)

### Leaderboard
- [ ] `marathon.py leaderboard [--tier N]` — reads all `answers/<user>/` dirs, aggregates solve count + XP per user
- [ ] Sort by: tier completion, total solved, average quality score
- [ ] Deposit `stats.json` alongside `solution.py` on submit for shared metrics

### Anki deck export
- [ ] `marathon.py export-anki [--output deck.apkg] [--include-sr-history]`
- [ ] Front: problem name + README problem statement. Back: `.meta/solution.py` with hints as extra field
- [ ] `--include-sr-history`: pre-populate Anki cards with your FSRS ReviewLog so scheduling continues rather than cold-starting
- [ ] Optional dep: `genanki`; source: [donnemartin/interactive-coding-challenges](https://github.com/donnemartin/interactive-coding-challenges)

### FSRS upgrade (replace SM-2)
- [ ] Replace SM-2 with [py-fsrs](https://github.com/open-spaced-repetition/py-fsrs) v6 for better-calibrated review scheduling (FSRS outperforms SM-2; Anki switched to FSRS as default in 23.10)
- [ ] Drop-in: `Scheduler`, `Card`, `ReviewLog` API; migrate `sr_ef`, `sr_n`, `sr_interval` to FSRS card state on first `review` call
- [ ] Adds `py-fsrs` as optional dep (~1000 lines pure Python)

### FSRS weight optimizer
- [ ] `marathon.py fsrs-optimize` — ingest full ReviewLog history, run `fsrs-optimizer` to calibrate the 17 FSRS parameters to the user's personal forgetting curve
- [ ] Output updated parameters into progress JSON
- [ ] Source: [open-spaced-repetition/fsrs-optimizer](https://github.com/open-spaced-repetition/fsrs-optimizer) (pip installable)

### Forgetting curve visualization
- [ ] `marathon.py curve NNN` — sparkline of predicted retention probability for exercise NNN over the next 30 days based on FSRS state
- [ ] Shows "the forget cliff is coming in 3 days"; purely derived from existing progress data
- [ ] Source: FSRS algorithm visualization, Anki stats page

### Review session discipline mode
- [ ] `marathon.py review --session` — locks you into reviewing all due items before `next` can advance
- [ ] `--soft` flag: warns instead of hard-gating
- [ ] Source: Anki daily review discipline model (without punitive features)

### Inotify file watcher
- [ ] Replace mtime polling in `marathon.py watch` with `watchdog` (optional dep) for instant rerun on save
- [ ] Fallback to 1s polling when `watchdog` not installed
- [ ] Source: rustlings inotify-driven watch

### Pre-commit hook
- [ ] `.git/hooks/pre-commit` (or `pre-commit` config) runs `marathon.py verify --changed-only`
- [ ] `marathon.py verify --changed-only` — only re-run reference solutions for exercises touched in `git diff --name-only`
- [ ] Document in CONTRIBUTING.md

---

## Content organization and discovery

### Pattern taxonomy
- [ ] Add `"pattern": "sliding-window"` (and similar) field to `manifest.json` per exercise
- [ ] Patterns: sliding-window, two-pointers, fast-slow-pointers, binary-search, BFS, DFS, backtracking, dynamic-programming, topological-sort, heap, trie, union-find, monotonic-stack, bit-manipulation, divide-and-conquer
- [ ] `marathon.py pattern` — show all patterns with solved/total counts
- [ ] `marathon.py next --pattern two-pointers` — force next exercise from that pattern
- [ ] `marathon.py list --pattern dynamic-programming` — filter by pattern
- [ ] Source: NeetCode roadmap (the most effective interview prep mental model)

### Named curated shortlists
- [ ] `exercises/curations.json` with named ordered exercise lists: `blind75`, `async-mastery`, `interview-week`, etc.
- [ ] `marathon.py list --curated blind75` — show exercises in that track with solved status
- [ ] `marathon.py next --curated interview-week` — advance within the curated track
- [ ] Source: NeetCode 150, Blind 75, tech-interview-handbook "minimum effective dose" concept

### Concept prerequisite DAG
- [ ] Add `"prereqs": ["001", "007"]` field per exercise in `manifest.json`
- [ ] `marathon.py recommend` upgrades from tag-coverage heuristic to topological sort (never recommend until prereqs solved)
- [ ] `marathon.py map NNN` — print the prerequisite chain for one exercise as a tree
- [ ] Source: Exercism v3 concept exercise DAG model

### Company tag metadata
- [ ] Add `"companies": ["Google", "Amazon", "Meta"]` field to relevant manifest entries
- [ ] `marathon.py list --company google` — surface company-targeted exercises
- [ ] Source: NeetCode, FAANG-Coding-Interview-Questions, LeetScrape

### LSP config generation
- [ ] `marathon.py lsp NNN` — generate `pyrightconfig.json` scoped to one exercise folder
- [ ] Eliminates IDE confusion from `from problem import *` collision across exercises
- [ ] Source: rustlings `lsp` subcommand

---

## Gamification improvements

### Power tokens (streak reward)
- [ ] After N consecutive exercises solved without hints/reveals: award a "power token"
- [ ] `marathon.py tokens` shows balance; `--use-token` flag on `reveal` (bypasses XP penalty) or `hint --level 3` (no hints_used increment)
- [ ] Avoids hearts/lives punishment; source: Boot.dev random chest on 15-in-a-row streaks

### Per-exercise time-series solve history
- [ ] Add `kata_history: [{"date": ..., "duration_s": ..., "hints_used": ...}]` to progress JSON
- [ ] `marathon.py kata NNN` appends to history; `marathon.py kata NNN --history` shows improvement sparkline: "Attempt 1: 28min | Attempt 2: 14min | Attempt 3: 9min"
- [ ] Source: competitive programming dashboard pattern

### Hot streak XP multiplier
- [ ] If ≥5 exercises solved in a single session (< 30 min between solves): 1.5× XP multiplier activates
- [ ] Shown in `run` output; encourages deep sessions over scattered touches
- [ ] Source: Codewars consecutive-solve bonus

### Kyu/Dan rank system
- [ ] Decouple skill rank from XP level: kyu 8 → kyu 1 → dan 1 → dan 8 based on solved difficulty thresholds
- [ ] Honor (separate counter) tracks community contributions: submitting answers, creating exercises, writing notes
- [ ] Show both in `marathon.py status` header; source: Codewars honor + kyu/dan model

### Tier completion certificates
- [ ] `marathon.py certificate --tier 2` — generate SVG (stdlib `xml.etree.ElementTree`) with tier name, solve stats, XP earned, completion date, user name
- [ ] No external validation; useful for motivation and portfolio screenshots
- [ ] Source: Boot.dev course certs, progHours

---

## Testing and quality improvements

### Linter improvements
- [ ] `lint-exercises` currently checks 9 conditions; add:
  - `hints.md` contains all three `## Hint 1/2/3` sections
  - `notes.md` exists (part of 7-file layout but not currently checked)
  - `README.md` contains `## Topics` and `## Target Time` sections
  - `manifest.json` entry exists for every exercise dir and has all required fields
  - `test_problem.py` has at least one `def test_` function

### Hidden test tier
- [ ] Some exercises ship `.meta/test_hidden.py` — runs only during `marathon.py verify`, never exposed to learners
- [ ] `lint-exercises` checks for presence when the file exists; `verify` runs hidden tests during CI
- [ ] Catches solutions that only pass cherry-picked examples; source: HackerRank hidden tests

### Property-based testing option
- [ ] Some exercises gain `.meta/test_pbt.py` using Hypothesis `@given` / `@settings`
- [ ] `marathon.py run NNN --pbt` — run property-based tests (optional dep: `hypothesis`)
- [ ] Good for tier3/4 exercises; source: HypothesisWorks/hypothesis

### Stage-by-stage test streaming
- [ ] Custom pytest plugin hook on `pytest_runtest_logreport` — print each test result as it completes with pass/fail prefix and timestamp
- [ ] Especially valuable for slow async tests (tier4); source: codecrafters-io/cli streaming model

---

## Collaborative features

### `marathon.py status --all`
- [ ] Combined view of all users' progress: user × tier × solve count table sorted by total XP
- [ ] Source: ROADMAP TODO

### `marathon.py coach --users alice,bob`
- [ ] Side-by-side progress matrix: exercises in rows, users in columns, colored by solved/unsolved/hinted
- [ ] Reads from `answers/` directory; no server required
- [ ] Source: [naimulcsx/progHours](https://github.com/naimulcsx/progHours) coach analytics dashboard

### AST-normalized solution fingerprinting
- [ ] On `submit`, hash `ast.dump(ast.parse(source))` and check against existing `answers/<user>/` entries
- [ ] If match: "Your approach matches Austin's. `marathon.py peer NNN --user austin` to see their solution."
- [ ] Source: exercism/python-representer — turns individual solutions into shared knowledge

### Group timed events
- [ ] `marathon.py event create --name sprint-2026-04 --exercises 010,020,030 --deadline 2026-04-30`
- [ ] Creates `answers/events/<name>.json` with participant/solve/timestamp records
- [ ] `marathon.py event status <name>` — mini-leaderboard within the event
- [ ] Source: Advent of Code community events, Codewars kumite tournaments

### Peer notification
- [ ] Flag in `marathon.py status` when partner has submitted a new answer you can now view
- [ ] Reads `answers/<peer>/` directory listing and compares mtime to last-checked timestamp

### Shared exercise notes
- [ ] `answers/<user>/NNN/notes.md` for persistent post-solve commentary
- [ ] `/reflect` skill writes output to notes file instead of being ephemeral
- [ ] `marathon.py notes NNN` — open notes file in `$EDITOR`

### Discord bot
- [ ] Stateless bot reading `answers/` from git repo
- [ ] `/marathon-status @user`, `/marathon-challenge @user NNN`, `/marathon-leaderboard`
- [ ] ~200 lines of `discord.py`

---

## Agent tutor improvements

### Structured Socratic hint protocol
- [ ] Update `.claude/commands/hint.md` to enforce: hint level 1 = LLM must respond with a question (not a statement), level 2 = directional statement, level 3 = code fragment
- [ ] Source: LLM tutoring research finding that 35% of LLM hints are too direct (Springer 2025); Exercism `actionable/informative/celebratory` taxonomy

### Tutor memory
- [ ] Persist per-exercise learner context across sessions: what they struggled with, approaches tried, common mistakes
- [ ] Source: [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) Soul Templates

### `marathon.py interview NNN` — simulated interview mode
- [ ] User types their approach explanation; Claude (via `claude -p` subprocess) plays interviewer
- [ ] Asks clarifying questions, probes time/space complexity, gives feedback on communication quality
- [ ] Different from `/reflect` (post-solve) — this is in-solve communication coaching
- [ ] Source: yangshun/tech-interview-handbook behavioral interview prep

### Exercise-aware model switching
- [ ] Auto-suggest upgrading to Opus/GPT-4o for Tier 3-4 exercises where deeper reasoning helps
- [ ] `/model sonnet` default; `/model opus` recommended for canonical problems

---

## Architecture improvements

### XDG Base Directory compliance for progress file
- [ ] Move progress from `exercises/.marathon_progress.json` (gitignored) to `$XDG_DATA_HOME/marathon/progress.json` (default: `~/.local/share/marathon/`)
- [ ] Progress survives `git clone` and repo deletion; enables multi-repo marathon instances
- [ ] Auto-migrate existing file from old location on first run
- [ ] Source: `bootdev` CLI XDG pattern

### Plugin/hook system
- [ ] Read `~/.config/marathon/hooks/` for user Python modules registering callbacks: `on_pass`, `on_badge_earn`, `on_streak_break`, `on_review_due`
- [ ] Enables: ntfy.sh push notifications, Slack webhooks, custom badge logic — without modifying the runner
- [ ] Source: pytest `conftest.py` hook model

### `marathon.py config` — user config file
- [ ] Read/write `~/.config/marathon/config.toml` (XDG_CONFIG_HOME)
- [ ] Keys: `editor`, `default_tier_filter`, `color_theme` (auto/always/never), `watch_interval_ms`
- [ ] `marathon.py config set editor=nvim`, `marathon.py config show`
- [ ] Source: `~/.bootdev.yaml` pattern

---

## Exercise source expansion

### Multiple named solution approaches
- [ ] `.meta/` gains `solution_brute.py` + `solution_optimal.py` with Big-O labeled header comments
- [ ] `marathon.py reveal NNN` shows brute-force first; `--optimal` flag shows optimal; `--compare` shows diff
- [ ] Source: `darkprinx/break-the-ice-with-python`, `MTrajK/coding-problems` (Big-O labeled approaches)

### Structured "further reading" links
- [ ] Add `## Learn More` section to `hints.md` format with 2-3 curated doc/blog/paper links per exercise
- [ ] Linter checks for this section's presence in authored exercises
- [ ] Source: `david-legend/python-algorithms` per-DS further reading links

### LeetCode integration
- [ ] `scripts/import_leetcode.py` — generate stubs + pytest from LeetCode via [LeetScrape](https://github.com/nikhil-ravi/LeetScrape) (needs session cookie)
- [ ] [leetcode-prep-mcp](https://github.com/dpkirschner/leetcode-prep-mcp) — MCP tool for fetching problems dynamically

### Codeforces / competitive programming import
- [ ] `scripts/import_codeforces.py` — given a Codeforces problem URL, fetch sample test cases from the public problem page (no auth required), generate exercise scaffold
- [ ] Source: Codeforces problems are publicly scrapeable; multiple AoC import scripts as reference

### LLM-assisted hints backfill
- [ ] `scripts/gen_hints.py --exercises 032-061` — use Claude to generate substantive 3-level hints from README + test content; human review pass before commit
- [ ] The 30 Exercism exercises with generic boilerplate are the single largest content gap

### LLM-assisted exercise generation
- [ ] `marathon.py new --from-description "implement a LRU cache" --tier 3` — scaffold full 7-file exercise using Claude; generate draft, human reviews before commit
- [ ] Source: ROADMAP TODO + LLM tutoring research

### Generator-based test authoring
- [ ] `scripts/gen_testcases.py` — write a generator script + reference solution, auto-produce `test_problem.py`
- [ ] Source: [online-judge-tools/oj](https://github.com/online-judge-tools/oj) `generate-input` + `generate-output`

### Seasonal challenge mode (AoC-style)
- [ ] `marathon.py season create --name "interview-sprint-2026" --weeks 4`
- [ ] Creates structured sequence of exercises with weekly themes and a final "boss" exercise
- [ ] Source: Advent of Code seasonal content model

### Koans-style fill-in-the-blank tier
- [ ] New exercise variant: `test_problem.py` has `assert result == ____` placeholders; learner fills in expected values
- [ ] Good for tier1 language fluency (operator precedence, type coercion, scope)
- [ ] Source: [gregmalcolm/python_koans](https://github.com/gregmalcolm/python_koans) (~5k stars)

### Multiple-choice question mode
- [ ] Concept-check exercises: "which of these is correct for `asyncio.gather`?"
- [ ] Source: [learnbyexample/TUI-apps](https://github.com/learnbyexample/TUI-apps) (~979 stars)

---

## Export and integration

### Jupyter dual-notebook export
- [ ] `marathon.py export-notebook NNN [--output challenge.ipynb]`
- [ ] Challenge notebook: problem statement + empty stub cell + test cell
- [ ] Solution notebook (separate): reference solution cells
- [ ] Source: [donnemartin/interactive-coding-challenges](https://github.com/donnemartin/interactive-coding-challenges) dual challenge+solution notebook model

### VS Code tasks.json integration
- [ ] `marathon.py lsp NNN` generates both `pyrightconfig.json` + `.vscode/tasks.json`
- [ ] Tasks: "Run Marathon Tests" (`marathon.py run NNN`), "Get Hint" (`marathon.py hint NNN --level 1`)
- [ ] No VS Code extension needed — pure tasks.json, works today; source: rustlings-helper approach

### Full VS Code extension
- [ ] Sidebar explorer showing exercise list with pass/fail markers
- [ ] CodeLens above `problem.py` function definitions: "Run Tests", "Get Hint"
- [ ] Ref: [Rustlings Helper](https://marketplace.visualstudio.com/items?itemName=drwilco.rustlings-helper)

### Notion database sync
- [ ] `marathon.py sync-notion --token TOKEN --db-id ID` — push exercise records to Notion
- [ ] Lower priority than Obsidian (requires OAuth, rate limits, brittle schema)

---

## Long-term / advanced

### Textual TUI
- [ ] Full reactive TUI with keyboard navigation for `marathon.py watch`
- [ ] Live-updating panel: test output + progress sidebar + hint panel
- [ ] Ref: [Textualize/textual](https://github.com/Textualize/textual), [jeffwright13/pytest-tui](https://github.com/jeffwright13/pytest-tui)

### Multi-language support
- [ ] Add Go or TypeScript exercise runner alongside pytest
- [ ] `marathon.py run NNN --lang go` invokes `go test` instead of pytest
- [ ] Progress tracks `{"001": {"python": "passed", "go": "passed"}}`
- [ ] "Solve in Python first, then port to Go" workflow for senior roles

### Docker sandbox
- [ ] Optional containerized test runner for untrusted exercise code
- [ ] Source: [numbertheory/egglings](https://github.com/numbertheory/egglings) Docker model

### Full Exercism catalog test
- [ ] Test the import pipeline against all 193 Exercism practice exercises
- [ ] Identify any that fail conversion or have Python 3.10 incompatibilities

### Architecture decision records
- [ ] Document key design choices: per-user dirs, honor-system gating, manifest format, XDG migration

---

## Explicitly not doing

These patterns exist in similar projects but are wrong for python-marathon:

- **Hearts/lives system** — penalizing hint usage hurts learning. Duolingo's own research shows this backfires.
- **Mandatory online sync** — the offline-first architecture (gitignored local JSON) is a strength.
- **Daily streak as primary metric** — streaks measure consistency, not quality. Show but don't gate features behind them.
- **Big-O auto-verification in test suite** — empirical complexity detection is too slow for the main run loop. Keep in optional `bench` command.
- **Leaderboard by raw solve count** — gamifies quantity over quality. Show tier completion instead.
- **WASM/browser execution** — adds massive infrastructure for marginal benefit over `python marathon.py`.

---

## Research references

| Project | Stars | Key feature |
|---------|-------|-------------|
| [rust-lang/rustlings](https://github.com/rust-lang/rustlings) | ~55k | `I AM NOT DONE` sentinel, inotify watch, `lsp` subcommand, interactive watch keys |
| [gregmalcolm/python_koans](https://github.com/gregmalcolm/python_koans) | ~5k | Fill-in-the-blank assertion mode, show-first-failure UX |
| [donnemartin/interactive-coding-challenges](https://github.com/donnemartin/interactive-coding-challenges) | ~31k | Anki deck export, dual challenge/solution notebook pattern |
| [textualize/rich](https://github.com/textualize/rich) | ~50k | Colored tables, progress bars, syntax highlighting |
| [open-spaced-repetition/py-fsrs](https://github.com/open-spaced-repetition/py-fsrs) | ~600 | FSRS v6 spaced repetition (outperforms SM-2) |
| [open-spaced-repetition/fsrs-optimizer](https://github.com/open-spaced-repetition/fsrs-optimizer) | — | Personal forgetting curve calibration |
| [online-judge-tools/oj](https://github.com/online-judge-tools/oj) | ~1.1k | Generator-based test case creation pipeline |
| [skygragon/leetcode-cli](https://github.com/skygragon/leetcode-cli) | ~3.8k | Problem filtering, stats, offline caching |
| [nikhil-ravi/LeetScrape](https://github.com/nikhil-ravi/LeetScrape) | ~58 | Stub + pytest generation from LeetCode, company tags |
| [exercism/problem-specifications](https://github.com/exercism/problem-specifications) | ~900 | 200+ canonical JSON test specs |
| [exercism/python-analyzer](https://github.com/exercism/python-analyzer) | — | Structured hint taxonomy (actionable/informative/celebratory) |
| [exercism/python-representer](https://github.com/exercism/python-representer) | — | AST normalization for solution deduplication + fingerprinting |
| [learnbyexample/TUI-apps](https://github.com/learnbyexample/TUI-apps) | ~979 | Multiple-choice question mode, Textual TUI |
| [bootdotdev/bootdev](https://github.com/bootdotdev/bootdev) | — | XP/levels, power tokens, XDG config, colored CLI |
| [naimulcsx/progHours](https://github.com/naimulcsx/progHours) | — | Coach analytics dashboard, group progress matrix |
| [HayesBarber/spaced-repetition-learning](https://github.com/HayesBarber/spaced-repetition-learning) | — | SM-2 for LeetCode, daily queue UX |
| [CoisiniIce/ReCode](https://github.com/CoisiniIce/ReCode) | — | Per-exercise notes, FSRS scheduling |
| [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) | — | Soul Templates (tutor personality), per-exercise tutor memory |
| [aider-chat/aider](https://aider.chat/) | ~28k | Repo-map concept, `/ask` vs `/code` mode split |
| [yangshun/tech-interview-handbook](https://github.com/yangshun/tech-interview-handbook) | — | Interview communication coaching, curated shortlists |
| [neetcode-gh/leetcode](https://github.com/neetcode-gh/leetcode) | ~6.3k | Pattern taxonomy (NeetCode roadmap), curated tracks |
| [MTrajK/coding-problems](https://github.com/MTrajK/coding-problems) | — | Multiple solution approaches with Big-O labels |
| [codecrafters-io/cli](https://github.com/codecrafters-io/cli) | — | Stage-by-stage test streaming |
| [se2p/pynguin](https://github.com/se2p/pynguin) | ~500 | Automated pytest generation from Python modules |
| [numbertheory/egglings](https://github.com/numbertheory/egglings) | — | Docker sandbox for exercise execution |
| [dpkirschner/leetcode-prep-mcp](https://github.com/dpkirschner/leetcode-prep-mcp) | — | MCP tool for fetching LeetCode problems |
| [karote00/local-leetcode-trainer](https://github.com/karote00/local-leetcode-trainer) | — | `challenge <difficulty>` random picker |
| [wislertt/leetcode-py](https://github.com/wislertt/leetcode-py) | — | LLM-assisted exercise generation |
| LLM tutoring research (Springer 2025) | — | 35% of LLM hints too direct; Socratic first-hint protocol |
