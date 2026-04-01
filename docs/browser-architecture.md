# Browser Architecture — Production-Grade OpenClaw Control Plane

**Layer model for reliable, fast, MiniMax-M2.7-native browser automation.**

---

## The Core Problem

Raw browser automation fails because:
1. Model sees noisy full-page snapshots → hallucinates DOM structure
2. No distinction between "read" and "act" → model wastes tokens on traversal
3. Generic waits (sleep, networkidle) → false positives, wasted cycles
4. No session ownership → tabs clash, auth state leaks between contexts
5. Screenshot-first reasoning → burns VLM tokens on every turn

**Fix: 5-layer stack that matches what production browser agents actually do.**

---

## 5-Layer Architecture

```
┌─────────────────────────────────────────────────┐
│  LAYER 1: Policy & Skills                       │
│  Selector contracts, completion registries,     │
│  recovery playbooks, visual fallback triggers    │
└──────────────────────┬──────────────────────────┘
                       │ structured skill calls
┌──────────────────────▼──────────────────────────┐
│  LAYER 2: Structured Snapshot / Ref Engine      │
│  OpenClaw browser snapshot → compact AI refs    │
│  + app-specific DOM micro-queries (enriched)    │
└──────────────────────┬──────────────────────────┘
                       │ deterministic actions
┌──────────────────────▼──────────────────────────┐
│  LAYER 3: Lease / Session Manager              │
│  {origin, account, proxyId, profile} → hot tab  │
│  targetId ownership, TTL, health, cooldown      │
└──────────────────────┬──────────────────────────┘
                       │ enforcement per turn
┌──────────────────────▼──────────────────────────┐
│  LAYER 4: Signal Registry (per-site)           │
│  network response / websocket / DOM sentinel /  │
│  JS predicate / mutation stabilization         │
└──────────────────────┬──────────────────────────┘
                       │ event-driven completion
┌──────────────────────▼──────────────────────────┐
│  LAYER 5: Provider / Model Router              │
│  MiniMax-M2.7-highspeed (operator)              │
│  MiniMax-M2.7 (planner) / VLM fallback        │
│  llm-task for micro-classifications             │
└─────────────────────────────────────────────────┘
```

---

## Layer 1: Policy Skills

### browser-selector-contract
```
Selector priority (enforced, not suggested):
1. data-oc="element.name"     — owned apps, explicit contract
2. getByRole({ name })        — user-semantic, all apps
3. label / placeholder / text  — form/content fallbacks
4. frameLocator + above        — iframe boundaries
5. CSS/XPath                   — emergency only
```
**Install:** Add `data-oc` attributes to owned UIs. Configure sidecars to treat `data-oc` as test-id attribute.

### browser-completion-signals
```
Site-specific completion detector registry:
- chatgpt:      websocket frame EOF + Stop btn gone + DOM stable
- openchat:     network response + spinner gone + mutation quiet
- claude:       [data-testid="submit-button"] re-enabled + streaming stop
- generic:      networkidle NOT used — use waitForResponse + DOM sentinel
```

### browser-lease-recovery
```
Recovery ladder (in order):
1. Stale ref after nav → re-snapshot, re-resolve
2. Tab targetId gone → lease_acquire new tab, re-navigate
3. Soft 429         → backoff 30s, retry once
4. Hard block       → retire lease, acquire new {account, proxy}
5. Auth expired     → full re-auth flow, new lease
6. 3 failures       → circuit break, alert human
```

### browser-chat-streaming
```
ChatGPT streaming completion detection:
1. Arm waitForResponse(/v1/chat/completions) BEFORE sending
2. Watch websocket for done/finish frames
3. Poll isGenerating() every 2s (Stop btn present = still going)
4. DOM stable: no MutationObserver changes for 1.5s
5. Completion = all 3 signals align
```

### browser-vision-fallback
```
When to escalate to VLM:
- Canvas/rendering app (no accessible refs)
- Anti-bot puzzle (CAPTCHA, challenge)
- Screenshot-only ambiguous state
- Accessibility-poor third-party widget
- Explicit request from human

Before screenshot: capture structured snapshot + refs first.
VLM prompt template: "Given refs [e12, e48], describe what e12 describes."
```

---

## Layer 2: Structured Snapshot First

**Rule: Always snapshot before act. Always re-snapshot after nav.**

OpenClaw browser snapshot returns refs. These are the action surface:
```
browser snapshot profile=openclaw → e12, e48, ...
browser act kind=click ref=e12   → deterministic
browser snapshot                  → refs updated post-nav
```

**DOM micro-queries (chatgpt-dom-driver.js) are ENRICHMENT only:**
- Snapshot gets the page structure
- DOM driver enriches with app-specific state (isGenerating, canSend, turnCount)
- DOM driver does NOT drive primary navigation

---

## Layer 3: Lease Manager

```javascript
// Lease key: { origin, account, proxyId, browserProfile }
class BrowserLease {
  constructor({ origin, account, proxyId, profile }) { ... }
  
  acquireTab() { /* returns targetId */ }
  retire()     { /* cleanup, mark expired */ }
  health()     { /* failure count, cooldown state */ }
  extend(ttl)  { /* heartbeat extend */ }
}

// OpenClaw session → 1 active lease
// Subagents get their own lease (no sharing)
// Parallel work → separate sessions with separate leases
```

