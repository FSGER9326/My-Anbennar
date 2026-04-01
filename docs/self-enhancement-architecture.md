# Self-Enhancement Architecture

**How skills, memory, subagents, compression, and modding work as one system.**

---

## The Loop

```
   ┌─────────────────────────────────────────────────────┐
   │                  WORK happens                        │
   │  (background worker, subagent, main session)         │
   └────────────────────────┬────────────────────────────┘
                            │
                   ┌────────▼────────┐
                   │  DATA captured  │
                   │  trial logs     │
                   │  errors         │
                   │  patterns       │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │  LEARN & DETECT │
                   │  subagent       │
                   │  .learnings/    │
                   │  trial log      │
                   └────────┬────────┘
                            │
              ┌─────────────▼─────────────┐
              │  Pattern detected 3+ times │
              │  High reusability score    │
              │  Same action repeated      │
              └─────────────┬─────────────┘
                            │
              ┌─────────────▼─────────────┐
              │  SKILL created             │
              │  (autonomous-skill-creator │
              │   or self-improving-agent) │
              └─────────────┬─────────────┘
                            │
              ┌─────────────▼─────────────┐
              │  Skill INSTALLED           │
              │  • Embedded in memory      │
              │  • Available to subagents  │
              │  • Referenced in compressed│
              │    context                 │
              └─────────────┬─────────────┘
                            │
              ┌─────────────▼─────────────┐
              │  Next work cycle:          │
              │  Skill auto-loaded →       │
              │  Better template →         │
              │  Faster, higher quality    │
              └───────────────────────────┘
```

---

## Integration Points

### 1. Skill Creation ↔ Memory

**Skills are embedded into memory-lancedb on creation:**

- Skill description becomes searchable semantic content
- "How do I write a Verne mission?" → finds `eu4-lane-writer` skill automatically
- Memory search returns skills alongside notes and learnings
- Skills reference memory: `[Context: See MEMORY.md section on Verne identity]`

**Implementation:** When a skill is created, add its description to memory search via:
```
memory-lancedb embed skills/<name>/SKILL.md
```

### 2. Skill Creation ↔ Context Compression

**Instead of compressing procedures, extract them as skills:**

Before compression:
> "We wrote another mission file. Used the same pattern: has_country_flag trigger, addProvinceModifier effect, tooltip with lore text..."

After compression with skills:
> "Wrote mission file using EU4 lane writer skill (skills/eu4-lane-writer/). Context: Silver Oaths chain, Lane 1."

**Token savings:** Compressed context references skills instead of repeating procedures.
**Quality gain:** Next time the same procedure is needed, the skill is loaded with full detail.

### 3. Skill Creation ↔ Subagent Work

**Subagent trials feed skill creation:**

| Trial Result | Action |
|-------------|--------|
| Reusability 10/10, 3+ occurrences | → Auto-create skill |
| Reusability 8-9/10, 5+ occurrences | → Flag as skill candidate |
| Reusability 1-6/10 | → Keep as one-off, no skill |

**Subagent output improvements from skills:**
- Skill provides template → subagent starts with more context
- Less prompting needed → fewer tokens in/out
- More consistent output → higher quality scores

### 4. Skill Creation ↔ Modding

**Verne-specific patterns that become skills:**

| Pattern | Skill Name | Trigger |
|---------|------------|---------|
| Lane design doc writing | `verne-lane-writer` | Writing new lane doc |
| Mission implementation | `verne-mission-writer` | Writing mission code |
| Modifier creation | `verne-modifier-creator` | Adding new modifier |
| Localisation generation | `verne-localisation-writer` | Creating .yml entries |
| QA compliance scan | `verne-qa-checker` | Checking standards |
| Cross-reference audit | `verne-auditor` | Verifying consistency |
| GFX generation | `verne-gfx-pipeline` | Creating event art |

### 5. Skill Creation ↔ Background Worker

**Every 5th background cycle (Priority 5), the worker:**

1. Scans conversation history for repeated patterns
2. Checks subagent trial log for high-reusability scores
3. Creates skills from confirmed patterns
4. Updates the task queue with newly automatable tasks
5. Logs to `skills/self-improving-agent/ledger.md`

---

## Skill Lifecycle

