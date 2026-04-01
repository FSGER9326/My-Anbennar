# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260331-001] best_practice

**Logged**: 2026-03-31T21:55:00+02:00
**Priority**: high
**Status**: promoted
**Area**: config

### Summary
Sub-agent spawned sessions cannot reliably write files to the parent workspace.

### Details
When sub-agents write to relative paths like `docs/design/lanes/`, the files end up in ephemeral directories that get cleaned up after the session ends. This happened across 8 sub-agent spawns — all reported success but zero files survived.

### Suggested Action
Always use explicit absolute paths when sub-agents need to write files. E.g., `C:\Users\User\.openclaw\workspace\docs\design\lanes\` not `docs/design/lanes/`.

### Metadata
- Source: error
- Related Files: AGENTS.md
- Tags: subagent, file-io, reliability
- Pattern-Key: subagent.filepaths.absolute

### Resolution
- **Resolved**: 2026-03-31T21:50:00Z
- **Notes**: Switched to absolute paths for all file writes — worked on second attempt.

---

## [LRN-20260331-002] insight

**Logged**: 2026-03-31T21:55:00+02:00
**Priority**: medium
**Status**: resolved
**Area**: plugins

### Summary
Many "top OpenClaw plugins" articles list tools that don't actually exist on npm/ClawHub.

### Details
Composio article and Reddit post listed env-guard, cost-tracker, openclaw-ntfy as "must-have" plugins. None were found on npm or ClawHub. The Reddit post was likely describing unreleased or renamed tools. Only stock plugins (memory-lancedb, lobster) and real npm packages (lossless-claw) were actually installable.

### Suggested Action
Verify plugin existence on npm/ClawHub before recommending or installing. Don't trust marketing articles at face value.

### Metadata
- Source: conversation
- Tags: plugins, verification
- Pattern-Key: verify.before.install

---

## [LRN-20260331-003] knowledge_gap

**Logged**: 2026-03-31T21:59:00+02:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
memory-lancedb plugin conflicts with stock memory-core — "memory slot" is set to "memory-core" by default.

### Details
Enabling memory-lancedb in plugins.entries doesn't automatically activate it. The plugin system has a "memory slot" concept where only one memory provider can be active. Warning: `plugin disabled (memory slot set to "memory-core")`. memorySearch config (hybrid search, MMR, temporal decay) works independently with the builtin memory engine. The Ollama embedding endpoint works but memory-lancedb needs additional slot configuration.

### Suggested Action
Investigate how to switch the memory slot from memory-core to memory-lancedb. May require `openclaw plugins enable memory-lancedb` with specific flags or a config key not yet discovered. For now, memorySearch hybrid config is active and provides BM25+vector search via the builtin engine.

### Metadata
- Source: error
- Related Files: plugins.entries.memory-lancedb, memorySearch config
- Tags: memory, lancedb, plugin, config

---

## [LRN-20260331-005] best_practice

**Logged**: 2026-03-31T22:25:00+02:00
**Priority**: high
**Status**: promoted
**Area**: automation

### Summary
Health monitoring cron job added (every 30 min) + heartbeat standing order for diagnostics.

### Details
Automated health monitor checks: gateway status, task audit, channel health, memory index, log errors. Reports only issues (silent on HEALTH_OK). Standing order in AGENTS.md for heartbeat-driven checks 1-2x/day. Script at scripts/health-check.sh for full diagnostic output.

### Suggested Action
Review cron runs periodically. If health monitor generates too many false positives, adjust the check criteria or increase interval.

### Metadata
- Source: conversation
- Tags: health, monitoring, cron, automation
- Pattern-Key: health.monitoring

---

## [LRN-20260401-001] correction

**Logged**: 2026-04-01T11:10:00+02:00
**Priority**: high
**Status**: resolved
**Area**: memory

### Summary
Session context is lost at compaction. Structural decisions made in chat must be written to daily file IMMEDIATELY, not relied upon between sessions.

### Details
Falk decided on 10-column lane map in prior session (Mar 31 / Apr 1 overnight). This decision was NOT captured in daily file or MEMORY.md. When new session started, the 10-column structure was unknown until Falk pointed it out. Had to search downloaded chat files and ChatGPT planning session to recover the information.

### Suggested Action
- Added "CAPTURE DECISIONS IMMEDIATELY" rule to AGENTS.md
- Added "Memory Capture" section to MEMORY.md lessons
- When Falk makes a structural decision (branch names, lane counts, architecture), write to daily file right away

### Metadata
- Source: error
- Related Files: AGENTS.md, MEMORY.md
- Tags: memory, compaction, decisions
- Pattern-Key: memory.capture.decisions

---

## [LRN-20260401-002] best_practice

**Logged**: 2026-04-01T11:10:00+02:00
**Priority**: high
**Status**: resolved
**Area**: cron

### Summary
Cron jobs need timeout tuning and delivery fixes. Auto-planner (120s) and upstream sync (180s) were timing out. QA delivery was failing because Telegram target wasn't set.

### Suggested Action
- auto-planner: timeout 120s → 300s
- anbennar-upstream-sync: timeout 180s → 600s
- verne-qa-check: delivery mode 'none' → 'announce' (no Telegram target needed)

### Metadata
- Source: error
- Related Files: cron jobs
- Tags: cron, timeout, delivery
- Pattern-Key: cron.tuning

---

## [LRN-20260401-003] insight

**Logged**: 2026-04-01T11:10:00+02:00
**Priority**: medium
**Status**: resolved
**Area**: architecture

### Summary
Three memory systems exist but aren't synced: OpenClaw memory (daily files + MEMORY.md), Obsidian vault (Crab Memory), and OpenViking (knowledge graph server at :1933).

### Details
- OpenClaw memory: what agents read/write (daily files, MEMORY.md)
- Obsidian vault: `C:\Users\User\Documents\Crab Memory\` with Daily Notes, Knowledge Base, Learnings, Projects, Templates, Archive
- OpenViking: FastAPI server at http://127.0.0.1:1933 with search, sessions, relations, skills, content management endpoints
- Currently only OpenClaw memory is written to. Obsidian daily notes are stale. OpenViking has no writes from agent side.

### Suggested Action
- Ask Falk what the intended sync flow is
- Consider: write daily notes to all three? Use OpenViking as primary?

### Metadata
- Source: conversation
- Tags: memory, obsidian, openviking, sync
- Pattern-Key: memory.multi-system

---

## [LRN-20260401-004] correction

**Logged**: 2026-04-01T11:10:00+02:00
**Priority**: high
**Status**: resolved
**Area**: subagent

### Summary
Auto skill creation (Hermes-based) is integrated but has never fired. Ledger shows 0 autonomous creations. The system needs explicit triggering, not just passive definition.

### Details
The autonomous skill creator is defined in skills/self-improving-agent/ with detection triggers (3+ occurrences, reusability ≥9). But the background worker is supposed to trigger it every 5th cycle (Priority 5 in HEARTBEAT.md). Today's heartbeat spawned S05/S06 tasks instead of running Priority 5 self-improvement. The protocol is defined but not properly wired into the heartbeat loop.

### Suggested Action
- Explicitly run self-improvement cycle when heartbeat fires and all higher-priority tasks are done
- Check Trial Log for patterns with 3+ occurrences before considering skill creation
- QA compliance fix patterns (S02 tooltips, S05 typos) are emerging candidates

### Metadata
- Source: error
- Related Files: HEARTBEAT.md, skills/self-improving-agent/
- Tags: skill-creation, self-improvement, background-worker
- Pattern-Key: skill.creation.triggering

---

## [LRN-20260401-005] best_practice

**Logged**: 2026-04-01T11:10:00+02:00
**Priority**: medium
**Status**: pending
**Area**: subagent

### Summary
Spawning subagent with outdated architecture info wastes the spawn. Always check MEMORY.md and recent decisions before spawning design/implementation work.

### Details
Spawned "design-docs-reconciliation" subagent with 9-slot info. The project had already moved to 10-column lane map. Had to kill the subagent and respawn with correct instructions. Wasted ~13 min and 73k tokens.

### Suggested Action
- Before spawning any subagent for design/architecture work, read MEMORY.md for latest decisions
- Check daily file for recent structural changes
- Verify branch name matches current work

### Metadata
- Source: error
- Related Files: subagent-patterns.md
- Tags: subagent, memory, architecture
- Pattern-Key: subagent.check.memory.first

---

## [LRN-20260331-007] correction

**Logged**: 2026-03-31T23:37:00+02:00
**Priority**: high
**Status**: promoted
**Area**: chatgpt

### Summary
CORRECTION: Only Thinking 5.4 has DALL-E. Pro 5.4 does NOT have image generation. Extended thinking effort is a separate setting from model selection.

### Details
Earlier learning LRN-20260331-006 incorrectly stated "Pro 5.4 has DALL-E." The correct model is Thinking 5.4. The model selector has three options:
- Instant 5.3 (fast text, no DALL-E)
- Thinking 5.4 (complex reasoning + DALL-E ✅)
- Pro 5.4 (research-grade text only, no DALL-E)

Thinking effort (Standard/Extended) is a separate dropdown in Configure dialog. Standard = faster image gen, Extended = deeper reasoning. Both work with DALL-E.

### Suggested Action
Always select Thinking 5.4 for image generation. Never use Pro 5.4 or Instant 5.3.

### Metadata
- Source: correction
- Tags: chatgpt, dalle, model, image-generation
- Pattern-Key: chatgpt.model.mapping

---

## [LRN-20260331-006] best_practice

**Logged**: 2026-03-31T23:28:00+02:00
**Priority**: high
**Status**: promoted
**Area**: art-generation

### Summary
ChatGPT Pro mode (plain) does NOT have DALL-E. Extended Pro mode is required for image generation. Extended thinking overhead is just the cost of DALL-E access.

### Details
Image generation failed repeatedly when the art generator subagent tried standard/pro mode. Only Extended Pro mode has DALL-E image generation capability. The extended thinking doesn't improve image quality (DALL-E is a separate model), but it's the mode that has DALL-E access.

### Suggested Action
Always use Extended Pro mode for image generation. Don't waste time trying standard mode.

### Metadata
- Source: error
- Related Files: docs/chatgpt-browser-bridge.md
- Tags: chatgpt, dalle, image-generation, mode

---

## [LRN-20260401-001] insight

**Logged**: 2026-04-01T00:29:00+02:00
**Priority**: high
**Status**: pending
**Area**: security

### Summary
HERMES AGENT scans context files (AGENTS.md, SOUL.md, etc.) for prompt injection before injecting them into the system prompt. We should do the same.

### Details
Hermes scans for: "ignore previous instructions", "do not tell the user", "system prompt override", "disregard your instructions", HTML comment injections, hidden divs, secret extraction patterns (curl, cat .env), invisible unicode characters. When found, they block the content and log the finding.

### Suggested Action
Add a context file scanning function to our startup process. Check AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md before using them in prompts. Sanitize any content that matches threat patterns.

### Metadata
- Source: code_review
- Related Files: AGENTS.md, SOUL.md, TOOLS.md
- Tags: security, prompt_injection, context_files

---

## [LRN-20260401-002] insight

**Logged**: 2026-04-01T00:29:00+02:00
**Priority**: medium
**Status**: pending
**Area**: architecture

### Summary
HERMES AGENT has smart model routing — detects complex keywords in user messages and routes to cheap/strong models automatically. We implemented something similar but could use keyword-based auto-routing.

### Details
Hermes checks user messages for complex keywords (debug, implement, refactor, analyze, architecture, etc.). If found → use strong model. If not found → use cheap model. This saves tokens on simple queries automatically without manual intervention.

### Suggested Action
Add keyword-based routing to our setup: if user message contains complex keywords → use MiMo Pro. If simple (lookup, greeting, quick question) → use MiMo Flash automatically. Already have subagent-light for this, but main session could benefit.

### Metadata
- Source: code_review
- Related Files: TOOLS.md, docs/chatgpt-browser-bridge.md
- Tags: model_routing, efficiency, token_savings

---

## [LRN-20260401-003] insight

**Logged**: 2026-04-01T00:29:00+02:00
**Priority**: medium
**Status**: pending
**Area**: architecture

### Summary
HERMES AGENT uses a structured context compressor: auxiliary cheap model summarizes middle turns while protecting head (system prompt) and tail (recent context). Iterative summary updates save previous summaries into a running context overview.

### Details
Instead of OpenClaw's simple compaction (which truncates), Hermes uses a cheaper model to *summarize* old turns and keeps those summaries as "memory." This preserves semantic content while reducing token count. They also have an "iteration overview" that accumulates summaries across multiple compact cycles.

### Suggested Action
When OpenClaw triggers compaction, the notes we save to MEMORY.md should be structured (not free-form). Use a cheap model for summarization rather than the main model.

### Applied Pattern (2026-04-01)
OpenClaw's compaction already summarizes before truncating. To make it Hermes-style:
1. BEFORE compaction triggers, proactively save structured notes to daily file:
   - Decisions made
   - Current task status
   - Blockers
   - Key data (IDs, paths, configs)
2. After compaction, the saved notes survive in daily file
3. This is already partially what we do via MEMORY.md and daily notes

### What we CAN'T do (yet)
Hermes uses an "iteration overview" — a running summary that accumulates across multiple compaction cycles. OpenClaw compacts the entire context, so summaries don't persist across compact → compact cycles. Our daily notes serve as the persistence layer instead.

### Metadata
- Source: code_review
- Related Files: MEMORY.md
- Tags: context_management, compaction, efficiency

---

## [LRN-20260401-007] insight

**Logged**: 2026-04-01T00:46:00+02:00
**Priority**: high
**Status**: promoted
**Area**: automation

### Summary
Background worker system established: when main session is idle (heartbeat, no active tasks), subagents automatically work through the Verne modding task queue from background-worker.md.

### Details
Priority queue: fix design doc issues → write modifier/localisation files → QA compliance → generate GFX → research → polish. Idle detection checks: heartbeat firing, no running subagents, no pending human input, last human message >5 min ago. Subagents announce only if critical finding or task completed.

### Metadata
- Source: conversation
- Tags: automation, subagent, background, verne
- Pattern-Key: background.worker

---

## [LRN-20260401-004] best_practice

**Logged**: 2026-04-01T00:43:00+02:00
**Priority**: high
**Status**: promoted
**Area**: efficiency

### Summary
Memory layered indexing implemented: Tier 1 (daily files, core config), Tier 2 (learnings), Tier 3 (docs, repo). Temporal decay half-life set to 14 days.

### Details
extraPaths in memorySearch config now includes:
- Tier 1: MEMORY.md, memory/ (daily files) — always most relevant
- Tier 2: .learnings/LEARNINGS.md, ERRORS.md — important but less accessed
- Tier 3: docs/, Anbennar repo — on-demand reference, older content
- Temporal decay: 14-day half-life (replaces 30-day) — more aggressive decay for faster context relevance

### Metadata
- Source: code_review
- Tags: memory, indexing, efficiency, configuration

---

## [LRN-20260401-005] best_practice

**Logged**: 2026-04-01T00:43:00+02:00
**Priority**: medium
**Status**: promoted
**Area**: efficiency

### Summary
Session naming convention: name sessions by topic for better memory search results. "Verne - Art Generation" beats "New Chat".

### Suggested Action
Always name sessions when starting new conversations. Include topic and action type.

### Metadata
- Source: code_review
- Tags: memory, session, naming, efficiency

---

## [LRN-20260401-011] insight

**Logged**: 2026-04-01T00:58:00+02:00
**Priority**: high
**Status**: promoted
**Area**: automation

### Summary
Self-enhancement architecture fully integrated: background worker → skill detection → skill creation → memory embedding → context compression → improved subagent work → more work → repeat. This is a compound self-improvement loop.

### Details
The complete loop: Work happens → data captured (trial logs, errors) → patterns detected (3+ occurrences) → skill created (SKILL.md + scripts) → skill installed → embedded in memory-lancedb → available to subagents → compressed context references skills → next work cycle starts with better templates → faster, higher quality. Skills are the bridge between memory (what happened) and execution (how to do it).

### Metadata
- Source: conversation
- Tags: integration, self_improvement, skills, architecture
- Related Files: docs/self-enhancement-architecture.md, skills/self-improving-agent/, skills/autonomous-skill-creator/

---

## [LRN-20260401-009] insight

**Logged**: 2026-04-01T00:52:00+02:00
**Priority**: high
**Status**: promoted
**Area**: automation

### Summary
Hermes autonomous skill creator installed. It detects repeated patterns from conversation history and automatically creates new skills. Three detection methods: repetition (same action 3+ times), code pattern (copied function templates), complexity (multi-step procedures).

### Details
Skill creator uses three detectors:
1. RepetitionDetector — finds same action type + message combinations (3+ occurrences)
2. CodePatternDetector — finds frequently copied code templates (>3 copies, >80 lines)
3. ComplexityDetector — finds multi-step procedures that should be bundled

When a pattern is detected, the creator: generates a plan → creates SKILL.md + scripts → validates → installs automatically. Logged to `skills/autonomous-skill-creator-ledger.md`.

Skills created autonomously get a `# Skill Created Autonomously` note to track which ones the system created vs human-created.

