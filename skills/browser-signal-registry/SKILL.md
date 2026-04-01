# browser-signal-registry

**Plugin:** `browser-signal-registry`
**CLI:** `openclaw signal list | show <site> | check <url>`

**Purpose:** Source of truth for how to detect "done" on any given website.

---

## Why a Registry?

Every browser task needs to answer one question: **"When is this page done?"**

Without a registry, every agent has to re-infer the answer each time. With a registry, the signal policy is pre-loaded and consistent.

The registry is the **Signal Registry** in the 5-layer browser architecture:
```
Policy Skills → Structured Snapshot/Ref → [Signal Registry] → Lease Manager → Model Router
```

---

## Core Concept: Completion = ALL Signals Fire

For a given site, completion requires **ALL signals** to fire:

```
ChatGPT completion = HTTP response (200)  ← AND
                   Stop button gone        ← AND
                   DOM stable 1.5s
```

One signal firing doesn't mean done. **All of them.**

---

## Signal Types

| Type | Description | Best For |
|------|-------------|----------|
| `network` | waitForResponse with URL/status match | API calls, streaming endpoints |
| `websocket` | WebSocket frame or close event | Real-time streaming (SSE, WebSocket) |
| `dom` | Element appears/disappears/enables | UI state changes |
| `predicate` | JS expression evaluated in page | Custom conditions |
| `stable` | No DOM mutations for N ms | Final verification only |

---

## CLI Usage

```bash
# List all registered sites
openclaw signal list

# Show detailed signals for a site
openclaw signal show chatgpt.com

# Check which site a URL matches
openclaw signal check https://claude.ai/chat/abc123
```

---

## Adding a New Site

Edit `src/signal-registry.ts`. Add an entry to `SIGNAL_REGISTRY`:

```typescript
'myapp.com': {
  name: 'My App',
  url: 'https://myapp.com',
  completionSignals: [
    {
      type: 'network',
      urlPattern: '/api/chat',
      status: 200,
      timeout: 60000,
    },
    {
      type: 'dom',
      selector: 'button[data-testid="stop-button"]',
      state: 'hidden',
      timeout: 120000,
    },
    {
      type: 'stable',
      duration: 1500,
      timeout: 30000,
    },
  ],
  microQueries: {
    generatingIndicator: 'button[data-testid="stop-button"]',
    completeIndicator: 'button[aria-label*="Regenerate"]',
    errorSelector: '[role="alert"]',
    canSendSelector: 'button[data-testid="send-button"]',
  },
  knownTraps: [
    // selectors that give false signals
    '.stretching-anchor',
  ],
},
```

---

## Built-in Sites

| Site | Signals |
|------|---------|
| chatgpt.com | network(/v1/chat/completions) + dom(stop gone) + stable(1.5s) |
| claude.ai | network(/api/chat/stream) + dom(submit enabled) + stable(1.5s) |
| gemini.google.com | network(/v1beta/models) + dom(thinking gone) + stable(1.5s) |
| __generic__ | network(200) + stable(2s) — fallback |

---

## Micro-Queries

The `microQueries` section provides pre-built DOM query helpers:

```javascript
// From chatgpt-dom-driver.js style:
// Check if generating
document.querySelector('button[data-testid="stop-button"]') !== null

// Check if complete
document.querySelector('button[aria-label*="Regenerate"]') !== null

// Check for error
document.querySelector('[role="alert"]')?.innerText

// Can send next message?
document.querySelector('button[data-testid="send-button"]')?.disabled === false
```

---

## Known Traps

Some selectors give **false signals**. List them in `knownTraps`:

```typescript
// ChatGPT: this element stretches and triggers false "generating" states
knownTraps: ['[data-testid="stretching-anchor"]']
```

Agents should **ignore or filter out** signals from known trap selectors.

---

## Integration Points

The signal registry integrates with:
- **browser-lease-manager** — reads signals when acquiring a lease
- **Completion watcher** — implements the signal logic (network + DOM + stable)
- **LLM prompts** — `summarizeSignals(site)` injects signal summary into context

```javascript
import { getSiteSignals, summarizeSignals } from './signal-registry.js';

const site = getSiteSignals('https://chatgpt.com');
console.log(summarizeSignals(site));
// "network(chat/completions, 200) + dom(hidden:stop-button) + stable(1500ms)"
```
