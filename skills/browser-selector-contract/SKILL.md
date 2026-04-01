# browser-selector-contract

**When to use:** Any browser action — click, type, snapshot evaluation, DOM query.

**Enforce this selector hierarchy on every browser action. Always.**

---

## Selector Priority (enforced, not suggested)

### Tier 1 — Explicit automation contract (owned apps)
```javascript
// data-oc attribute is the primary contract for any UI you own
data-oc="element.name"

// Usage in browser act:
browser act ref=[data-oc="composer.submit"]   // ✅ BEST
browser act ref=[data-oc="message.last"]

// Usage in JS evaluation:
document.querySelector('[data-oc="composer.submit"]')
```

**Rule:** If `data-oc` exists on the target element, use it. Always. Outranks all other selectors.

### Tier 2 — Semantic role/name (all apps)
```javascript
// getByRole is the user-semantic standard — mirrors how users perceive UI
getByRole('button', { name: 'Submit' })
getByRole('textbox', { name: 'Search' })
getByRole('menuitem', { name: 'Copy' })

// Common roles: button, textbox, checkbox, radio, menuitem, tab, dialog, alert
```

**Rule:** Tier 2 is the default for third-party apps and when Tier 1 is unavailable.

### Tier 3 — Semantic labels and content
```javascript
// Label associations (form controls)
<label for="email">Email</label>  →  getByRole('textbox', { name: 'Email' })

// Placeholder text
getByPlaceholder('Search...')

// Visible text (exact or substring)
getByText('Submit')
getByText('Cancel', { exact: false })

// Alt text (images)
getByAltText('Profile picture')

// Title attribute
getByTitle('Close dialog')
```

**Rule:** Use when Tier 1/2 is unavailable. Prefer role/name over text.

### Tier 4 — Frame-aware targeting
```javascript
// For controls inside iframes
frameLocator('iframe[name="chat"]')
  .getByRole('button', { name: 'Send' })

// Nested iframes — chain frameLocator()
frameLocator('iframe[name="outer"]')
  .frameLocator('iframe[name="inner"]')
  .getByRole('textbox')
```

**Rule:** Always scope to the correct frame before querying inside iframes.

### Tier 5 — CSS / XPath (emergency only)
```javascript
// CSS — last resort
ref='css:div.container button.primary'

// XPath — only if CSS can't express the relationship
ref='xpath://button[contains(@class, "submit")]'
```

**Rule:** Tier 5 ONLY when Tiers 1-4 cannot express the target. Never prefer CSS/XPath over semantic selectors.

---

## Selector Stability Ranking

```
MOST STABLE (use first)
├── data-oc / data-testid          — explicit automation contract
├── role + name                    — user-semantic, accessibility-aligned
├── label / placeholder / alt      — semantic associations
├── visible text                   — content-based
└── LEAST STABLE (avoid)
    ├── nth-child                  — DOM position, breaks on any insert
    ├── deep descendant (>)        — DOM shape coupling
    ├── generated classes (.x-12)  — build artifact, changes constantly
    └── CSS/XPath chains           — DOM structure coupling
```

---

## OpenClaw browser tool usage

```javascript
// snapshot returns refs — use these directly
browser snapshot profile=openclaw
// → e12: button[name="Submit"][aria-label="Send message"]
// → e48: div[data-oc="message.last"]

// act uses refs directly (deterministic)
browser act kind=click ref=e48

// act can also use CSS/XPath if ref unavailable
browser act kind=click ref='css:button.primary'

// For JS evaluation (chatgpt-dom-driver style)
browser act kind=evaluate fn={() => document.querySelector('[data-oc="composer.submit"]')?.click()}
```

---

## Anti-patterns (never do)

```javascript
// ❌ NEVER use nth-child as primary selector
ref='xpath://div[3]/span[2]/button'  // Breaks on any DOM change

// ❌ NEVER use generated/minified class names
ref='css:.x-12-btn-primary'  // Changes every build

// ❌ NEVER use deep descendant chains
ref='css:html body div#root div.container div.row button'  // Way too fragile

// ❌ NEVER assume DOM position is stable
ref='css:form > div:nth-child(2) > button'  // React rerenders break this

// ❌ NEVER prefer screenshot over structured refs
// Unless: canvas, anti-bot puzzle, or explicit VLM fallback requested
```

---

## Owned UI: Add data-oc attributes

For any UI you control, add `data-oc` attributes to critical elements:

```html
<!-- ChatGPT streaming UI -->
<button data-oc="composer.submit">Send</button>
<button data-oc="composer.stop">Stop generating</button>
<div data-oc="message.last"></div>
<span data-oc="stream.indicator"></span>
<textarea data-oc="composer.input" placeholder="Message ChatGPT..."></textarea>

<!-- Verne dashboard (if you build one) -->
<button data-oc="verne.lane.add">Add Lane</button>
<div data-oc="verne.mission.card.1"></div>
<select data-oc="verne.slot.select"></select>
```

**This is the single highest-return selector reliability change.** One `data-oc` attribute saves multiple failed selector attempts.

---

## Quick Reference Card

```
SELECTOR HIERARCHY (always in order):

1. data-oc="name"           → explicit contract (owned UI)      ⭐ BEST
2. getByRole('role', {name}) → user-semantic (all UI)          ✅ DEFAULT
3. label / placeholder / text → semantic fallbacks              ✅ IF NEEDED
4. frameLocator + above      → iframe boundaries                 ✅ IF NEEDED
5. CSS / XPath              → emergency only                    ⚠️ LAST RESORT

NEVER: nth-child | generated classes | deep chains | position-based
ALWAYS: re-snapshot after navigation (refs change)
```
