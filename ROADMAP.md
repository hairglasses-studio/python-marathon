# python-marathon Roadmap

## Done

### Exercise bank (61 exercises)
- [x] 31 original exercises across 4 tiers (openai-prep + hand-written async)
- [x] 10 Exercism easy exercises (tier5_exercism_easy, 032-041)
- [x] 20 Exercism medium exercises (tier5_exercism_medium, 042-061)
- [x] `exercises/manifest.json` — tags, difficulty, target_minutes on all 61
- [x] `scripts/import_exercism.py` — import pipeline with dry-run, auto-renumber
- [x] `scripts/generate_from_specs.py` — auto-generate tests from `canonical-data.json`
- [x] `scripts/backfill_manifest.py` — one-shot manifest generator
- [x] All 61 exercises verified passing under Python 3.10

### CLI runner (33 subcommands)
- [x] Core: `status`, `run`, `next`, `list`, `watch`, `hint`, `reveal`, `reset`
- [x] Collaboration: `submit [--git]`, `peer`, `challenge-peer`, `peer-status`, `diff`, `leaderboard`
- [x] Discovery: `tag [--filter]`, `recommend`, `challenge [--tier]`, `badges`
- [x] Gamification: `kata`, SM-2 `review`, `stats [--json]`
- [x] Export: `export`, `import-progress`, `export-obsidian`
- [x] Admin: `verify [--changed-only]`, `lint-exercises`, `new`, `import`, `completion`, `doctor`, `shell`, `deps`, `migrate`

### Multi-user collaborative learning
- [x] Per-user identity (`.marathon_user`), namespaced progress JSON
- [x] `answers/` directory tracked in git, per-user subdirectories
- [x] Claude Code deny rules on `answers/**`

### Multi-agent tutor support
- [x] Claude Code: full harness (deny rules + 13 slash commands)
- [x] Codex CLI: `.codex/config.toml` + `.agents/skills/` (4 skills)
- [x] Gemini CLI: `.gemini/settings.json` context bridge
- [x] GitHub Copilot: `.github/copilot-instructions.md`

### Budget model configuration
- [x] Claude: Sonnet 4.6 (Claude Pro $20/mo)
- [x] Codex: o3-mini (ChatGPT Plus $20/mo)
- [x] Gemini: Flash 2.5 free tier

### Gamification and progress
- [x] Solve-time recording, streak tracking, activity heatmap
- [x] 16 badges (`badges.json`), XP/levels (50 levels), SM-2 spaced repetition
- [x] `# MARATHON: NOT DONE` sentinel (rustlings pattern)
- [x] Progress schema versioning (v2) + `migrate` command
- [x] Incremental test gates (`@pytest.mark.incremental`)

### CI, quality, and DX
- [x] `.github/workflows/verify.yml` (Python 3.10/3.11/3.12 matrix)
- [x] `scripts/pre-commit` + `verify --changed-only`
- [x] Man page, zsh completions (307 lines), Makefile
- [x] `.python-version` pinned 3.10, getting-started README
- [x] CONTRIBUTING.md

---

## P0 — Bug fixes

- [ ] **Hints backfill (032-061)** — 30 Exercism exercises have boilerplate hints; generate substantive 3-level hints from README + test content *(LLM-assisted, ~30 exercises)*

---

## P1 — High impact, zero new deps (stdlib only)

Each item is shippable in one dev-loop iteration.

