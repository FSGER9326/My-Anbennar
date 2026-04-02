# Auto-Planner: Cron Job Status & On-Demand Triggers

Track cron job health and provide on-demand trigger capability.

## Active Jobs (10 total)

| Name | Schedule | Next Run (Berlin) | Status | Notes |
|------|----------|-------------------|--------|-------|
| health-monitor | Every 30 min | ~17:00 | ⚠ CLI broken (EPERM) | Gateway healthy, CLI corrupted. Fix: run npm update as admin. |
| auto-planner | Every 4h | ~20:00 | ✅ OK | Gateway healthy |
| obsidian-sync | Every 30 min | ~17:00 | ✅ OK | Running well |
| verne-qa-check | Mon/Wed/Fri 2 AM | Fri 02:00 | ⚠️ false-error | Ran Wed 18:40 (manual trigger), found 40+ missing tooltips. Cron status shows error but run succeeded. |
| anbennar-upstream-sync | Wed/Sun 10 AM | Sun 10:00 | ⚠ Partial | Timed out at 181s but generated full report |
| mod-inspiration-scout | Mon/Thu 8 PM | Thu 20:00 | ✅ OK | — |
| chatgpt-extended-thinking | Tue/Fri 6 PM | Fri 18:00 | ✅ OK | — |
| chatgpt-deep-research | Saturday 2 PM | Sat 14:00 | ✅ OK | — |
| nightly-timeout-tuning | Daily 3 AM | Thu 03:00 | ✅ OK | Cron added 2026-04-01 |
| nightly-openviking-sync | Daily 3 AM | Thu 03:00 | ✅ OK | Cron added 2026-04-01 |

## System Audit (2026-04-01 18:45)

### Fixed This Session
- **Model dropdown** — clawzempic removed, only Minimax models remain
- **Git pre-commit hook** — PowerShell QA hook installed, core.hooksPath configured
- **S05 typos** — Already fixed in prior commit (4d86b61b78)
- **CLI --version** — Working again (2026.3.28, f9b1079)
- **entry.js** — Patched run-main-WhPPYnun.js -> run-main-Cv4tme_8.js

### Needs Admin Rights (EPERM-blocked)
1. **CLI full update** — npm update -g openclaw -> EPERM on C:\Program Files\nodejs\
2. **memory-lancedb fix** — vectordb npm package can't install to system directory
3. **OpenClaw 2026.3.31** — Can't upgrade from 2026.3.28

### Cascading Hash Corruption
The failed npm update left entry.js with 2026.3.31-era hashes referencing non-existent files:
- Gateway: ✅ Healthy ({"ok":true,"status":"live"})
- CLI --version: ✅ Works
- CLI status/doctor: ❌ Broken (missing provider-onboard-B0AuPavZ.js etc.)
- Memory plugin: ⚠ Unavailable (vectordb not installed)

### What Works
Gateway, all cron jobs, subagent execution, browser tool, memory files, docs, skills, scripts, OpenViking, Ollama

### Admin Fix
Run PowerShell as Administrator, then: npm update -g openclaw

## Recent Run Results

### anbennar-upstream-sync (ran Wed 10:00)
- Timed out at 181s but generated full report
- Key finding: commit 5cb66b5f (PR !3980) modifies Verne loc
- Safe merges available: ~15 commits

### health-monitor (pattern over 12h)
- ~50% timeout rate at 300s limit
- Cause: memory_lancedb plugin missing vectordb causes CLI hangs
- Works when gateway is responsive, times out during plugin load failures
- Status: Acceptable — gateway runtime unaffected

### verne-qa-check (last ran Mon 20:00)
- Found 40+ missing tooltip/localisation keys
- Syntax, modifiers, chain logic, lore: pass
- Delivery switched from announce to none

## On-Demand Triggers

| Trigger | Command |
|---------|---------|
| "Run QA now" | openclaw cron run 899e270a-14d3-4fae-98df-d027b0435bea |
| "Check upstream" | openclaw cron run a82b645a-0ec2-4c9a-9410-a175090c7d49 |
| "Find inspiration" | openclaw cron run 7e1b3da2-92ef-468f-b756-6af248a3adfe |
| "Analyze architecture" | openclaw cron run 609b2d33-f9b1-412d-9211-3ad8d43ed7a4 |
| "Deep research" | openclaw cron run 5238600d-6308-4332-a92c-cf5556f76b01 |
| "Health check now" | openclaw cron run 4e9fbcbb-cc30-441a-9ebd-81bab6f872d8 |

## Last Auto-Check
- Date: 2026-04-01 20:03
- Jobs: 10 active, 2 triggered manually (verne-qa-check, anbennar-upstream-sync)
- Health: Gateway healthy, memory-lancedb still disabled
- verne-qa-check: false error flag — actual run succeeded (18:40, 40+ missing tooltips found)
- anbennar-upstream-sync: re-triggered manually (timed out at 181s but generated report)
- Pending: Admin npm update for full CLI fix, memory-lancedb vectordb install
- Next check: ~22:00