### Metadata
- Source: code_review (nousresearch/hermes-agent)
- Related Files: skills/autonomous-skill-creator/
- Tags: skill_creation, automation, self_improvement

---

## [LRN-20260401-010] insight

**Logged**: 2026-04-01T00:52:00+02:00
**Priority**: high
**Status**: pending
**Area**: technical

### Summary
Hermes learned that plugin tool results are NOT streamed and can be 10-100KB JSON blobs. Using `process.stdout.write` (correct) instead of `console.log` avoids breaking streaming. Buffer output and flush at end.

### Details
OpenClaw plugin tool results (from MCP or custom plugins) come as very large JSON objects. If they're streamed chunk by chunk, the model loses context about the initial parts. Use `process.stdout.write` with manual flushing to send results atomically. This is an undocumented technical limitation we should watch for.

### Metadata
- Source: code_review (nousresearch/hermes-agent)
- Related Files: learnings-reference/knowledge_base/openclaw_api_notes.md
- Tags: technical, openclaw, streaming, plugins

---

## [LRN-20260401-008] insight

**Logged**: 2026-04-01T00:48:00+02:00
**Priority**: high
**Status**: promoted
**Area**: automation

### Summary
Background worker system is fully self-improving: each completed task is evaluated (10-dimension scoring), trial logged to subagent-patterns.md, task queue updated with discovered tasks, and every 5th cycle the worker reviews its own protocol for improvements.

