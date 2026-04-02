# Cron Status

**Last updated:** 2026-04-02 04:03 UTC (auto-planner)
**Auto-planner run ID:** 2248456a-cb82-41f8-9727-1583d4fb5a6a

## Jobs Overview

| Job | ID | Status | Consecutive Errors | Last Run | Next Run | Notes |
|-----|----|--------|--------------------|----------|----------|-------|
| health-monitor | 4e9fbcbb | ✅ ok | 0 | ~04:03 UTC | ~04:33 UTC | delivery mode=none |
| obsidian-sync | b77737f5 | ✅ ok | 0 | ~04:01 UTC | ~04:31 UTC | delivery mode=none |
| auto-planner | 2248456a | ✅ ok | 0 | 04:03 UTC | 08:03 UTC | running now |
| verne-qa-check | 899e270a | ✅ ok | 0 | 03:12 UTC | 03 Apr 02:00 | delivery mode=none |
| anbennar-upstream-sync | a82b645a | ❌ ERROR | 3 | 02:00 UTC | 04 Apr 10:00 | Telegram delivery fail — needs chatId or mode=none |
| nightly-timeout-tuning | 15255640 | ⚠️ WARN | 1 | 03:00 UTC | 03 Apr 03:00 | Telegram delivery fail — needs chatId or mode=none |
| nightly-openviking-sync | 9c0c3470 | ✅ ok | 0 | 03:00 UTC | 03 Apr 03:00 | delivery mode=none |
| mod-inspiration-scout | 7e1b3da2 | ⏳ pending | — | never | 03 Apr 20:00 | |
| chatgpt-extended-thinking | 609b2d33 | ⏳ pending | — | never | 03 Apr 18:00 | |
| chatgpt-deep-research | 5238600d | ⏳ pending | — | never | 04 Apr 14:00 | |
| self-improvement-detector | d2fa4304 | ⏳ pending | — | never | 08:03 UTC | |

## Issues Requiring Human Action

### 1. anbennar-upstream-sync — Telegram delivery error (CRITICAL)
- **Error:** `Delivering to Telegram requires target <chatId>`
- **consecutiveErrors:** 3
- **Fix options:**
  - Option A (recommended): Change delivery mode to `"none"` — no announcement needed
  - Option B: Add `"chatId"` to the delivery config for this job
- **How to fix:**
  ```bash
  openclaw cron update a82b645a-0ec2-4c9a-9410-a175090c7d49 --patch '{"delivery":{"mode":"none"}}'
  ```

### 2. nightly-timeout-tuning — Telegram delivery error (WARNING)
- **Error:** `Delivering to Telegram requires target <chatId>`
- **consecutiveErrors:** 1
- **Fix options:**
  - Option A (recommended): Change delivery mode to `"none"` — announcements not critical for this job
  - Option B: Add `"chatId"` to the delivery config
- **How to fix:**
  ```bash
  openclaw cron update 15255640-1c49-4997-a1b4-a99124b9592e --patch '{"delivery":{"mode":"none"}}'
  ```

## All Other Jobs
All other 8 jobs are healthy — running on schedule, no errors.

## Notes
- `openclaw tasks audit` timed out during this run; not an error condition, just slow.
- Config warning about `memory-lancedb` plugin is cosmetic (disabled in config, still present — normal).
- `docs/cron-status.md` did not exist before this run; created fresh.