- [ ] **Keystroke watch mode** — `termios`/`select` raw-mode in `watch`: keys `h`=hint, `l`=list, `r`=rerun, `n`=next, `q`=quit, `?`=help
- [ ] **Self-report quality rating** — after review solve, prompt `[0=forgot 1=hard 2=ok 3=easy]` via `termios`; feed into SM-2 quality
- [ ] **Pattern taxonomy** — add `"pattern"` field to manifest; `marathon.py pattern` lists patterns; `next --pattern X` filters
- [ ] **Named curated shortlists** — `curations.json` with `blind75`, `async-mastery`, etc.; `list --curated NAME`; `next --curated NAME`
- [ ] **Concept prerequisite DAG** — `"prereqs"` in manifest; `recommend` upgrades to topo-sort; `marathon.py map NNN` prints chain
- [ ] **Company tags** — add `"companies"` to manifest; `list --company google`
- [ ] **LSP config generation** — `marathon.py lsp NNN` generates `pyrightconfig.json` per exercise
- [ ] **Shared exercise notes** — `answers/<user>/NNN/notes.md`; `marathon.py notes NNN` opens in `$EDITOR`; `/reflect` writes to it
- [ ] **`status --all`** — combined multi-user progress view
- [ ] **Peer notification** — flag in `status` when partner has new viewable answers
- [ ] **stats NNN** — per-exercise aggregate from peer `answers/` files
- [ ] **shields.io badge** — CI writes `stats --json` to gist; badge in README
- [ ] **Linter improvements** — check hints.md sections, notes.md exists, README sections, manifest completeness, test function count
- [ ] **Tier certificate** — `marathon.py certificate --tier N` generates SVG via `xml.etree.ElementTree`
- [ ] **Power tokens** — streak reward; bypass XP penalty on reveal/hint
- [ ] **Kata history sparkline** — `kata_history` array in progress; `kata NNN --history` shows improvement
- [ ] **Hot streak XP multiplier** — 1.5x XP if ≥5 solves in <30 min session
- [ ] **Structured Socratic hint protocol** — update `hint.md` skill: L1=question, L2=statement, L3=code fragment
- [ ] **Document pre-commit in CONTRIBUTING.md**

---

## P2 — Medium effort (optional deps or moderate work)

- [ ] **Rich terminal output** — optional `rich` dep; colored `status` table, `verify` progress bar, syntax-highlighted stubs *(rich is installed)*
- [ ] **Inotify file watcher** — optional `watchdog` dep for instant rerun in `watch` *(watchdog is installed)*
- [ ] **Code quality scoring** — optional `radon` dep; CC + MI grades after each pass
- [ ] **Performance benchmarking** — `marathon.py bench NNN`; `timeit` comparison vs reference; optional `big_O`
- [ ] **FSRS upgrade** — replace SM-2 with `py-fsrs` for better scheduling; optional dep
- [ ] **FSRS weight optimizer** — `marathon.py fsrs-optimize`; personal forgetting curve calibration
- [ ] **Forgetting curve visualization** — `marathon.py curve NNN`; sparkline of predicted retention
- [ ] **Review session discipline** — `review --session` locks until all due items done
- [ ] **Anki deck export** — `marathon.py export-anki`; optional `genanki` dep
- [ ] **AST-normalized diff** — normalize variable names in `diff` output
- [ ] **Kyu/Dan rank system** — skill rank separate from XP level
- [ ] **Property-based testing** — `.meta/test_pbt.py` with Hypothesis; `run --pbt`
- [ ] **Stage-by-stage test streaming** — custom pytest plugin; print results as they complete
- [ ] **Hidden test tier** — `.meta/test_hidden.py` for CI-only adversarial tests
- [ ] **Coach dashboard** — `marathon.py coach --users X,Y`; side-by-side progress matrix
- [ ] **AST solution fingerprinting** — hash `ast.dump` on submit; detect matching approaches
- [ ] **Group timed events** — `marathon.py event create/status`; mini-leaderboard
- [ ] **Deposit stats.json on submit** — shared metrics per submitted answer

---

## P3 — Content and sources