### Details
The background worker doesn't just do tasks — it learns from doing them. After each task: evaluate on 10 dimensions, log trial, update roadmap. Every 5th cycle: review Trial Log patterns, recalibrate timeouts, merge/split tasks, update delegation matrix. This means the system gets faster and smarter over time without human intervention.

### Metadata
- Source: conversation
- Tags: automation, self_improvement, background, subagent
- Pattern-Key: self_improving.background.worker

---

## [LRN-20260401-006] best_practice

**Logged**: 2026-04-01T00:43:00+02:00
**Priority**: medium
**Status**: promoted
**Area**: automation

### Summary
session-memory hook auto-saves context on /new or /reset. command-logger hooks all commands to audit file. Both are now enabled and ready.

### Metadata
- Source: code_review
- Tags: hooks, automation, session

---

## [LRN-20260331-004] best_practice

**Logged**: 2026-03-31T22:07:00+02:00
**Priority**: high
**Status**: promoted
**Area**: eu4-modding

### Summary
EU4 Paradox script uses tabs for indentation, `#` for comments, no semicolons, and `{}` must be balanced.

### Details
Every `{` needs matching `}`. Indentation is tabs (not spaces). No semicolons at end of lines. Comment syntax is `#` only — `//` and `/* */` don't work. Event IDs follow `namespace.number` format. Localisation keys must have `:0` version tag.

