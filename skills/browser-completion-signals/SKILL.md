# browser-completion-signals

**When to use:** Waiting for a page/stream/action to finish. Every browser wait.

**Rule: Never use generic page-idle or networkidle as completion signal.**

---

## Why polling fails

```
❌ setTimeout(wait 10s)          — wastes cycles, fires even if done early
❌ networkidle                   — discouraged by Playwright; fires on background traffic
❌ page.waitForLoadState('networkidle') — same problem
✅ waitForResponse()            — event-driven, fires exactly when response finishes
✅ DOM sentinel                  — fires exactly when UI reaches expected state
✅ MutationObserver             — fires exactly when DOM stabilizes
```

---

## Completion Signal Types

### Type 1: Network Response (best for HTTP/GraphQL)
```javascript
// Wait for a specific API response
const response = await page.waitForResponse(
  resp => resp.url().includes('/v1/chat/completions') && resp.status() === 200
);
// Response is the signal — no polling needed
```

### Type 2: WebSocket Frame (best for streaming)
```javascript
// For ChatGPT-style streaming:
page.on('websocket', ws => {
  ws.on('frames', frame => {
    if (frame.payload.includes('[DONE]') || frame.type === 'close') {
      completionSignal.set(true);
    }
  });
});
```

### Type 3: DOM Sentinel (best for UI-driven apps)
```javascript
// Wait for a specific element to appear/change/disappear
await page.waitForSelector('[data-oc="completion-indicator"]', { state: 'hidden' });
// Or for an element to become enabled:
await page.waitForFunction(() => !document.querySelector('button[data-oc="submit"]').disabled);
```

### Type 4: JS Predicate (most flexible)
```javascript
// Custom completion condition
await page.waitForFunction(() => {
  const btn = document.querySelector('button[data-oc="send"]');
  return btn && !btn.disabled && document.querySelector('[data-oc="stream-indicator"]') === null;
});
```

### Type 5: MutationObserver Stabilization (best for "page settled")
```javascript
// Wait for DOM to stop changing (no mutations for N ms)
await page.waitForFunction(() => {
  let lastChange = window.__lastMutationTime || Date.now();
  return Date.now() - lastChange > 1500; // 1.5s of no changes
}, { timeout: 30000 });
```

---

## Site-Specific Registries

### ChatGPT (/chatgpt.com)
```javascript
completion: {
  arm: async (page) => {
    // Before sending: arm the response watcher
    const responsePromise = page.waitForResponse(
      r => r.url().includes('/v1/chat/completions'),
      { timeout: 60000 }
    );
    return { responsePromise };
  },
  
  poll: async (page) => {
    // isGenerating() returns true while stop button visible
    return await page.evaluate(() => {
      const stopBtn = document.querySelector('button[data-testid="stop-button"]');
      return !stopBtn; // true = complete, false = still generating
    });
  },
  
  stable: async (page) => {
    // DOM stable = no mutations for 1.5s
    return await page.evaluate(() => {
      const last = window.__lastMutationTime || 0;
      return Date.now() - last > 1500;
    });
  },
  
  signals: ['responseReceived', 'stopButtonGone', 'domStable_1500ms']
}
```

### Generic HTTP app
```javascript
completion: {
  arm: async (page) => {
    return { responsePromise: page.waitForResponse(r => r.status() === 200, { timeout: 30000 }) };
  },
  signals: ['response_200']
}
```

---

## Composite Completion Pattern

For ChatGPT-like streaming UIs, completion requires ALL signals to align:

```
Step 1: ARM   → before action: arm waitForResponse()
Step 2: ACT   → perform the action
Step 3: WAIT  → poll isGenerating() every 2s
Step 4: VERIFY → response received AND stop button gone AND DOM stable 1.5s
Step 5: READ  → extract response content
```

```javascript
async function waitForChatGPTCompletion(page) {
  // 1. Arm
  const responsePromise = page.waitForResponse(
    r => r.url().includes('/v1/chat/completions'),
    { timeout: 90000 }
  );
  
  // 2. Act (caller already sent message)
  
  // 3. Wait with polling
  let attempts = 0;
  while (attempts < 60) { // max 2 min
    const generating = await page.evaluate(() => {
      return !!document.querySelector('button[data-testid="stop-button"]');
    });
    if (!generating) break;
    await page.waitForTimeout(2000);
    attempts++;
  }
  
  // 4. Verify stability (1.5s of no DOM mutations)
  await page.waitForTimeout(1500);
  
  // 5. Done
  return true;
}
```

---

## Anti-Patterns

```javascript
❌ await page.waitForLoadState('networkidle')  // Playwright explicitly warns against this
❌ await page.waitForTimeout(10000)              // Blind polling, wastes time
❌ await page.waitForSelector('body')            // Fires too early
❌ // any form of screenshot polling             // Expensive, unreliable

✅ await page.waitForResponse(predicate)
✅ await page.waitForSelector('[data-oc="done"]', { state: 'hidden' })
✅ await page.waitForFunction(predicate)
✅ MutationObserver for stabilization
```

---

## Quick Reference

```
COMPLETION SIGNALS (in priority order):

HTTP/streaming  → waitForResponse()      ⭐ BEST for API calls
WebSocket      → websocket frame event  ⭐ BEST for streaming  
DOM change     → waitForSelector()       ✅ DEFAULT for UI
Custom state   → waitForFunction()       ✅ FLEXIBLE
DOM stable     → MutationObserver timer  ✅ FINAL VERIFY

NEVER: networkidle | blind timeout | screenshot polling
```
