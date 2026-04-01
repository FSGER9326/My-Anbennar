# browser-chat-streaming

**When to use:** ChatGPT, Claude, or any LLM chat interface with streaming responses.

**Completion detection for streaming UIs — event-driven, not polling.**

---

## The 3-Signal Composite Pattern

ChatGPT-like streaming requires **ALL 3 signals to align** before reading the response:

```
Signal 1: Transport done    → HTTP response received (waitForResponse)
Signal 2: UI Sentinel      → Stop button gone (DOM query: isGenerating === false)
Signal 3: DOM Stable       → No mutations for 1.5s (MutationObserver debounce)
```

Completion = `Signal1 AND Signal2 AND Signal3`

---

## Implementation

```javascript
// CHATGPT EXAMPLE

async function chatGPTCompletionWatcher(page) {
  // 1. ARM transport watcher BEFORE sending
  const responsePromise = page.waitForResponse(
    r => r.url().includes('/v1/chat/completions') && r.status() === 200,
    { timeout: 90000 }
  );

  // 2. ACT — message already sent by caller

  // 3. WAIT for UI sentinel (Stop btn gone)
  let attempts = 0;
  while (attempts < 60) { // max 2 min
    const isGenerating = await page.evaluate(() => {
      const stopBtn = document.querySelector('button[data-testid="stop-button"]');
      return !!stopBtn; // true = still generating
    });
    if (!isGenerating) break;
    await page.waitForTimeout(2000); // poll every 2s
    attempts++;
  }

  if (attempts >= 60) {
    throw new Error('ChatGPT taking too long (>2min). Check manually.');
  }

  // 4. VERIFY DOM stable (1.5s of no mutations)
  // We simulate this with a short wait since MutationObserver requires setup
  await page.waitForTimeout(1500);

  // 5. DONE — safe to read response
  return true;
}
```

---

## DOM Micro-Queries (chatgpt-dom-driver.js)

These are the stable ChatGPT DOM queries (from `scripts/chatgpt-dom-driver.js`):

```javascript
// Check if still generating
isGenerating(): boolean
  → document.querySelector('button[data-testid="stop-button"]') !== null

// Check if complete (Regenerate button visible)
isComplete(): boolean
  → document.querySelector('button[aria-label*="Regenerate"]') !== null

// Check for errors
getError(): string | null
  → document.querySelector('[role="alert"]')?.innerText

// Check if can send
canSend(): boolean
  → document.querySelector('button[data-testid="send-button"]')?.disabled === false

// Get last assistant message
getLastAssistantText(): string
  → document.querySelectorAll('[data-message-author-role="assistant"]').last?.innerText

// Get full UI state in one call
getUIState(): { generating, complete, canSend, error, turnCount, inputLength, assistantCount }
```

---

## Claude AI (claude.ai)

```javascript
async function claudeCompletionWatcher(page) {
  // Arm network response
  const responsePromise = page.waitForResponse(
    r => r.url().includes('/api/chat/stream'),
    { timeout: 90000 }
  );

  // Wait for streaming to stop — submit button re-enabled
  let attempts = 0;
  while (attempts < 60) {
    const stillStreaming = await page.evaluate(() => {
      // Claude shows a "stop" button or disables submit during streaming
      const submitBtn = document.querySelector('[data-testid="submit-button"]');
      return submitBtn?.disabled === true;
    });
    if (!stillStreaming) break;
    await page.waitForTimeout(2000);
    attempts++;
  }

  // DOM stable
  await page.waitForTimeout(1500);

  return true;
}
```

---

## Generic Streaming Completion

```javascript
async function genericStreamingCompletion(page) {
  // Strategy: arm ALL of these
  const responses = [];
  const wsFrames = [];
  
  // Network response
  page.on('response', r => {
    if (r.url().includes('/chat') || r.url().includes('/message')) {
      responses.push(r);
    }
  });
  
  // WebSocket frames (if streaming)
  page.on('websocket', ws => {
    ws.on('frames', frame => {
      wsFrames.push(frame);
    });
  });

  // Poll DOM sentinel every 2s
  let attempts = 0;
  while (attempts < 60) {
    const done = await page.evaluate(() => {
      // Custom per-app — replace with actual sentinel
      const spinner = document.querySelector('[data-testid="spinner"]');
      const stopBtn = document.querySelector('button[aria-label*="Stop"]');
      return !spinner && !stopBtn;
    });
    if (done) break;
    await page.waitForTimeout(2000);
    attempts++;
  }

  // Stabilize
  await page.waitForTimeout(1500);
  
  return responses.length > 0 || wsFrames.some(f => f.type === 'close');
}
```

---

## Common Sentinel Patterns

| App | Sentinel | How to detect |
|-----|----------|---------------|
| ChatGPT | Stop button gone | `button[data-testid="stop-button"]` null |
| Claude | Submit re-enabled | `[data-testid="submit-button"]` disabled === false |
| Gemini | Thinking indicator gone | `[data-testid="thinking-indicator"]` hidden |
| Grok | Response complete | Regenerate button visible |
| Generic | Spinner hidden | `[role="progressbar"]` removed from DOM |

---

## WebSocket Detection

```javascript
// For apps that stream over WebSocket
page.on('websocket', ws => {
  console.log('WebSocket opened:', ws.url());
  
  ws.on('frames', frame => {
    // Most streaming protocols send '[DONE]' or similar on completion
    if (frame.payload.includes('[DONE]') || 
        frame.payload.includes('[FINISH]') ||
        frame.type === 'close') {
      console.log('Stream complete via WebSocket');
    }
  });
  
  ws.on('close', () => {
    console.log('WebSocket closed — stream ended');
  });
});
```

---

## Anti-Patterns

```javascript
// ❌ NEVER use networkidle
await page.waitForLoadState('networkidle')  // Wrong — fires on background traffic

// ❌ NEVER blind timeout
await page.waitForTimeout(30000)  // Too long if done early, too short if slow

// ❌ NEVER poll screenshot
while (takingScreenshot()) await page.waitForTimeout(2000)  // Expensive, slow

// ❌ NEVER trust "body visible" as completion
await page.waitForSelector('body')  // Fires way too early

✅ ALWAYS arm transport watcher before acting
✅ ALWAYS use DOM sentinel (Stop btn, spinner, submit re-enabled)
✅ ALWAYS verify DOM stability (1.5s MutationObserver debounce)
```

---

## Quick Reference

```
STREAMING COMPLETION (ChatGPT example):

1. ARM   → waitForResponse('/v1/chat/completions')
2. ACT   → clickSend()
3. WAIT  → poll isGenerating() every 2s until false
4. VERIFY → waitForTimeout(1500ms) for DOM stable
5. READ  → getLastAssistantText()

ALL 3 signals: transport + sentinel + stable

NEVER: networkidle | blind timeout | screenshot polling
```
