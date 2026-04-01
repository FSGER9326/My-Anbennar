# ChatGPT UI Reference
**Living document — update when discovering new selectors, patterns, or gotchas**

## Page Structure

### URL Patterns
| URL | What it shows |
|-----|---------------|
| `https://chatgpt.com/` | Home/new chat (lighter page load) |
| `https://chatgpt.com/c/<id>` | Existing conversation |
| `https://chatgpt.com/g/g-p-<id>-<slug>/project` | Project page (HEAVY — nested iframes, may crash browser tool) |
| `https://chatgpt.com/g/g-p-<id>-<slug>/c/<id>` | Chat within a project |
| `https://chatgpt.com/library` | Images gallery |
| `https://chatgpt.com/deep-research` | Deep Research hub |

### Model Selection
The model selector dropdown (ref: `button[aria-label="Model selector"]`) shows available models:
- **Instant** — "For everyday chats" (fastest)
- **Thinking** — "For complex questions" (o3/o4-mini extended reasoning)
- **Pro** — "Research-grade intelligence" (best reasoning, NO image generation)
- **Configure...** — settings

To select a model: click Model selector → click desired model menuitem.

**IMPORTANT:** The model selector button always shows "ChatGPT" regardless of which model is selected. The actual model is determined by the mode buttons in the composer.

### Composer Modes
The chat input area has toggle buttons that change the active mode:

| Button text | When active | What it means |
|-------------|-------------|---------------|
| "Extended thinking, click to remove" | Extended thinking ON | Model uses extended reasoning chain |
| "Extended Pro, click to remove" | Extended Thinking + Pro model | Extended thinking with Pro model (best reasoning) |
| "Deep research, click to remove" | Deep Research ON | Multi-step web research (5-15 min) |
| "Extended thinking" | OFF (click to enable) | Standard mode, no extended reasoning |
| "Deep research" | OFF (click to enable) | Standard mode |

**Note:** When you select Pro model from the model selector, the composer shows "Extended Pro" instead of separate "Extended thinking" buttons. Deep Research is a separate toggle that appears in the Openclaw project.

### Chat Input
- **Visible input:** `div[contenteditable="true"]` (ProseMirror editor, NOT a textarea)
- **Hidden textarea:** `textarea#prompt-textarea` (fallback, class `wcDTda_fallbackTextarea`)
- **Placeholder:** "Ask anything" or "Chat with ChatGPT"
- **Send button:** `button[data-testid="send-button"]` or `button[aria-label*="Send"]`

**Filling text:** Use `contenteditable` div, not textarea:
```js
const el = document.querySelector('div[contenteditable="true"]');
el.focus();
el.textContent = text;
el.dispatchEvent(new Event('input', {bubbles: true}));
```

### Send/Action Buttons
| Button | Selector | When visible |
|--------|----------|-------------|
| Send | `button[data-testid="send-button"]`, `button[aria-label="Send prompt"]` | After typing |
| Stop | `button[data-testid="stop-button"]` | While generating |
| Regenerate | `button[aria-label*="Regenerate"]` | After response complete |
| Copy | `button[aria-label*="Copy"]` | After response complete |

### Conversation Content
| Element | Selector | Notes |
|---------|----------|-------|
| Assistant message | `[data-message-author-role="assistant"]` | The wrapper div |
| Assistant markdown | `.markdown` inside assistant msg | Clean text container |
| User message | `[data-message-author-role="user"]` | User wrapper |
| Conversation turn | `[data-testid^="conversation-turn-"]` | Each turn (user + assistant) |

## Deep Research Page Structure

### The Deep Research Card
Deep Research reports render inside a **nested cross-origin iframe**:
```
Main page
└── iframe (ChatGPT response container)
    └── iframe (Deep Research sandbox)
        └── connector_openai_deep_research.web-sandbox.oaiusercontent.com
```

**This iframe is VERY HEAVY.** The OpenClaw browser tool's `gateway` often crashes when:
- Scrolling within Deep Research pages
- Trying to access elements inside the nested iframe
- Running `evaluate()` on the page (memory spike)

### Deep Research Card Elements (inside nested iframe)
| Element | Description |
|---------|-------------|
| Title | Report title |
| "Research completed in Xm · N citations · M searches" | Header stats |
| **Export button** (↓ icon) | Opens dropdown |
| **Expand button** (↗ icon) | Expands to full screen |
| Export dropdown options | "Copy contents", "Export to Markdown", "Export to Word", "Export to PDF" |

### How to Extract Deep Research Content

**DO NOT use the OpenClaw browser tool for Deep Research extraction.** It crashes.

**Use Playwright sidecar instead** (`scripts/download-deep-research.js`):
```js
const { chromium } = require('playwright-core');
const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
const page = await browser.contexts()[0].newPage();
await page.goto(url, { waitUntil: 'load', timeout: 60000 });
await page.waitForTimeout(8000);

// Navigate nested iframes
const innerFrame = page.frameLocator('iframe').first().frameLocator('iframe').first();

// Click Export → Export to Markdown
await innerFrame.getByRole('button', { name: 'Export' }).first().click();
await page.waitForTimeout(1000);
await innerFrame.getByText('Export to Markdown').click();

// Wait for download
const download = await page.waitForEvent('download', { timeout: 120000 });
await download.saveAs(outputPath);
```

**Proven selectors that work:**
- `page.frameLocator('iframe').first().frameLocator('iframe').first()` — gets the Deep Research sandbox iframe
- `getByRole('button', { name: 'Export' })` — Export button (use `.first()` if multiple)
- `getByText('Export to Markdown')` — Markdown download option

