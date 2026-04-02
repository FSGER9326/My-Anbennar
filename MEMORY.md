# MEMORY.md — Jordan / Falk / Verne Overhaul

## People
- **Falk Stürmann** — Timezone: Europe/Berlin. Casual/practical tone. Works on Anbennar EU4 modding (Verne overhaul).

## Projects
- **Anbennar Verne overhaul** — `C:\Users\User\Documents\GitHub\My-Anbennar`, branch `chore/verne-10-lane-blueprint` → PR #109
- **10-column lane map** — design in ChatGPT, implementation in progress

## OpenClaw System
- **Provider:** Minimax (`minimax/MiniMax-M2.7-highspeed`) — primary model
- **ChatGPT bridge:** openclaw browser, Thinking 5.4 = DALL-E, profile=openclaw
- **9 cron jobs:** health (30min), auto-planner (4h), QA (Mon/Wed/Fri), upstream (Wed/Sun), inspiration (Mon/Thu), deep-research (Sat), extended-thinking (Tue/Fri), nightly-timeout-tuning (3am), nightly-openviking-sync (3am)
- **self-improvement-detector cron** (id: 9d21e12d-9b89-4b89-9cc2-e26bb4da0e2f) — every 6h, isolated, runs autonomous-skill-creator

## Key Infrastructure
- **Provider:** Minimax — API at `api.minimax.io/v1`
- **9 cron jobs** — health, auto-planner, QA, upstream sync, inspiration, deep-research, etc.
- **4-layer QA:** git hook + file watcher + cron + Monday retroactive
- **Verne Art project:** ChatGPT DALL-E
- **Design source of truth:** ChatGPT Modding project + downloaded chat files in `~/Downloads/`

## 10-Column Lane Map
| Lane | Theme | Slot |
|------|-------|------|
| 1 | Court & Oaths | 1 |
| 2 | Adventure Network | 2 |
| 3 | Maritime Empire | 3 |
| 4 | Dynastic Machine | 4 |
| 5 | Trade & Colonisation | 5 |
| 6 | Red Court & Arcane | 6 |
| 7 | Military Orders | 7 |
| 8 | Faith & Apostolic Empire | 8 |
| 9 | Industrial Foundries | 9 |
| 10 | Diplomacy & Liliac War Legacy | 10 |

## Autonomous Modding Addon (My-Anbennar Sheriff)
Built 2026-04-02. Bundle includes:
- `openclaw-plugin-anbennar/` — Sheriff plugin (before_prompt_build injection + anbennar.* tools)
- `hooks/anbennar-preflight/` — session-start preflight hook
- `scripts/mission_truth_audit.py` — mission ID graph + loc completeness (67 declared, 34 missing loc titles)
- `scripts/legacy_interaction_audit.py` — zzz stubs + orphan mission refs (PASSED: 0 issues)
- `scripts/registry_expand.py` — Markdown registry → JSON, fail-on-legacy-edit
- `scripts/anbennar-hotspot-explainer.py` — git diff → hotspot intersection report
- `schemas/mod-spec.schema.json` — JSON Schema for mod specs
- `scripts/pre_pr_gate.sh` — upgraded to 8 steps (added registry + mission truth audit)
- `.github/workflows/verne-validation.yml` — wired new audits into CI

## QA Status (2026-04-02)
- S01: ⚠️ Partial — expansion missions (design doc issue)
- S02: ✅ Fixed (2026-04-01)
- S03: ⚠️ Partial — Liliac War flag-gated missions
- S04: ✅ Pass
- S05: ✅ Fixed (2026-04-01)
- S06: ✅ Fixed (2026-04-01)
- S07: ✅ Pass — 117 missions with _title/_desc
- S08: ✅ Pass
- **Mission truth audit:** 67 declared, 34 missing loc title keys — ACTION REQUIRED
- **Legacy interaction audit:** PASSED

## Git State
- Workspace: `C:\Users\User\.openclaw\workspace` = My-Anbennar git repo
- Branch: `main` (was `chore/verne-10-lane-blueprint`, merged via PR #109)
- Remote: `origin` → `https://github.com/FSGER9326/My-Anbennar.git`
- Latest commits: d2e2d4f8 (fix: mission_truth_audit CRLF+regex), 6fc02ac6, 5230cb5b
- Pre-commit hook: bash script checking Paradox semicolons
- Post-commit hook: no-op batch file (removed executable bit)

## OpenViking
- Server: `http://127.0.0.1:1933` (auto-starts with Windows)

## Obsidian Vault
- Path: `C:\Users\User\Documents\Crab Memory`
- Sync script: `scripts/sync-to-obsidian.ps1` — syncs daily notes, learnings, addon scripts
- 06-Systems/My-Anbennar-Addon/INDEX.md — addon documentation
- 05-Learnings/OPENCLAW-LEARNINGS.md — merged learnings

## Lessons
- Python regex `\s` does NOT match `_` (underscore is NOT whitespace)
- Paradox mission IDs can contain lowercase letters (e.g., `A33_the_vernman_renaissance`)
- CRLF files need `.replace("\r", "")` before regex processing with `^` anchor
- `git add` on large trees (24k files) gets SIGKILL'd on constrained RAM
- `git reset --hard` on large repos takes time; run in background
- Index lock files from SIGKILL'd git processes — remove manually
- Windows console can't print emoji (cp1252 codec error) — use ASCII in print statements
- `python3` alias broken on Windows → use `python`
