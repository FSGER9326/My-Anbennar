# Background Worker Protocol

When the main session is idle (heartbeat or nothing happening), subagents
automatically work through pending Verne modding tasks.

**Architecture:** See `docs/self-enhancement-architecture.md` for full integration.

## How It Works

1. Heartbeat fires → check if main session is idle (no active conversation)
2. If idle AND there's pending work: spawn a background subagent
3. If already running a background subagent: skip (don't spawn duplicates)
4. Subagent reports completion → update roadmap, daily notes, trial log
5. Every 5th cycle → run self-improvement (Priority 5)

## Idle Detection

Main session is considered idle when:
- Heartbeat fires (nothing to respond to)
- No active subagent running (check sessions_list)
- No pending human input needed
- Last human message was >5 minutes ago

## Background Task Queue

Priority-ordered list of tasks to work through when idle:

### Priority 1: Critical path (blocks everything)
- [x] ~~Fix verne_mission_start flag~~ ✅ Done by bg worker (1m49s)
- [x] ~~Fix verne_royal_arbitration_complete flag~~ ✅ Done
- [x] ~~Fix reform name typos~~ ✅ Done (2 fixes)
- [x] ~~Fix lane4 reform references~~ ✅ Done
- [x] ~~Remap 5 conflicting positions (Lane 1, 4)~~ ✅ Done
- [x] ~~Remap 6 remaining position conflicts (Lane 3, 5, 8)~~ ✅ Done
- [x] ~~Write modifier definitions file (verne_overhaul_modifiers.txt)~~ ✅ Already exists (4134 bytes)
- [x] Write localisation skeleton file ✅ Done (2026-04-01 03:12)

### Priority 2: Quality & completeness
- [x] ~~Run full QA compliance scan on all lane design files~~ ✅ Done 2026-04-01 02:40
- [ ] Generate remaining 11 GFX assets via ChatGPT (needs human — browser)
- [x] ~~Verify all government reform references exist in the codebase~~ ✅ Done 2026-04-01 03:05

### Priority 3: Knowledge & improvement
- [x] Sync daily memory to Obsidian vault (`C:\Users\User\Documents\Crab Memory\Daily Notes\`) ✅ 2026-04-01
- [x] Sync learnings to vault (`Crab Memory\Learnings\`) ✅ 2026-04-01
- [x] Update knowledge base pages in vault with latest project status ✅ 2026-04-01
- [ ] Scan more modding pages from wiki (decisions, scripting tutorial)
- [x] ~~Research additional mod inspiration (check Paradox forums, Steam Workshop)~~ ✅ Done 2026-04-01 14:14 (8 entries in docs/inspiration-bank.md)
- [x] ~~Review and consolidate .learnings/ into MEMORY.md~~ ✅ Done 2026-04-01 09:32
- [x] Check Anbennar upstream for new commits since last sync ✅ 2026-04-01 07:31

### Priority 4: Polish & documentation
- [ ] Upload reference files to ChatGPT Verne Art project (VerneArtPack)
- [ ] Create Verne Research project in ChatGPT with wiki references
- [x] ~~Review tooltip compliance on all design docs (standards S01-S05)~~ ✅ Done 2026-04-01 11:38 (17 issues found — see docs/tooltip-compliance-report.md)
- [ ] Update roadmap with current status

### Priority 5: Self-improvement (run every 5th background cycle)
- [ ] Run autonomous skill creator — scan history for repeated patterns
- [ ] Check Trial Log in `docs/subagent-patterns.md` — consolidate learnings
- [ ] Review `.learnings/` files for promoted patterns (3+ occurrences)
- [ ] Update delegation matrix and timeout guidelines
- [ ] Archive completed tasks, add newly discovered ones
- [ ] Review background worker protocol itself — any inefficiencies?

## Auto-progress Rules

Background subagents should:
1. Pick the HIGHEST priority pending task
2. Complete it fully (not half-done)
3. Update the relevant files
4. Log results to daily notes + update roadmap status
5. NOT announce to human unless: critical finding, task completed, or blocked

## Self-Improvement Protocol (after each task)

### 1. Evaluate itself (use subagent-patterns.md criteria)
- Scope fit, Speed, Quality/Correctness, Self-sufficiency, Tokens (1-5 each)
- If reusability score ≥9 → flag as skill candidate
- Log trial to `docs/subagent-patterns.md` Trial Log

### 2. Update the task queue
- Mark completed tasks
- If a task revealed new subtasks, add them
- If priority order should change, update it
- If a task type consistently scores low, flag for main session

### 3. Knowledge capture
- New pattern → update `docs/subagent-patterns.md`
- Error → log to `.learnings/ERRORS.md`
- Standard/correction → update `.learnings/LEARNINGS.md` or `docs/verne-standards-tracker.md`
- Roadmap changed → update `docs/verne-roadmap.md`

### 4. Skill creation (every 5th cycle or 3+ same-type tasks)
- Check `skills/autonomous-skill-creator/SKILL.md` for protocol
- Run repetition, code pattern, and complexity detectors
- If skill created → embed description in memory search
- Log to `skills/self-improving-agent/ledger.md`

### 5. Queue optimization (every 3 completed tasks)
- Are priorities still correct?
- Are any tasks blocked that we could unblock?
- Should any tasks be split or merged?
- Is queue length manageable?