## Sidebar

### Sidebar Structure
| Element | Selector | Notes |
|---------|----------|-------|
| Open sidebar | `button[aria-label="Open sidebar"]` | Shows sidebar |
| Close sidebar | `button[aria-label="Close sidebar"]` | Hides sidebar |
| New chat | `[data-testid="create-new-chat-button"]` | Start new chat |
| Projects list | `button:has-text("Projects")` | Expandable |

### Sidebar Gotcha
The sidebar `div#stage-slideover-sidebar` intercepts pointer events even when `aria-expanded="false"`. Playwright clicks on "Close sidebar" or "New chat" inside the sidebar area will timeout because the overlay div intercepts.

**Solution:** Navigate directly via URL instead of clicking sidebar buttons:
- New chat: `page.goto('https://chatgpt.com/')` instead of clicking "New chat"
- Open project: `page.goto('https://chatgpt.com/g/g-p-<id>/project')` instead of clicking

## Navigation

### Efficient Navigation Pattern
```js
// New chat (fastest)
await page.goto('https://chatgpt.com/', { waitUntil: 'load', timeout: 30000 });
await page.waitForTimeout(8000);  // Wait for JS hydration

// Open existing chat
await page.goto('https://chatgpt.com/c/<id>', { waitUntil: 'load', timeout: 30000 });

// Open project page (HEAVY — may timeout!)
await page.goto('https://chatgpt.com/g/g-p-<id>/project', { waitUntil: 'domcontentloaded', timeout: 30000 });
await page.waitForTimeout(10000);
```

### `waitUntil` Strategy
- **`load`** — best for ChatGPT pages (DOM ready, resources loading)
- **`domcontentloaded`** — fallback for project pages
- **`networkidle`** — NEVER use on ChatGPT (background connections never settle)

## Playwright Sidecar (CDP Connection)

### When to use the sidecar instead of OpenClaw browser tool
- Deep Research page interaction (cross-origin iframe)
- Any page that causes gateway timeout/crash
- Download automation (export reports)
- When you need `frameLocator` for nested iframes

### Connection
```js
const { chromium } = require('playwright-core');
const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
```

### Known Gotchas
1. **Project pages time out** — ChatGPT project URLs (`/g/g-p-.../project`) are very heavy. Use `https://chatgpt.com/` instead when possible.
2. **Sidebar overlay** — the sidebar div intercepts clicks even when closed. Navigate via URL, don't click sidebar buttons.
3. **ProseMirror input** — ChatGPT uses contenteditable div, not textarea. Must use `el.textContent = text` + `dispatchEvent(new Event('input', {bubbles:true}))`.
4. **Deep Research iframe** — `page.frameLocator('iframe').first().frameLocator('iframe').first()` for nested cross-origin.
5. **Wait times** — ChatGPT needs 8+ seconds after page load for JS hydration before interacting.

## Response Detection

### Check if generating
```js
document.querySelector('button[data-testid="stop-button"]') !== null
```

### Check if response complete
```js
document.querySelector('button[aria-label*="Regenerate"]') !== null
```

### Get last assistant text
```js
const msgs = document.querySelectorAll('[data-message-author-role="assistant"]');
const last = msgs[msgs.length - 1];
(last?.querySelector('.markdown')?.innerText || last?.innerText || '').trim();
```

### Get all assistant texts
```js
Array.from(document.querySelectorAll('[data-message-author-role="assistant"]'))
  .map(m => (m.querySelector('.markdown')?.innerText || m.innerText).trim());
```

## Rate Limits
ChatGPT Plus has rate limits on the web UI. Detection:
- Text appears in UI: "You've reached our limit of messages per hour. Please try again later."
- Element appears as `[role="alert"]` or error banner
- The `getError()` function from chatgpt-dom-driver.js checks for this

## Performance Metrics (measured)
| Interaction | Time | Method |
|-------------|------|--------|
| Page load → interactable | 8-10s | `waitForTimeout(8000)` |
| Type + send prompt | 1-2s | contenteditable fill + click |
| Response wait (Deep Research) | 5-15min | Wait for Regenerate button |
| Response wait (regular chat) | 10-60s | Wait for Regenerate button |
| Export Deep Research via sidecar | ~90s | goto + frameLocator + click + download |
| Full page snapshot (OpenClaw) | 15-30s | browser snapshot (HEAVY) |
| JS evaluate (OpenClaw) | 1-3s | browser act kind=evaluate |
| Playwright evaluate | <1s | page.evaluate() via sidecar |

## ChatGPT Projects
Projects group conversations with shared sources and instructions:
- **Modding** (`g-p-69cb9f6f4efc819188e90b492c235334-modding`) — Verne modding work
- **Openclaw** (`g-p-69cce3fc61e08191aa7d0f48ee2487ef-openclaw`) — Agent self-improvement
- **Verne Art** (`g-p-69cc42e831648191ab13873705111e51-verne-art`) — DALL-E art

**Key difference:** Project pages are HEAVY (nested iframes for sources panel, project settings). Regular `chatgpt.com/c/` pages are much lighter.

### Project vs Non-Project
- **Project pages:** Sources tab (GitHub, Google Drive), project-specific instructions, heavier DOM
- **Non-project pages:** Standard ChatGPT, lighter, more reliable for automation

**Rule:** Use non-project pages (`chatgpt.com/c/`) for automation tasks. Only use project pages when you need project sources/instructions.