```
1. DETECT     A pattern is noticed (3+ occurrences, high reusability)
                    │
2. VALIDATE   Check: Is this broadly applicable? Is the solution verified?
                    │
3. CREATE     Generate SKILL.md + scripts using extract-skill.sh
                    │
4. VALIDATE   Check: Does it pass all quality gates?
                    │
5. INSTALL    Copy to skills/ directory, embed in memory
                    │
6. USE        Auto-loaded when context matches trigger conditions
                    │
7. IMPROVE    Each use generates trial data → skill gets better over time
```

---

## Current Skills

| Skill | Source | Type | Status |
|-------|--------|------|--------|
| `eu4-modding` | Human-created | Knowledge | Active |
| `self-improving-agent` | ClawHub | Automation | Active |
| `security-auditor` | Human-created | Security | Active |
| `autonomous-skill-creator` | Hermes ported | Self-enhancement | Active (pending integration) |

---

## Monitoring

Track skill effectiveness via:
- `skills/self-improving-agent/ledger.md` — skills created autonomously
- `skills/self-improving-agent/assets/LEARNINGS.md` — skill-related learnings
- Subagent trial log — how skills improve subagent performance
- Context compression ratio — tokens saved by referencing skills

---

## Key Insight

**Skills are the bridge between memory and execution.**

Memory knows *what happened*.
Skills know *how to do it*.
The autonomous skill creator connects them.

Notes tell you "we made this mistake before."
Skills tell you "just run this to do it right."

---

## 2026-04-01 Optimization Round (based on ChatGPT research)

Applied from cross-framework research (LangGraph, CrewAI, AutoGen, BabyAGI3, Airflow/Prefect).

### 1. Spawn Manifest — Context Compression ✅ DONE
- Created `scripts/spawn-compiler.ps1` — task-specific context capsules
- 6 worker types: researcher, coder, verifier, memory_writer, planner, worker
- Each capsule: narrow tools_allow, tools_deny, contexts, budgets, retrieval_keys
- Workers get ONLY what their task type needs — no universal bootstrap
- Token savings: verifier gets ~80% less context than universal load

### 2. Concurrency Hard-Cap ✅ DONE
- `maxConcurrent: 8` → **3** (memory-constrained)
- `maxChildrenPerAgent: 2`
- maxSpawnDepth: 1 (no chains)
- Browser lane: 1, exec-heavy lane: 1, generic: 1
- Config updated in `openclaw.json` via gateway patch

### 3. Health Monitor → Lightweight ✅ DONE
- Old: ran `openclaw CLI` commands → 50% timeout (broken memory-lancedb)
- New: `scripts/health-lightweight.ps1` — gateway HTTP ping only
- Cron job updated: `4e9fbcbb-cc30-441a-9ebd-81bab6f872d8`
- No more CLI dependency for health checks

### 4. Lifeboat Hard-Cap ✅ DONE
- Created `LIFEBOAT.md` — ~400 token compact state
- Contains: identity, current objective, next 3 actions, blockers, critical prefs, memory keys
- Loaded FIRST on every session bootstrap
- Replaces narrative-style session notes as primary state

### 5. Role Separation (partially done)
- Tool allowlists defined in spawn-compiler.ps1 per task type
- Agent roles: planner, worker, verifier, memory_writer defined
- Gap: memory_writer role is defined but no cron/job dedicated to it
- Trial logging still falls to main agent — needs automation

### 6. Auto-planner → Event-Driven (pending)
- Current: fixed 4h interval cron
- Target: on-demand trigger from new tasks, upstream changes, blocker detection
- Implementation: add trigger conditions to auto-planner cron message
- Status: documented, not yet implemented

### 7. QA Subagent Timeouts (critical gap)
- Root cause: subagents spend too much time reading context before editing
- Fix applied: spawn-compiler gives narrow tool access + budget caps
- QA tasks now get `verifier` capsule (read/exec only, 8 tool calls, 300s)
- Also: "ship first, verify later" rule added — make edit, then verify
- Status: mechanism in place, needs real trial to validate

### 8. npm Update (BLOCKED — needs admin)
- `C:\Program Files\nodejs\node_modules\openclaw` — broken from failed update
- Both appdata and program files installs exist; appdata was patched to 2026.3.28
- Fix: Run PowerShell as Administrator → `npm update -g openclaw`
- After fix: memory-lancedb will auto-install vectordb dependency

### Metrics to Track (per ChatGPT recommendation)
- Worker startup latency (before/after manifest adoption)
- Initial prompt size (tokens per worker type)
- Cache hit rate (prompt caching benefit)
- Queue wait time (concurrency pressure)
- Success/failure by task class
- Verifier pass rate (QA quality)
