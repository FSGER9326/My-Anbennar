# Improvement Plan — From Deep Research Reports
**Sources:**
- `C:\Users\User\Downloads\deep-research-agent-improvement-v2.md` (27KB, 31 citations)
- `C:\Users\User\Downloads\deep-research-browser-bridge.md` (22KB, 26 citations)
- Research report from ChatGPT (2026-04-01): browser automation, selector strategies, completion signals, MCP servers

**Principle:** No extra cost. Uses existing tools (OpenClaw browser, Playwright-core, OpenViking, Obsidian). No new API subscriptions.

---

## Implementation Status (2026-04-01)

### ✅ DONE — Production-Grade Browser Stack

**1. Browser Architecture Doc**
- `docs/browser-architecture.md` — full 5-layer design: Policy Skills → Snapshot/Ref → Lease Manager → Signal Registry → Model Router
- Covers: selector contracts, completion signals, lease semantics, rate-limit handling, MCP topology, hot-tab strategy

**2. Browser Skills (5 created)**
- `skills/browser-selector-contract/` — selector hierarchy enforcement (data-oc > role > label > iframe > CSS)
- `skills/browser-completion-signals/` — event-driven completion (waitForResponse + DOM sentinel + MutationObserver)
- `skills/browser-lease-recovery/` — recovery ladder (stale_ref → tab_gone → soft_429 → hard_block → circuit_break)
- `skills/browser-chat-streaming/` — ChatGPT 3-signal composite (transport + sentinel + stable)
- `skills/browser-vision-fallback/` — VLM escalation only when text-first fails

**3. AGENTS.md Updated**
- Browser section added with selector hierarchy, completion signals, lease rules, model router, MCP recommendations
- MEMORY.md updated with browser lessons

### ⏳ NEXT — High Priority

**4. Completion Signal Registry (plugin/service)**
- Per-site completion detector registry keyed by domain
- `browser-signal-registry` plugin: stores network/websocket/dom/predicate rules per app
- Wire into OpenClaw hooks (before_prompt_build injects site policy)

**5. Lease Manager (plugin)**
- `browser-lease-manager` plugin: owns {origin, account, proxyId, profile} → hot tab targetId
- Tracks TTL, failure count, cooldown, health
- Integrates with Session Handoff for targetId persistence

**6. Prompt Caching Optimization**
- MiniMax caching rewards stable prefixes
- Current issue: compact prefixes, but dynamic content interleaved unpredictably
- Goal: keep tool schemas + policy static, append dynamic lease state + task refs last

**7. Micro-Query Loop Enhancement**
- chatgpt-dom-driver.js already exists (17 functions)
- Missing: wire into OpenClaw browser tool as enrichment layer
- `browser-observation-cache` plugin: store compact snapshot summaries
- chatgpt-completion-watcher.js already exists but needs integration testing

### 🔄 STARTED

**8. OpenViking KG Schema + Hot-Path Writes**
- `scripts/openviking-write.ps1` — 3 facts committed
- Missing: create relations between nodes (Decision → affects → File)
- KG schema needed for OpenViking: Entity nodes (File, Feature, Decision, Issue, Task, LoreConstraint) + edges

**9. Nightly Timeout Auto-Tuning Cron**
- `docs/subagent-patterns.md` has Timeout Tuning Table (grows from trial results)
- Missing: automated nightly cron that reads trial log, computes p50/p90/p95, updates table

### 📋 FUTURE

**10. Chrome DevTools MCP Integration**
- Best fit for OpenClaw existing-session mode (same-host live Chrome reuse)
- Install: `npm install -g @modelcontextprotocol/server-chrome-devtools`
- Configure: openclaw config set browser.devtools.mcp.enabled true

**11. Playwright MCP Sidecar**
- Accessibility snapshots as action surface
- `mcp install playwright` or direct connection to Playwright MCP daemon
- Custom test-id attribute: `--test-id-attribute=data-oc`

**12. llm-task for Failure Classification**
- Use for micro-decisions (failure class, completion detector choice, lease retirement)
- 7 classes: stale_ref | soft_429 | hard_block | auth_expired | overlay | app_busy | completion_pending
- Requires: `llm-task` plugin configured with MiniMax

---

## Selector Contract: data-oc

**Highest-return reliability change for owned UIs.**

ChatGPT DOM driver uses `data-testid` internally (OpenAI's contract). For any UI Falk builds/controls, add `data-oc`:
```html
<button data-oc="composer.submit">Send</button>
<button data-oc="composer.stop">Stop</button>
<div data-oc="message.last"></div>
```

Configure: Playwright MCP `--test-id-attribute=data-oc`

---

## MCP Topology Decision

| Need | Best MCP |
|------|----------|
| Same-host live Chrome reuse | Chrome DevTools MCP ⭐ |
| Deterministic automation + accessibility snapshots | Playwright MCP ⭐ |
| Hosted concurrency + stealth + sessions | Browserbase MCP |
| Warm local daemon + low latency | browser-use MCP |

---

## Priority Matrix (2026-04-01)

| # | Strategy | Status | Effort | Impact |
|---|----------|--------|--------|--------|
| 1 | Browser architecture + 5 skills | ✅ Done | 3h | High |
| 2 | AGENTS.md browser section | ✅ Done | 30min | High |
| 3 | browser-signal-registry plugin | ⏳ Next | 3-4h | High |
| 4 | browser-lease-manager plugin | ⏳ Next | 3-4h | High |
| 5 | Prompt caching optimization | ⏳ Next | 2h | Medium |
| 6 | Micro-query integration (observation-cache) | ⏳ Next | 2h | Medium |
| 7 | OpenViking KG schema + relations | 🔄 Started | 3-4h | Medium |
| 8 | Nightly timeout auto-tuning cron | 🔄 Started | 1-2h | Medium |
| 9 | Chrome DevTools MCP | 📋 Future | 1h | High |
| 10 | Playwright MCP sidecar | 📋 Future | 1h | High |
| 11 | llm-task failure classification | 📋 Future | 2h | Medium |

---

## MiniMax M2.7 Fit Analysis

**What M2.7 does well:**
- Tool-driven, text-first browser automation
- Stable policy + deterministic execution (exactly the 5-layer stack)
- Long-horizon state tracking across turns

**Where M2.7 struggles:**
- No image input in text API (VLM fallback needed for canvas/screenshots)
- Sensitive to prompt noise — needs compact, stable prefixes
- Large browser snapshots = DOM hallucinations

**Design implications:**
- Structured snapshots + refs = text-first control = M2.7 optimal
- Screenshot-only = VLM escalation path
- Prompt caching = keep system/skill content STATIC, append dynamic last

**Model routing:**
- Default operator: MiniMax-M2.7-highspeed (faster, same quality)
- Planning/diagnosis: MiniMax-M2.7
- Visual fallback: MiniMax Image Understanding MCP or external VLM
- Micro-classifications: llm-task (JSON-only, no tools exposed)