- [ ] **LLM-assisted hints backfill** — `scripts/gen_hints.py` for Exercism exercises
- [ ] **LLM-assisted exercise generation** — `new --from-description`; Claude generates 7-file scaffold
- [ ] **LeetCode import** — `scripts/import_leetcode.py` via LeetScrape *(needs session cookie)*
- [ ] **Codeforces import** — `scripts/import_codeforces.py` from public problem pages
- [ ] **Generator-based test authoring** — `scripts/gen_testcases.py` (oj pattern)
- [ ] **Multiple solution approaches** — `.meta/solution_brute.py` + `solution_optimal.py`
- [ ] **Further reading links** — `## Learn More` in hints.md
- [ ] **Koans-style fill-in-blank tier** — `assert result == ____` placeholders
- [ ] **Multiple-choice question mode** — concept checks
- [ ] **Seasonal challenge mode** — `marathon.py season create` (AoC-style)

---

## P4 — Long-term / infrastructure

- [ ] **XDG Base Directory compliance** — move progress to `$XDG_DATA_HOME/marathon/`
- [ ] **Plugin/hook system** — `~/.config/marathon/hooks/` with `on_pass`, `on_badge_earn`, etc.
- [ ] **User config file** — `marathon.py config` reading `~/.config/marathon/config.toml`
- [ ] **Textual TUI** — full reactive terminal UI for watch mode
- [ ] **Multi-language support** — Go/TypeScript runners alongside pytest
- [ ] **Docker sandbox** — containerized test runner
- [ ] **VS Code tasks.json** — `lsp NNN` generates `.vscode/tasks.json`
- [ ] **Full VS Code extension** — sidebar explorer with pass/fail markers
- [ ] **Jupyter dual-notebook export** — challenge + solution notebooks
- [ ] **Notion sync** — `sync-notion --token`
- [ ] **Full Exercism catalog test** — verify import pipeline against all 193 exercises
- [ ] **Architecture decision records**
- [ ] **Tutor memory** — persist per-exercise learner context across sessions
- [ ] **Interview simulation** — `marathon.py interview NNN` with Claude as interviewer
- [ ] **Exercise-aware model switching** — auto-suggest Opus for tier3-4

---

## Explicitly not doing

- **Hearts/lives system** — penalizing hints hurts learning
- **Mandatory online sync** — offline-first is a strength
- **Daily streak as primary metric** — show, don't gate
- **Big-O auto-verification in test suite** — too slow; keep in `bench`
- **Leaderboard by raw solve count** — show tier completion instead
- **WASM/browser execution** — marginal benefit over CLI

---

## Research references

| Project | Stars | Key feature |
|---------|-------|-------------|
| [rustlings](https://github.com/rust-lang/rustlings) | ~55k | sentinel, inotify watch, interactive keys, lsp |
| [python_koans](https://github.com/gregmalcolm/python_koans) | ~5k | fill-in-blank, show-first-failure |
| [interactive-coding-challenges](https://github.com/donnemartin/interactive-coding-challenges) | ~31k | Anki deck, dual notebooks |
| [rich](https://github.com/textualize/rich) | ~50k | colored tables, progress bars |
| [py-fsrs](https://github.com/open-spaced-repetition/py-fsrs) | ~600 | FSRS v6 (outperforms SM-2) |
| [oj](https://github.com/online-judge-tools/oj) | ~1.1k | generator-based test creation |
| [leetcode-cli](https://github.com/skygragon/leetcode-cli) | ~3.8k | filtering, stats, offline cache |
| [LeetScrape](https://github.com/nikhil-ravi/LeetScrape) | ~58 | stub+pytest from LeetCode |
| [problem-specifications](https://github.com/exercism/problem-specifications) | ~900 | 200+ canonical JSON specs |
| [python-analyzer](https://github.com/exercism/python-analyzer) | — | hint taxonomy |
| [python-representer](https://github.com/exercism/python-representer) | — | AST normalization |
| [bootdev](https://github.com/bootdotdev/bootdev) | — | XP, tokens, XDG config |
| [DeepTutor](https://github.com/HKUDS/DeepTutor) | — | tutor memory, soul templates |
| [tech-interview-handbook](https://github.com/yangshun/tech-interview-handbook) | — | curated shortlists, communication coaching |
| [neetcode/leetcode](https://github.com/neetcode-gh/leetcode) | ~6.3k | pattern taxonomy, curated tracks |
