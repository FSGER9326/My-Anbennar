# Improvement Plan — From Deep Research Reports
**Sources:**
- `C:\Users\User\Downloads\deep-research-agent-improvement-v2.md` (27KB, 31 citations)
- `C:\Users\User\Downloads\deep-research-browser-bridge.md` (22KB, 26 citations)

**Principle:** No extra cost. Uses existing tools (OpenClaw browser, Playwright-core, OpenViking, Obsidian). No new API subscriptions.

---

## HIGH IMPACT — Implement This Week

### 1. Playwright Sidecar for Cross-Origin Iframe Clicks ✅ DONE
**Problem:** OpenClaw browser tool can't click inside cross-origin iframes (Deep Research cards).
**Solution:** Playwright script connecting via CDP, using `frameLocator` for nested iframes.
**Status:** Script created at `C:\Users\User\.openclaw\workspace\scripts\download-deep-research.js`. Successfully downloaded both Deep Research reports (27KB + 22KB).
**Pattern:** `const innerFrame = page.frameLocator('iframe').first().frameLocator('iframe').first();` → `innerFrame.getByRole('button', { name: 'Export' }).first().click()`
**Use for:** Any time OpenClaw browser tool can't reach inside an iframe.

### 2. Micro-Query Loop (Replace Snapshots with JS Evaluate)
**Problem:** Every interaction does a full page snapshot (100KB+ DOM) when we only need to check one thing.
**Solution:** Use `browser act kind=evaluate` for targeted DOM queries instead of snapshots.
**Implement:** A reusable set of JS evaluation functions:

```js
// Check if ChatGPT is still generating
() => document.querySelector('button[data-testid="stop-button"]') !== null

// Get last assistant message text
() => {
  const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
  const last = msgs[msgs.length-1];
  return (last?.querySelector('.markdown')?.innerText || last?.innerText || '').trim();
}

// Check for error state
() => {
  const err = document.querySelector('[role="alert"], [data-testid="error-message"]');
  return err ? err.innerText : null;
}

// Send message (fill textarea + submit)
() => {
  const ta = document.querySelector('textarea#prompt-textarea');
  ta.value = text;
  ta.dispatchEvent(new Event('input', {bubbles:true}));
  document.querySelector('button[data-testid="send-button"]').click();
}
```

**Impact:** Replace 90% of snapshots with 10-50ms evaluate calls. Snapshots only needed for navigation/unknown states.

### 3. Core Memory Already Implemented ✅ DONE
**From research:** "Adopt Letta-style memory blocks as plain text/YAML. persona, human, project_state, active_work."
**Status:** Already created today at `CORE_MEMORY.md` with exactly these 4 blocks.
**Next:** Also create a `MEMORY_RETRIEVAL.md` index file that lists all available memory sources and their last update time, so the agent can quickly decide what to load.

### 4. Session Handoff Already Implemented ✅ DONE
**From research:** "Add a second file called 'Last Session Handoff' overwritten at end of each session with ReSum-style compact reasoning state."
**Status:** Already created today at `SESSION_HANDOFF.md`.
**Next:** Make the handoff more structured — add YAML frontmatter with `last_session`, `key_decisions`, `in_progress`, `next_actions` fields.

### 5. Structured Trial Log with Failure Taxonomy
**From research:** "Treat each subagent spawn as an experiment run. Classify → propose fix → promote."
**What's missing from current trial log:** JSON structure, failure taxonomy, reflexion stub.
**Action:** Update `docs/subagent-patterns.md` to use a JSON template for each trial:

```json
{
  "id": "trial-14",
  "type": "doc-writer",
  "model": "openrouter/xiaomi/mimo-v2-pro",
  "timeout_setting": 900,
  "status": "timeout",
  "wall_time": 599,
  "failure_taxonomy": "timeout",
  "scores": {"speed": 2, "quality": 3, "correctness": 3, "self_sufficiency": 3, "tokens": 2},
  "reflection": "900s was not enough for 6-lane rewrite. The first 4 lanes took 15min. Next time: 1500s."
}
```

**Automated failure taxonomy rules:**
- `timeout` → wall_time >= timeout_setting
- `tool_error` → returned non-zero exit code
- `incomplete_output` → artifacts missing or empty
- `wrong_content` → quality or correctness score < 3