**Rules:**
- One hot tab per lease (browser-use daemon model)
- Auth state persists in profile/storageState
- Retire after TTL even if "healthy" (browserPool retirement)
- Key by {origin, account, proxyId} — never share leases across identities

---

## Layer 4: Signal Registry

```javascript
const registry = {
  'chatgpt.com': {
    completion: {
      network:  waitForResponse('/v1/chat/completions'),
      websocket: 'frame' type == 'done' || 'close',
      dom:       isGenerating() === false,
      stable:    mutationObserver(1500ms no change)
    },
    challenge: ['[data-testid="error-message"]', 'iframe[src*="challenge"]'],
    expired:   window.location.includes('/auth')
  },
  'claude.ai': {
    completion: {
      network:  waitForResponse('/api/chat/stream'),
      dom:      document.querySelector('[data-testid="submit"]')?.disabled === false,
      stable:   mutationObserver(1000ms no change)
    }
  }
};
```

**Event-driven, NOT polling.** Use MutationObserver natively. OpenClaw browser tool supports `wait` on selector/JS predicate — use that before polling loops.

---

## Layer 5: Model Router

```javascript
// Routing rules (before_model_resolve hook):
function routeModel(turn) {
  if (turn.tools.active.includes('browser_snapshot')) return 'minimax/MiniMax-M2.7-highspeed';
  if (turn.tools.active.includes('browser_act'))     return 'minimax/MiniMax-M2.7-highspeed';
  if (turn.complexity === 'high' && turn.tools.count > 5) return 'minimax/MiniMax-M2.7';
  if (turn.hasScreenshot && turn.needsVLM)         return 'vision-fallback';
  return 'minimax/MiniMax-M2.7-highspeed';
}
```

**MiniMax-M2.7-highspeed is the default operator** — same quality, faster. Standard M2.7 for planning/diagnosis. VLM path only for visual ambiguity.

---

## MCP Sidecar Recommendations

| MCP Server | Use When | Fit |
|------------|----------|-----|
| **Chrome DevTools MCP** | Same-host live Chrome reuse | ⭐ Best for OpenClaw existing-session mode |
| **Playwright MCP** | Deterministic automation, accessibility snapshots | ⭐ Best general-purpose sidecar |
| **Browserbase MCP** | Hosted concurrency, persistent sessions, stealth | ⭐ Best for scale |
| **browser-use MCP** | Warm local daemon, low-latency | Good for repeated flows |
| **mcp-for-dev/mcp-chrome** | Attach to existing Chrome via CDP | Secondary option |

**Note for MiniMax:** MCP schemas can be bulky. For repeated flows, prefer tightly-wrapped OpenClaw-native skill + CLI over raw MCP surface exposure.

---

## Rate Limit Handling

```
Model (MiniMax):
  429 + Retry-After → honor header, backoff
  429 no header     → exponential backoff 1s/2s/4s/8s + jitter
  Plan exhausted    → rotate key or wait for window

Browser/Site:
  Soft 429          → same session + IP, 30s backoff, 1 retry
  Hard block        → retire lease (session + proxy together)
  Challenge/CAPTCHA → retire immediately, alert human
  Broad outage      → circuit break, stop all traffic

Detection:
  llm-task for failure classification (JSON-only, no tools)
  7 classes: stale_ref | soft_429 | hard_block | auth_expired | overlay | app_busy | completion_pending
```

---

## Hot Tab Strategy (ChatGPT Example)

```
Session start:
  1. lease = BrowserLease.acquire({ origin: 'chatgpt.com', account: 'main' })
  2. tab   = lease.acquireTab()  → targetId
  
Each task:
  3. browser snapshot (tab.targetId) → refs
  4. browser act (ref=e12, text="...") → deterministic click/type
  5. completion watcher → event-driven wait
  6. browser snapshot → verify state
  
Session end:
  7. lease.extend(TTL) — keep warm, don't close
  8. Store targetId in Session Handoff for next session
```

**Never close and reopen for every task.** Keep the tab hot. This mirrors browser-use's 50ms command latency design.

---

## Prompt Caching Optimization

MiniMax caching rewards stability. Keep these STATIC:
- System prompt (browser policy)
- Skill descriptions (browser-selector-contract, etc.)
- Tool schema (stable action surface)
- Model routing rules
- Completion signal registry (site policies)

Append DYNAMIC content last:
- Current lease state
- Task-specific refs
- Last observation summary
- Site-specific completion detector

This = better cache hit rate + faster turns.

---

## Selector Contract: data-oc

For any UI OpenClaw owns/controls, add automation attributes:

```html
<!-- ChatGPT-style streaming app -->
<button data-oc="composer.submit">Send</button>
<button data-oc="composer.stop">Stop</button>
<div data-oc="message.last"></div>
<div data-oc="stream.indicator"></div>

<!-- Verne dashboard (owned) -->
<button data-oc="verne.lane.add">Add Lane</button>
<div data-oc="verne.mission.card.1"></div>
```

Configure: `Playwright --test-id-attribute=data-oc` or equivalent in your sidecar.

This is the single highest-return selector reliability change you can make.
