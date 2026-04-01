# Self-Improvement Implementation Plan
**Based on:** Deep Research (ChatGPT, 31 citations, 371 searches) + web research (agent-memory-vault, OpenClaw+CouchDB, MCPVault)
**Created:** 2026-04-01 12:36 CET

---

## Problem 1: Memory Decay Across Sessions

### Current State
- OpenClaw daily files + MEMORY.md survive compaction
- Obsidian vault synced every 30min (new today)
- OpenViking knowledge graph exists but nothing writes to it

### What Research Says
The winning pattern is **3-layer memory** (from jimmytherobot + LangChain):
1. **Thread memory** (session-scoped) — recent conversation, in-progress work
2. **Summary memory** (periodic) — distilled facts, decisions, behavioral notes
3. **Index memory** (long-term) — searchable knowledge graph, entity relationships

### Actions
- [x] **Done today:** Added "CAPTURE DECISIONS IMMEDIATELY" to AGENTS.md
- [x] **Done today:** Sync script writes daily files to Obsidian every 30min
- [x] **Done today:** CORE_MEMORY.md created (Letta-style pinned blocks: persona, human, project_state, active_work)
- [x] **Done today:** SESSION_HANDOFF.md created — compact reasoning state written at session end
- [x] **Done today:** AGENTS.md startup loads CORE_MEMORY + SESSION_HANDOFF; session-end protocol added
- [x] **Done today:** MEMORY.md trimmed and updated with Deep Research findings
- [x] **Done today:** OpenViking API tested — session write working, scripts/openviking-write.ps1 created
- [ ] **Next session:** Auto-write key decisions to OpenViking at end of session

---

## Problem 2: Subagent Learning Loop

### Current State
- Trial log with 13 entries, 10-dimension scoring
- Timeout Tuning Table added to subagent-patterns.md (today)
- AGENTS.md has pre-spawn check instructions

### What Research Says
Production systems use **closed-loop feedback**: task result → metrics → parameter adjustment → next task. The key insight: parameters should be data-driven, not manually set.

### Actions
- [x] **Done today:** Timeout Tuning Table with learned values (design doc rewrite: 900s→1500s)
- [x] **Done today:** Pre-spawn check instructions in AGENTS.md
- [ ] **Next:** Add auto-parameter tuning — before spawning, the main agent reads the Timeout Tuning Table and applies the tuned values automatically
- [ ] **Next:** After each subagent completes, automatically evaluate and update the table if timeout was wrong
- [ ] **Future:** When a pattern reaches 3+ occurrences with avg score ≥4.0, auto-generate a skill SKILL.md

---

## Problem 3: Skill Creation from Patterns

### Current State
- Autonomous skill creator exists but never fired (0 creations in ledger)
- Detection criteria: 3+ occurrences, reusability ≥9

### What Research Says
The threshold of "reusability ≥9" is too high for initial detection. Better approach:
1. **Lower threshold** to ≥4 occurrences for "emerging skill" flag
2. **Score each pattern** on reusability after each occurrence
3. **Auto-create** only when score is stable ≥4.0 across 3+ runs

### Actions
- [x] **Done today:** Logged that QA compliance fix pattern has 3 occurrences (trials 10-11-12)
- [x] **Done today:** Trajectory-based detection pattern documented (normalize tool sequences, count abstracted patterns)
- [ ] **Next:** Instrument subagent runs with normalized action/tool sequence logging
- [ ] **Next:** Implement n-gram frequency counter for pattern detection
- [ ] **Next session:** QA compliance fixes is the first skill candidate — next occurrence triggers auto-creation

---

## Problem 4: Knowledge Graph Integration

### Current State
- OpenViking server running at http://127.0.0.1:1933
- Has endpoints: search, sessions, relations, content, skills, roles
- Nothing writes to it

### What Research Says
Knowledge graphs work best for **entity relationships** — "Falk works on Verne", "Verne uses lane 10 structure", "lane 10 contains mission A33_lilliacy". This complements flat files (daily notes) with structured, queryable connections.

### Actions
- [x] **Done today:** OpenViking API tested — health, sessions, fs/ls, commit all working
- [x] **Done today:** Session c188967b created with 3 committed facts (decisions, tasks, learnings)
- [x] **Done today:** Write script created: scripts/openviking-write.ps1
- [x] **Done today:** Decided data placement:
  - Daily files = chronological session logs (OpenClaw)
  - Obsidian = human-browseable knowledge + MOCs (synced every 30min)
  - OpenViking = entity relationships + searchable facts (via write script)
- [ ] **Next:** Build nightly cron that writes key daily file content to OpenViking
  - Daily files = chronological session logs
  - Obsidian = human-browseable knowledge + MOCs
  - OpenViking = entity relationships + searchable facts
- [ ] **Future:** Write a sync script that pushes key facts from daily files to OpenViking

---

## Problem 5: Context Compression Without Loss

### Current State
- OpenClaw compacts when context gets too long
- MEMORY.md is designed as a "lifeboat" but may be too large
- Daily files survive compaction

### What Research Says
The "lifeboat" document should be:
1. **Small** (< 2KB) — fits within any remaining context
2. **Structured** — clear sections the model can quickly parse
3. **Current** — updated after every major work session
4. **Behavioral** — includes rules, not just facts

LangChain's approach: "summary memory" — periodically summarize conversation into a compact fact sheet that gets injected into the next session.

### Actions
- [x] **Done today:** MEMORY.md updated with current project state, 10-column map, key decisions
- [x] **Done today:** CORE_MEMORY.md created as the actual lifeboat (3.9KB, 4 pinned blocks)
- [x] **Done today:** SESSION_HANDOFF.md as ReSum-style compact reasoning state
- [x] **Done today:** AGENTS.md startup + session-end protocols updated

---

## Priority Status (updated 2026-04-01 13:00)

| Priority | Task | Status |
|----------|------|--------|
| 1 | Session-end summary protocol | ✅ Done (AGENTS.md + SESSION_HANDOFF.md) |
| 2 | Core memory lifeboat | ✅ Done (CORE_MEMORY.md, 4 pinned blocks) |
| 3 | OpenViking API test | ✅ Done (session write working, script created) |
| 4 | Auto-parameter tuning | ✅ Started (Timeout Tuning Table in subagent-patterns.md) |
| 5 | OpenViking sync from daily files | ⏳ Next session (nightly cron) |
| 6 | Skill candidate detection | ⏳ Next session (trajectory-based) |
| 7 | Reflexion-style learning | ⏳ Next session (reflection stubs) |
| 8 | Auto-parameter promotion | ⏳ Next session (nightly cron promotes tuned params) |
