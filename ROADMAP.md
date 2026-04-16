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

## Next up — High impact, minimal effort

These are pure Python, no new deps, each under ~50 lines.

### Solve-time recording
- [ ] Record `time.perf_counter()` at `marathon.py next`/`run` start, store `solve_duration_seconds` in progress JSON on pass
- [ ] Display in `marathon.py status` — actual time vs target time per exercise

### Streak tracking
- [ ] Add `streak_days` + `last_active_date` to progress JSON
- [ ] On any passing run: if `last_active_date` was yesterday, increment streak; else reset
- [ ] Show current streak in `marathon.py status`

### Random challenge picker
- [ ] `marathon.py challenge [tier]` — pick a random unsolved exercise, optionally filtered by tier
- [ ] Inspired by [local-leetcode-trainer](https://github.com/karote00/local-leetcode-trainer) "surprise me" UX

### SM-2 spaced repetition upgrade
- [ ] Replace the current `cmd_review` heuristic with proper SM-2 algorithm (~30 lines)
- [ ] Synthesize quality rating from existing signals: `quality = max(1, 5 - hints_used - (revealed * 2))`
- [ ] Store `sr_ef`, `sr_n`, `sr_interval` per exercise in progress JSON
- [ ] `marathon.py review` shows "today's review queue" with next-review dates
- [ ] Ref: [HayesBarber/spaced-repetition-learning](https://github.com/HayesBarber/spaced-repetition-learning), [supermemo2 PyPI](https://pypi.org/project/supermemo2/)

### Exercise scaffold generator
- [ ] `marathon.py new --name "slug" --tier T --tags "t1,t2" --target-minutes N`
- [ ] Creates the full 7-file directory with templates + adds manifest entry
- [ ] Generalizes `scripts/build_exercises.py` to work from CLI without notebooks

### Manifest enrichment
- [ ] Add `tags`, `prerequisites`, `difficulty` (1-10), `target_minutes` to all 41 entries in `manifest.json`
- [ ] `marathon.py tag --list` — show all tags with exercise counts
- [ ] `marathon.py tag --filter TOPIC` — list exercises matching a topic tag
- [ ] Enable tag-based recommendation in `marathon.py recommend`

### Incremental test gates
- [ ] Add `@pytest.mark.incremental` hook to `exercises/conftest.py` (~15 lines)
- [ ] Tests in a class skip after the first failure — "show one error at a time" UX
- [ ] Inspired by [python_koans](https://github.com/gregmalcolm/python_koans) and [pytest incremental docs](https://docs.pytest.org/en/stable/example/simple.html)

### Badge system
- [ ] Define badge specs in `exercises/badges.json`: slug, name, condition
- [ ] Check badges on every passing run; store earned badges in progress JSON
- [ ] Badge ideas: "Dawn Solver" (before 7am), "Clean Sweep" (no hints), "Tier Clear" (all exercises in a tier), "Speed Demon" (under half target time), "Streak 7" (7 days in a row)

### Progress export/import for cross-machine sync
- [ ] `marathon.py export > backup.json` — dump progress
- [ ] `marathon.py import backup.json --merge` — merge by taking max status, union of badges, latest timestamps
- [ ] Enables syncing between machines without git-tracking the progress file

### Obsidian vault export
- [ ] `marathon.py export-obsidian --vault PATH` — write one `.md` per solved exercise
- [ ] YAML frontmatter: tags, status, solved date, hints used, duration
- [ ] Body: problem statement + your solution in a code block
- [ ] Obsidian handles full-text search, graph view, tag navigation (~60 lines)

---

## Next up — Medium effort (optional deps or moderate work)

### Rich terminal output
- [ ] Optional `rich` dep with graceful degradation (`try: import rich`)
- [ ] `rich.table.Table` for `marathon.py status` — colored tier progress
- [ ] `rich.progress.Progress` for `marathon.py verify` — progress bar during long runs
- [ ] `rich.syntax.Syntax` for displaying `problem.py` stubs with highlighting
- [ ] `rich.panel.Panel` for exercise introductions in `marathon.py next`
- [ ] Ref: [textualize/rich](https://github.com/textualize/rich) (~50k stars)

### Activity heatmap
- [ ] GitHub-style 7xN grid of Unicode block chars (`" ░▒▓█"`) in `marathon.py status`
- [ ] Built from `first_solved` timestamps — shows solve density per week
- [ ] Pure Python, ~40 lines using only `datetime` + `collections`

### Code quality scoring
- [ ] Optional `radon` dep for cyclomatic complexity (CC) + maintainability index (MI)
- [ ] Display after each passing run: `Complexity: A (CC=3) | Maintainability: B (MI=68)`
- [ ] Composite "session score" combining tests, complexity, hints, time
- [ ] Ref: [radon](https://pypi.org/project/radon/), [xenon](https://pypi.org/project/xenon/)

### Performance benchmarking
- [ ] `marathon.py bench NNN` — timeit-based comparison against reference solution
- [ ] `.meta/bench_inputs.py` defines large inputs + threshold ratio
- [ ] Report: `Your solution: 2.3ms | Reference: 1.8ms | Ratio: 1.28x`
- [ ] Optional `big_O` dep for empirical complexity class detection
- [ ] Ref: [big_O](https://github.com/pberkes/big_O), [bigocheck](https://github.com/adwantg/bigocheck)

### Solution diff view
- [ ] `marathon.py diff NNN --user NAME` — side-by-side diff of your answer vs peer's
- [ ] Optional: AST-normalized diff (rename variables to placeholders, strip comments) inspired by [exercism/python-representer](https://github.com/exercism/python-representer)

### Leaderboard
- [ ] `marathon.py leaderboard` — reads all users' submitted answers + progress
- [ ] Sort by: tier completion, total solved, average quality score
- [ ] Deposit `stats.json` alongside `solution.py` on submit for shared metrics

### XP and level system
- [ ] Tier-weighted XP: tier1 = 10, tier2 = 25, tier3 = 100, tier4 = 50, tier5 = 15
- [ ] Bonus XP: no hints (+5), under target time (+3), streak bonus (+2/day)
- [ ] Levels 1-50 with thresholds; show in `marathon.py status`
- [ ] Inspired by [boot.dev](https://github.com/bootdotdev/bootdev) gamification

### Anki deck export
- [ ] `marathon.py export-anki` — generate `.apkg` deck from exercise metadata using `genanki`
- [ ] Front: problem name + key constraint. Back: approach name + time/space complexity
- [ ] Inspired by [donnemartin/interactive-coding-challenges](https://github.com/donnemartin/interactive-coding-challenges) which ships an Anki deck

---

## Exercise source expansion

### More Exercism
- [ ] Import medium-difficulty batch into `tier5_exercism_medium/` (anagram, binary-search, linked-list, matrix, robot-name, etc.)
- [ ] Curate a "top 30" Exercism list ordered by interview relevance
- [ ] Backfill hand-written `.meta/hints.md` for imported exercises (current ones are placeholder templates)

### Exercism problem-specifications
- [ ] `scripts/generate_from_specs.py` — auto-generate `test_problem.py` from `canonical-data.json`
- [ ] 200+ language-agnostic exercise specs with structured test cases
- [ ] Ref: [exercism/problem-specifications](https://github.com/exercism/problem-specifications) (~900 stars)

### LeetCode integration
- [ ] `scripts/import_leetcode.py` — generate stubs + pytest from LeetCode via [LeetScrape](https://github.com/nikhil-ravi/LeetScrape) (needs session cookie)
- [ ] Company tag metadata (Google, Amazon, Meta) in manifest for targeted prep
- [ ] [leetcode-prep-mcp](https://github.com/dpkirschner/leetcode-prep-mcp) — MCP tool for fetching problems dynamically

### LLM-assisted exercise generation
- [ ] `marathon.py generate "description"` — call Claude/Codex API to produce all 7 exercise files
- [ ] Validate generated solution passes generated tests before writing
- [ ] Inspired by [wislertt/leetcode-py](https://github.com/wislertt/leetcode-py) LLM-assisted creation workflow

### Generator-based test authoring
- [ ] `scripts/gen_testcases.py` — write a generator script + reference solution, auto-produce `test_problem.py`
- [ ] Inspired by [online-judge-tools/oj](https://github.com/online-judge-tools/oj) (~1.1k stars): `oj generate-input` + `oj generate-output`
- [ ] Eliminates the biggest bottleneck in adding new exercises

---

## Collaborative features

### Progress dashboard
- [ ] `marathon.py status --all` — combined view of all users' progress
- [ ] Per-exercise comparison: who solved what, relative timing

### Peer notification
- [ ] Flag in `marathon.py status` when partner has submitted a new answer you can now view
- [ ] Requires reading `answers/<peer>/` directory listing

### Shared exercise notes
- [ ] `answers/<user>/NNN/notes.md` for persistent post-solve commentary
- [ ] `/reflect` skill writes output to notes file instead of being ephemeral

### Challenge mode
- [ ] `marathon.py challenge --user PEER --exercise NNN` — create a timed challenge
- [ ] Both users solve the same exercise; compare times and approaches
- [ ] Store challenges in `answers/challenges.json`

### Discord bot
- [ ] Stateless bot reading `answers/` from git repo
- [ ] `/marathon-status @user` — embed with progress summary
- [ ] `/marathon-challenge @user NNN` — create solve challenge
- [ ] `/marathon-leaderboard` — sorted by tier completion
- [ ] ~200 lines of `discord.py`

---

## Agent tutor improvements

### Codex skill surface
- [ ] `.agents/skills/` repo-local skills as Codex equivalent to Claude slash commands
- [ ] Mirror key skills: verify, submit, peer, pull-questions

### Tutor memory
- [ ] Persist per-exercise learner context across sessions
- [ ] What they struggled with, approaches tried, common mistakes
- [ ] Inspired by [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) Soul Templates

### Structured hint taxonomy
- [ ] Replace free-form hint text with structured schema: `actionable` / `informative` / `celebratory`
- [ ] Inspired by [exercism/python-analyzer](https://github.com/exercism/python-analyzer) comment taxonomy

### Exercise-aware model switching
- [ ] Auto-suggest upgrading to Opus/GPT-4o for Tier 3-4 exercises where deeper reasoning helps
- [ ] `/model sonnet` default, `/model opus` recommended for canonical problems

### Concept curriculum DAG
- [ ] Define prerequisite relationships between exercises in manifest.json
- [ ] `marathon.py recommend` uses DAG to suggest exercises with all prereqs satisfied
- [ ] Inspired by [Exercism concept tracks](https://exercism.org/docs/building/product/concept-exercises)

---

## CLI and DX enhancements

### Inotify file watcher
- [ ] Replace mtime polling in `marathon.py watch` with `watchdog` (optional dep)
- [ ] Instant test re-run on save instead of 1-second poll
- [ ] Inspired by [rustlings](https://github.com/rust-lang/rustlings) inotify-driven watch

### LSP config generation
- [ ] `marathon.py lsp NNN` — generate pyright/pylsp config scoped to one exercise
- [ ] Avoids `from problem import *` collision across exercises in IDE
- [ ] Inspired by rustlings `lsp` subcommand

### Two-dimensional exercise addressing
- [ ] Support `marathon.py run tier2 3` alongside `marathon.py run 012`
- [ ] More natural for learners who think in tiers
- [ ] Inspired by [JayAndJef/pythonistas](https://github.com/JayAndJef/pythonistas)

### Multiple-choice question mode
- [ ] Not all exercises need to be code completion
- [ ] Concept checks: "which of these is correct for `asyncio.gather`?"
- [ ] Inspired by [learnbyexample/TUI-apps](https://github.com/learnbyexample/TUI-apps) (~979 stars)

### Kata/repeat mode
- [ ] `marathon.py kata NNN` — re-solve an exercise from scratch without using `reset`
- [ ] Tracks repetition count and time improvement across attempts
- [ ] Inspired by [matthewdeanmartin/kata-python](https://github.com/matthewdeanmartin/kata-python)

### Textual TUI
- [ ] Full reactive TUI with keyboard navigation for `marathon.py watch`
- [ ] Live-updating panel: test output + progress sidebar + hint panel
- [ ] Ref: [Textualize/textual](https://github.com/Textualize/textual), [jeffwright13/pytest-tui](https://github.com/jeffwright13/pytest-tui)

---

## Quality and testing

### CI pipeline
- [ ] GitHub Actions workflow: `marathon.py verify` on every push
- [ ] Run only on changed exercise dirs: `git diff --name-only HEAD~1`
- [ ] shields.io badge from `marathon.py stats --json` output

### Exercise linter
- [ ] `marathon.py lint-exercises` — validate all exercises have the required 7-file layout
- [ ] Check imports in test files (`from problem import *`)
- [ ] Verify stub has `raise NotImplementedError`

### Pre-commit hook
- [ ] Run `marathon.py verify` on changed exercise dirs only
- [ ] Prevents pushing broken reference solutions

### Full Exercism catalog test
- [ ] Test the import pipeline against all 193 Exercism practice exercises
- [ ] Identify any that fail conversion or have Python 3.10 incompatibilities

### Docker sandbox
- [ ] Optional containerized test runner for untrusted exercise code
- [ ] Inspired by [numbertheory/egglings](https://github.com/numbertheory/egglings) Docker model

---

## External integrations

### VS Code extension
- [ ] Sidebar explorer showing exercise list with pass/fail markers
- [ ] CodeLens above `problem.py` function definitions: "Run Tests"
- [ ] Read `.marathon_progress.json` for status coloring
- [ ] Ref: [Rustlings Helper](https://marketplace.visualstudio.com/items?itemName=drwilco.rustlings-helper)

### Jupyter notebook export
- [ ] `marathon.py export-notebook NNN` — generate `.ipynb` with problem + your solution + test results
- [ ] Uses `nbformat` to create notebook cells programmatically
- [ ] Useful for post-solve annotation and sharing

### Notion database sync
- [ ] `marathon.py sync-notion --token TOKEN --db-id ID` — push exercise records to Notion
- [ ] Lower priority than Obsidian (requires OAuth, rate limits, brittle schema)

### Multi-language support
- [ ] Add Go or TypeScript exercise runner alongside pytest
- [ ] `marathon.py run NNN --lang go` invokes `go test` instead of pytest
- [ ] Progress tracks `{"001": {"python": "passed", "go": "passed"}}`
- [ ] "Solve in Python first, then port to Go" workflow for senior roles

### FSRS upgrade
- [ ] Replace SM-2 with [py-fsrs](https://github.com/open-spaced-repetition/py-fsrs) for better-calibrated review scheduling
- [ ] FSRS outperforms SM-2 (Anki switched to FSRS as default in 23.10)
- [ ] Adds `py-fsrs` as optional dep (~1000 lines pure Python)

---

## Documentation

- [ ] Contributing guide for adding new exercises
- [ ] Exercise difficulty calibration (compare target times to actual solve data from progress JSON)
- [ ] Video walkthrough for Austin's onboarding
- [ ] Architecture decision records for key design choices (per-user dirs, honor-system gating, manifest format)

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

| Project | Stars | Key feature to steal |
|---------|-------|---------------------|
| [rust-lang/rustlings](https://github.com/rust-lang/rustlings) | ~55k | `I AM NOT DONE` sentinel, inotify watch, `lsp` subcommand, progress bar |
| [gregmalcolm/python_koans](https://github.com/gregmalcolm/python_koans) | ~5k | "Show first failing test only" UX |
| [donnemartin/interactive-coding-challenges](https://github.com/donnemartin/interactive-coding-challenges) | ~31k | Anki deck export, dual challenge/solution notebook pattern |
| [textualize/rich](https://github.com/textualize/rich) | ~50k | Colored tables, progress bars, syntax highlighting |
| [open-spaced-repetition/py-fsrs](https://github.com/open-spaced-repetition/py-fsrs) | ~600 | FSRS v6 spaced repetition (outperforms SM-2) |
| [online-judge-tools/oj](https://github.com/online-judge-tools/oj) | ~1.1k | Generator-based test case creation pipeline |
| [skygragon/leetcode-cli](https://github.com/skygragon/leetcode-cli) | ~3.8k | Problem filtering, stats, offline caching, session management |
| [nikhil-ravi/LeetScrape](https://github.com/nikhil-ravi/LeetScrape) | ~58 | Stub + pytest generation from LeetCode, company tags |
| [exercism/problem-specifications](https://github.com/exercism/problem-specifications) | ~900 | 200+ canonical JSON test specs, language-agnostic |
| [exercism/python-analyzer](https://github.com/exercism/python-analyzer) | — | Structured hint taxonomy (actionable/informative/celebratory) |
| [exercism/python-representer](https://github.com/exercism/python-representer) | — | AST normalization for solution diffing |
| [learnbyexample/TUI-apps](https://github.com/learnbyexample/TUI-apps) | ~979 | Multiple-choice question mode, Textual TUI |
| [bootdotdev/bootdev](https://github.com/bootdotdev/bootdev) | — | XP/levels, achievement system, colored CLI |
| [HayesBarber/spaced-repetition-learning](https://github.com/HayesBarber/spaced-repetition-learning) | — | SM-2 for LeetCode, daily queue UX |
| [CoisiniIce/ReCode](https://github.com/CoisiniIce/ReCode) | — | Per-exercise notes, FSRS scheduling, Monaco editor |
| [karote00/local-leetcode-trainer](https://github.com/karote00/local-leetcode-trainer) | — | `challenge <difficulty>` random picker |
| [wislertt/leetcode-py](https://github.com/wislertt/leetcode-py) | — | LLM-assisted exercise generation, data structure visualization |
| [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) | — | Soul Templates (tutor personality), per-exercise tutor memory |
| [aider-chat/aider](https://aider.chat/) | ~28k | Repo-map concept, `/ask` vs `/code` mode split |
| [se2p/pynguin](https://github.com/se2p/pynguin) | ~500 | Automated pytest generation from Python modules |
| [numbertheory/egglings](https://github.com/numbertheory/egglings) | — | Docker sandbox for exercise execution |
| [dpkirschner/leetcode-prep-mcp](https://github.com/dpkirschner/leetcode-prep-mcp) | — | MCP tool for fetching LeetCode problems |
