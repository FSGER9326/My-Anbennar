# browser-vision-fallback

**When to use:** Text-first browser control failed, page is visually ambiguous, canvas/rendering app, anti-bot puzzle, or accessibility-poor widget.

**Rule: Vision fallback is escalation, not the primary path.**

---

## When to Escalate

```
Escalate to VLM/screenshot when ALL of:
  1. Structured refs unavailable (no data-oc, no semantic role)
  2. Page is canvas-heavy, rendering-intensive, or inaccessible
  3. Anti-bot puzzle detected (CAPTCHA, challenge iframe)
  4. DOM micro-queries return no stable anchor
  5. Human explicitly requests visual analysis
```

**Never screenshot-first.** Always try structured snapshot + DOM driver first.

---

## Before Taking Screenshot

```javascript
// 1. Always grab structured snapshot first
browser snapshot profile=openclaw
// → refs available even if you can't click them

// 2. Document what refs exist and what they map to
// → e12: canvas#render-surface (unclickable)
// → e48: div.toolbar (visible but no semantic role)

// 3. If refs exist but are insufficient → THEN screenshot
```

---

## Screenshot + VLM Prompt Template

```
Context:
- URL: {url}
- Current page state: {snapshot_summary}
- Target element: {description of what you're looking for}
- Refs on page: {list of refs with descriptions}

Image: [screenshot]

Task: Describe what you see at the target location, 
or identify the correct element to click for: {goal}

Response format:
{
  "element": "description",
  "action": "click | type | read | skip",
  "confidence": 0.0-1.0,
  "reasoning": "brief"
}
```

---

## Common Visual Escalation Cases

### Case: Canvas app (Figma, Excalidraw, game)
```
Problem: Canvas elements have no DOM refs
Escalation: Screenshot + VLM with coordinates
VLM prompt: "This is a canvas app. Given the goal to click the 'Export' button,
             what coordinates relative to the canvas should be clicked?"
Output: { x: 850, y: 120 }
Action: browser act kind=click x=850 y=120
```

### Case: Anti-bot / CAPTCHA
```
Problem: Challenge iframe or CAPTCHA detected
Escalation: Screenshot + VLM to read challenge
VLM prompt: "Read the challenge text and any input field.
             What is the challenge? What's the answer?"
Action: 
  - If solvable (image CAPTCHA): solve and type
  - If unsolvable: retire lease, alert human
```

### Case: Inaccessible dropdown / widget
```
Problem: Custom widget with no semantic role
Escalation: Screenshot + VLM
VLM prompt: "This dropdown is inaccessible via DOM.
             Describe what's visible and where to click to open it."
Action: Use coordinates or found text anchor
```

### Case: Ambiguous state (chat not responding)
```
Problem: Can't tell if generating or stuck
Escalation: Screenshot + VLM
VLM prompt: "Is ChatGPT still generating? Is there an error?
             What is the current state of the page?"
```

---

## VLM Tool Paths

```
1. OpenClaw image tool (configured image model)
   → browser screenshot → image tool → description

2. MiniMax Image Understanding (if available via OAuth/MCP)
   → Higher quality for complex scenes

3. External VLM (Claude/GPT-4o) via browser-use or API
   → Fallback for hard visual problems
```

---

## After Visual Escalation

```javascript
// If VLM identifies element:
// → Add to data-oc registry for future runs
// → Update completion signal registry if state misdetected

// If VLM fails:
// → Log to .learnings/browser-vision-failures.md
// → Consider retiring lease if confidence is low
```

---

## Anti-Patterns

```javascript
// ❌ NEVER screenshot-first
browser screenshot → VLM parse → click  // Wasteful, slow

// ❌ NEVER screenshot without structured context
// Always include: URL, refs available, goal

// ❌ NEVER trust VLM coordinates for critical actions
// Always prefer DOM refs if available

// ❌ NEVER escalate for simple form fills
// getByRole('textbox', {name: 'Email'}) works fine
```

---

## Quick Reference

```
ESCALATION PATH:

Text-first failed?
  → Snapshot + DOM micro-queries → still stuck?
    → Check if canvas/anti-bot/inaccessible → YES: screenshot + VLM
    → Otherwise: use getByRole or CSS with caution

VLM prompt MUST include:
  - URL + page summary
  - Available refs
  - Goal (click/type/read)
  - Expected element description

After escalation:
  - Log to .learnings/
  - Add data-oc if found
  - Update signal registry if state misdetected
```