### 6. Nightly Timeout Auto-Tuning Cron
**From research:** "Record p95 runtime per archetype. Set default timeout to p95 + safety_margin."
**Action:** Create a new cron job that runs nightly:

Reads the trial log, computes p50/p90/p95 per archetype (QA, doc-writer, analyzer, browser), updates the Timeout Tuning Table, promotes settings that improve outcomes.

---

## MEDIUM IMPACT — This Month

### 7. OpenViking KG Schema + Hot-Path Writes ✅ PARTIALLY DONE
**From research:** "Entity nodes: File, Feature, Decision, Issue, Task, LoreConstraint. Edges: DECISION_IMPLIES_DECISION, DECISION_AFFECTS_FILE, etc."
**Done:** Write script exists (`scripts/openviking-write.ps1`), 3 facts committed.
**Missing:** KG schema for OpenViking nodes/relations, batch nightly extraction from daily logs.
**Action:** Test creating relations between nodes (e.g., Decision → affects → Mission file). Set up nightly cron to extract entities from daily files.

### 8. Trajectory-Based Skill Detection
**From research:** "Instead of counting repeated tasks, count repeated trajectories. Normalize tool calls: SEARCH → READ → PATCH → TEST → WRITELOG."
**Action:** 
- Add tool sequence logging to each subagent trial (just track what tools were called in order)
- Add a normalization step: replace file paths with `<FILE>`, province names with `<PROVINCE>`
- Use n-gram frequency counter over normalized sequences
- When a pattern hits 3+ occurrences AND saves time → flag for skill creation

### 9. Reflexion-Style Reflection Stubs
**From research:** "After each subagent run, add a reflection stub: one paragraph explaining what should change next time."
**Action:** Add a `reflection` field to each trial log entry. After a failed subagent, write 1-2 sentences about what went wrong and what to do differently. The next spawn of that archetype automatically includes this as a "what to avoid" note.

### 10. Page-Level DOM Extraction for ChatGPT
**From research:** Stable selectors for ChatGPT UI:
- `[data-message-author-role="assistant"]` — assistant messages
- `.markdown` — response content
- `button[data-testid="stop-button"]` — generating indicator
- `button[data-testid="send-button"]` — send button
- `textarea#prompt-textarea` — input field
- `button[aria-label="Regenerate"]` — completion indicator

**Action:** Create `scripts/chatgpt-dom-driver.js` (Playwright sidecar) with these stable selectors. Use for all future ChatGPT interactions instead of raw snapshots.

---

## LOW PRIORITY — Future

### 11. API Migration (costs money, skip for now)
**Research says:** Deep Research is available via Responses API (`o3-deep-research`, `o4-mini-deep-research`) with background mode + webhooks.
**Why skip:** API costs money. The Playwright sidecar + browser bridge works fine for our usage level. Only migrate if we need >10 deep research calls/day.

### 12. Prompt Compression (LLMLingua) — skip for now
**Research says:** LLMLingua/LongLLMLingua compress prompts with budget controller.
**Why skip:** Requires running a separate model. Our context window is large enough with CORE_MEMORY.md + SESSION_HANDOFF.md being small.

---

## Priority Status

| # | Strategy | Status | Effort | Impact |
|---|----------|--------|--------|--------|
| 1 | Playwright sidecar for iframes | ✅ Done | — | High |
| 2 | Micro-query loop (evaluate) | ⏳ Next | 2-3h | High |
| 3 | Core memory blocks | ✅ Done | — | High |
| 4 | Session handoff | ✅ Done | — | High |
| 5 | Structured trial log | ⏳ Next | 1h | Medium |
| 6 | Nightly timeout tuning cron | ⏳ Next | 1-2h | Medium |
| 7 | OpenViking KG schema | 🔄 Started | 3-4h | Medium |
| 8 | Trajectory-based skill detection | ⏳ Next | 2-3h | Medium |
| 9 | Reflexion-style reflection stubs | ⏳ Next | 30min | Medium |
| 10 | ChatGPT DOM driver | ⏳ Next | 2-3h | Medium |
| 11 | API migration | 📋 Future | — | High ($) |
| 12 | Prompt compression | 📋 Future | — | Low |