### Suggested Action
When writing any Paradox script file, always use tabs, balance braces, and verify localisation keys exist for all player-facing text.

### Metadata
- Source: conversation
- Tags: eu4, paradox, syntax, scripting
- Pattern-Key: eu4.modding.syntax
- Recurrence-Count: 1
- First-Seen: 2026-03-31
- Last-Seen: 2026-03-31

---

### EU4 Modding Knowledge Base
**Project reference file**: `docs/eu4-modding-reference.md`
**Promotion target**: EU4/Anbennar modding learnings with Pattern-Key `eu4.*` should be promoted to the reference file (not AGENTS.md) when Recurrence-Count >= 3.
**Categories to track**: syntax errors, modifier conventions, event patterns, localisation, cross-file dependencies.

---

**Logged**: 2026-03-31T21:55:00+02:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
PowerShell command separators differ from bash — use `;` not `||` or `|` for sequential commands.

### Details
Multiple commands failed because bash-style `||` operators don't work in PowerShell. The pipe character `|` works but `head` doesn't exist — use `Select-Object -First N` instead.

### Suggested Action
Always use PowerShell-native syntax: `;` for sequential, `Select-Object` for head, `ForEach-Object` for map.

### Metadata
- Source: error
- Tags: powershell, shell, windows
- Pattern-Key: shell.powershell.syntax

---
