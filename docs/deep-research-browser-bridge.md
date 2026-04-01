# Hardening and Accelerating an OpenClaw Browser Bridge to ChatGPT Web UI

## Executive summary

Your current “snapshot → parse DOM → act → snapshot” bridge is slow mostly because it treats *every* step as a full-page scrape and re-discovery problem, and fragile because React re-renders invalidate the ephemeral element references OpenClaw returns (OpenClaw explicitly notes refs aren’t stable and you should re-snapshot when actions fail). citeturn9view2turn2view0

The fastest path to a major improvement is **not** to perfect UI automation for everything, but to (a) **move the heavy lifting off the UI** using the **OpenAI Responses API and Deep Research API**, and (b) when the UI is truly required, **turn “full snapshots” into “micro-queries”** using OpenClaw’s built-in **JavaScript evaluation** + **selector waits** + **scoped/efficient snapshots**. OpenClaw supports `browser act kind=evaluate` / `openclaw browser evaluate` (arbitrary JS in page context) and powerful waits (URL/load/selector/JS predicate). citeturn9view0turn9view2

Two particularly high-impact discoveries for your use case:

- **Deep Research is available via API**: OpenAI provides deep research models (e.g., `o3-deep-research`, `o4-mini-deep-research`) through the **Responses API**—built for multi-step browsing + synthesis and designed to run for minutes with **background mode** + polling/webhooks. citeturn7search0turn8search1turn8search24turn16view1turn16view2  
- **OpenClaw already has “missing” capabilities you listed**: it supports **JS evaluation**, **file upload hooks**, **tab management**, and **scoped snapshots** (e.g., `snapshot --selector`, `--efficient`). Also, OpenClaw intentionally does **not** support CSS selectors *directly* for click/type actions (refs are required), which means your “selector-based act” idea needs to be implemented via `evaluate()` (or via a custom plugin/sidecar that exposes Playwright locators). citeturn9view2turn9view0

## What OpenClaw’s browser tool can and cannot do today

OpenClaw’s browser tool is deliberately designed around: **(1) snapshots that return refs** and **(2) `act` operations that use those refs**, to avoid brittle selectors. The docs spell out that **CSS selectors are intentionally not supported for actions** like click/type; you must act via snapshot refs (numeric or role refs like `e12`). citeturn9view2turn2view0

At the same time, several of your pain points are already addressable:

- **Direct DOM access via JS evaluation exists**: OpenClaw supports `browser act kind=evaluate` / `openclaw browser evaluate` and `wait --fn` (JS predicate waits). citeturn9view0turn9view2  
- **Scoped and “efficient” snapshots exist**: role snapshots can be scoped (`--selector`) and “efficient” presets reduce payload. citeturn9view2turn2view0  
- **Uploads have first-class support**: OpenClaw supports `openclaw browser upload ...` and notes upload is an “arming call” you run before triggering a chooser; it can also set file inputs via `--input-ref` or `--element`. citeturn9view2turn9view0  
- **Tab orchestration is available**: the browser tool/CLI and control API include tab operations (`GET /tabs`, `POST /tabs/open`, `POST /tabs/focus`, etc.), plus snapshots/actions endpoints. citeturn9view1turn11view2  
- **Internals matter for performance**: OpenClaw’s browser control server connects to Chromium via **CDP**, and for advanced actions (click/type/snapshot/PDF), it uses **Playwright on top of CDP**. citeturn9view1  

Security note: OpenClaw explicitly warns that evaluation and JS predicate waits execute arbitrary JavaScript in the page context and can be impacted by prompt injection; it can be disabled via configuration (`browser.evaluateEnabled=false`). citeturn9view0

## Browser automation improvements that work with OpenClaw’s design

### Reduce “resnapshot churn” with waits and smaller snapshots

Right now you pay the full cost of a snapshot just to learn that “ChatGPT is still generating” or “the last response appended.” Use `wait` for synchronization and take fewer snapshots:

- OpenClaw supports waiting for a selector to be visible, waiting for URL patterns, load state (e.g., `networkidle`), and even a JS predicate. citeturn9view2  
- For ChatGPT UI, you can often wait for a UI state transition (e.g., “Stop generating” disappears, “Send” enabled, “Regenerate” appears) instead of polling snapshots.

Even if you still need snapshot refs for clicks, you can make snapshots cheaper:
- Prefer `snapshot --efficient` or configure snapshot defaults to efficient mode. citeturn2view0turn9view2  
- Use `snapshot --selector "<container>"` to scope the snapshot to the composer or the message thread, rather than parsing the entire page. citeturn9view1turn9view2  

### Use `evaluate()` as your “selector-based action” escape hatch

Because OpenClaw doesn’t support `click(selector)` directly (by design), the practical way to do selector-based targeting is:

1) Use `evaluate()` to locate elements with `document.querySelector(...)` and
2) Trigger actions (`click()`, setting `value`, dispatching events) from inside the page context.

OpenClaw documents evaluation support explicitly. citeturn9view0

This approach has tradeoffs:
- It can be **faster** (no need to snapshot just to find a stable target).
- It can be **more brittle** if you target unstable classnames.
- It’s often **very robust** if you target `data-testid`, ARIA labels, roles, or stable IDs—exactly the locator philosophy Playwright recommends (e.g., role-based locators). citeturn4search3turn5search4  

### Adopt Playwright locator best practices (even if you’re not directly running Playwright code)

OpenClaw role snapshots are internally resolved with Playwright `getByRole(...)` (and `nth()` for duplicates). citeturn9view2  
So you benefit by thinking “Playwright-first”:

- Prefer **role/name** targeting over brittle CSS paths. Playwright emphasizes `getByRole()` and accessible names as a stable way to locate UI elements as users perceive them. citeturn4search3turn4search30  
- Shadow DOM is not a blocker if you move to a Playwright-driven bridge: Playwright’s docs state locators work with Shadow DOM by default (XPath is an exception, and closed shadow roots are not supported). citeturn6search1turn6search0  

If you decide to replace the OpenClaw bridge with a sidecar “real Playwright driver,” you can also integrate via MCP: Microsoft provides a Playwright MCP server designed for LLM browser automation using accessibility snapshots. citeturn13view4

## Programmatic DOM extraction for ChatGPT UI

To stop wasting time snapshotting the whole page just to extract the last assistant paragraph, treat ChatGPT’s DOM as an API surface and query it directly.

### Observed stable-ish selectors used in real implementations

Multiple open-source implementations converge on a handful of selectors that tend to survive UI refactors better than classnames:

- Prompt input commonly appears as **`textarea#prompt-textarea`** or **`textarea[data-testid="prompt-textarea"]`**. citeturn13view0turn13view1  
- Send button often uses **`button[data-testid="send-button"]`**. citeturn13view0turn13view1  
- While generating, a **Stop** button may appear (e.g., `button[data-testid="stop-button"]`), and can be used as a “busy indicator.” citeturn13view0  
- Messages may be marked with **`[data-message-author-role="assistant"]`** and **`[data-message-author-role="user"]`**; assistant markdown content may be inside a `.markdown` container. citeturn13view0  
- Another widely used approach is to select conversation turns via **`[data-testid^="conversation-turn-"]`** and take the last one. citeturn13view1  

These selectors appear in:
- `chrome-ai-bridge`, which centralizes selector fallbacks for ChatGPT and includes `data-testid`-based targets and `data-message-author-role`. citeturn13view0  
- A Playwright automation gist that waits for “Regenerate,” queries `[data-testid^="conversation-turn-"]`, and returns the last turn text. citeturn13view1  

### Completion detection without polling full snapshots

A pragmatic completion strategy seen in production scripts:

- Wait for `button:has-text("Regenerate")` (or the localized equivalent) after sending. citeturn13view1  
- Or poll the presence/absence of a “stop generating” control (`data-testid="stop-button"` / aria-label contains “Stop generating”). citeturn13view0  

In OpenClaw terms, the pattern becomes:
- `browser act kind=evaluate` to send message (fill textarea + press Enter), then
- `browser wait "<selector>"` to block until completed, then
- `browser act kind=evaluate` to extract final text.

### A concrete OpenClaw-style “micro-query” snippet

This is the core idea: keep your UI tab open, and replace most snapshots with fast eval calls.

```js
// Intended to run via OpenClaw `browser act kind=evaluate` / `openclaw browser evaluate`.
// Returns { generating, lastAssistantText }.

(() => {
  const stopBtn =
    document.querySelector('button[data-testid="stop-button"]') ||
    document.querySelector('button[aria-label*="Stop"]') ||
    document.querySelector('button[aria-label*="Stop generating"]');

  const assistantNodes = Array.from(
    document.querySelectorAll('[data-message-author-role="assistant"]')
  );

  // Prefer markdown text if present, else fall back to node innerText.
  const last = assistantNodes[assistantNodes.length - 1];
  const lastMarkdown = last?.querySelector?.(".markdown");
  const lastAssistantText = (lastMarkdown?.innerText || last?.innerText || "").trim();

  return {
    generating: Boolean(stopBtn),
    lastAssistantText
  };
})();
```

The selectors used above are grounded in real-world selector sets for ChatGPT automation. citeturn13view0  
And OpenClaw’s ability to run page JS is documented. citeturn9view0

### Rate limit and error detection via DOM

Instead of scanning the entire snapshot for “messages remaining,” detect error UI elements in a structured way:

- `chrome-ai-bridge` includes fallback selectors for error banners like `[role="alert"]` and `[data-testid="error-message"]`. citeturn13view0  

This can power a lightweight “UI health check” that returns:
- `{ ok: true/false, errorText, generating, canSend }`
without ever taking a snapshot.

### Conversation continuity: stop treating “new chat” as “new tab”

Two different ways to solve continuity:

- **UI-based continuity**: keep a single persistent browser profile (your `profile=openclaw`) and reuse the same ChatGPT tab; OpenClaw supports cookies/storage operations and clearly warns that the profile stores logged-in sessions (so you should treat it as sensitive). citeturn9view0turn9view1  
- **Automation-based continuity**: Playwright automation frameworks typically persist login via storage state; for example, `chatgpt-automation-mcp` states it maintains login state across runs using Playwright storage state. citeturn14view0  

A third (optional) approach is “export-based continuity”: ChatGPT supports share links for conversations. citeturn3search7 Tools exist to download shared conversation links into Markdown (example repo: `chatgpt_shared_conversation_to_markdown_file`). citeturn4search25  
This is more relevant if you decide “UI writes, separate pipeline reads.”

## Alternatives to a ChatGPT web-UI bridge

### Use the official OpenAI API for most work

The OpenAI **Responses API** is designed for multi-turn, stateful interactions, with built-in tools (web search, file search, computer use, remote MCP servers, etc.). citeturn7search29turn8search30

For your specific “Thinking vs Instant” problem, the API gives you a knob:
- The reasoning guide shows `reasoning.effort` (values depend on model) to trade latency/cost for deeper reasoning. citeturn16view3turn8search0  

For your “Deep Research not automated” problem, the API gives you an even bigger lever:

- OpenAI’s deep research guide states you can use deep research by calling the Responses API with models like `o3-deep-research` or `o4-mini-deep-research`, and you must provide at least one data source such as web search, remote MCP, or file search. citeturn7search0turn7search15turn7search24  
- Deep research is recommended to run in **background mode** because it can take minutes; background mode enables asynchronous execution and polling. citeturn7search15turn8search1  
- OpenAI webhooks can notify you when background work completes, reducing the need even for polling. citeturn8search24  

In other words: the entire “click Deep Research, wait 5–15 minutes, keep snapshotting” workflow can be replaced with a single API call + webhook/poll.

### Cost comparison vs UI bridging

By April 2026 pricing:

- API pricing for `gpt-5.4` is $2.50 / 1M input tokens and $15.00 / 1M output tokens (cached input is cheaper). citeturn16view0  
- Deep research model pricing (example): `o3-deep-research` lists $10 / 1M input tokens and $40 / 1M output tokens. citeturn16view1  
- Faster deep research (`o4-mini-deep-research`) lists $2 / 1M input tokens and $8 / 1M output tokens. citeturn16view2  
- Web search tool calls are priced separately (OpenAI’s pricing page lists $10 / 1k calls). citeturn16view0turn7search15  

ChatGPT subscription pricing (relevant because you’re currently using the UI):
- ChatGPT Plus is $20/month. citeturn17search31  
- ChatGPT Pro is $200/month, and the help center explicitly notes API usage is separate (billed independently). citeturn18view2  

**Practical takeaway:** if the bridge exists mainly to get “fast Q&A + occasional deep research,” the API will usually be both faster and operationally simpler, and you can choose models for latency vs depth rather than navigating UI toggles.

### Unofficial / reverse-engineered “ChatGPT APIs”

Projects like `revChatGPT` and forks of `transitive-bullshit/chatgpt-api` exist and explicitly market themselves as “reverse engineered” or “unofficial ChatGPT API” clients. citeturn5search13turn5search14turn5search5  
They can be useful as references for *automation patterns* (retry logic, session refresh, streaming), but they carry significant risks: breakage when the web app changes, unclear security properties (tokens/cookies), and potential ToS violations.

### MCP servers and “UI-as-an-API gateways” for ChatGPT

There are also projects that formalize UI automation:

- `chatgpt-automation-mcp` provides an MCP server that automates ChatGPT through Playwright, including model selection, send/receive, conversation management, and file upload—though it’s marked “OUT OF DATE” and was archived. citeturn14view0turn14view2  
- “UI-to-API” gateways like **CatGPT-Gateway** expose the ChatGPT web UI as an OpenAI-compatible API and advertise support for file attachments and image generation via browser automation. citeturn13view2  

These confirm there *is* precedent for building the kind of “bridge upgrade” you want—but also highlight why it stays brittle and maintenance-heavy: UI changes constantly, and serious projects need selector fallback systems, error recovery, and session restoration.

### Policy and account risk

If you are doing high-volume automation on the consumer UI, be aware: OpenAI’s own ChatGPT Pro help article explicitly prohibits “abusive usage” including “automatically or programmatically extracting data,” and prohibits “reselling access or using ChatGPT to power third-party services.” citeturn18view2  
Even if your use is internal, this is a strong signal that heavy UI-driven automation can trigger enforcement and interruptions.

## How other agent frameworks approach this problem

Most “agent frameworks” avoid “agent drives ChatGPT UI” entirely and integrate at the API layer:

- LangChain’s `ChatOpenAI` integration is an API wrapper pattern, supporting OpenAI (and Azure OpenAI) endpoints via the `langchain-openai` package. citeturn12search0turn12search20  
- AutoGPT is an agent platform built around LLM/tool loops, typically via API calls rather than controlling the ChatGPT website. citeturn12search1  
- BabyAGI implementations and explanations commonly describe it as a loop that uses OpenAI models via API plus a vector store for memory. citeturn12search2turn12search10  

When browser automation *is* needed, common patterns are:
- Use Playwright with role/text/test-id locators and auto-waiting. citeturn4search3turn5search4  
- Externalize browser execution (e.g., Browserless “Browsers as a Service”) so your agent connects to a managed browser over WebSocket, improving concurrency, stability, and infrastructure control. citeturn12search3turn12search19  

For “agent uses the web UI of another AI,” the established pattern is basically: treat it like testing a complex SPA:
- Selector fallback lists (multiple candidates per semantic element), as seen in `chrome-ai-bridge`. citeturn13view0  
- Robust response-done detection (stop button disappearance, regenerate presence), as seen in Playwright scripts. citeturn13view1  
- Session persistence via browser storage state, as described by `chatgpt-automation-mcp`. citeturn14view0  

## Improvement roadmap ranked by effort vs impact

### High impact, low-to-medium effort

The goal here is to cut your **15–30s per interaction** down to **sub-second to a few seconds** for most read/write steps, and stop paying the “full snapshot” tax.

First, use what OpenClaw already ships:
- **Implement a “micro-query loop” using `evaluate()` + `wait()`**. Use `evaluate()` to (a) set input text, (b) click send / press Enter, (c) read the latest assistant message, (d) read UI state (“generating?” “error?”). OpenClaw supports page JS execution and selector/JS predicate waits. citeturn9view0turn9view2  
- **Switch most snapshots to `--efficient` and scope them**: configure `snapshotDefaults.mode: "efficient"` and use `snapshot --selector` for the composer or message thread. citeturn2view0turn9view2  
- **Automate file uploads using OpenClaw’s upload support** (arming call), or if you move to Playwright-sidecar, use `setInputFiles()`. citeturn9view2turn3search2  

Concrete deliverables:
- A `ChatGPTDomDriver` module with:
  - `sendMessage(text)`
  - `isGenerating()`
  - `waitDone(timeout)`
  - `getLastAssistantText()`
  - `getErrorBanner()`
- Backed by selector fallbacks grounded in known automation selector sets. citeturn13view0turn13view1  

Expected impact: removes most re-snapshot cycles and avoids parsing huge DOM dumps for tiny state checks.

### Very high impact, medium effort

**Move “Deep Research” and most “Thinking” workloads to the API**:

- Use **Responses API + deep research models** (`o3-deep-research` / `o4-mini-deep-research`) rather than clicking Deep Research in ChatGPT. citeturn7search0turn16view1turn16view2  
- Run long jobs with `background=true` and either poll or use webhooks. citeturn8search1turn8search24  

This directly replaces your most painful workflow: “click correct deep research button, wait 5–15 minutes, keep snapshotting.” The API is explicitly designed for this pattern. citeturn7search15turn8search1  

Expected impact: eliminates the most fragile and time-consuming part of the UI bridge, and makes completion detection a clean state machine (`queued` → `in_progress` → `completed`).

### Medium impact, low effort

**Automate tab orchestration using the existing OpenClaw browser endpoints**

OpenClaw exposes tab operations and a local control API. citeturn9view1turn11view2  
Instead of manual 3-tab juggling, implement:
- A tab pool with a lease system (`idle`, `busy`, `cooldown`, `dead`)
- A heartbeat per tab using `evaluate()` micro-queries (e.g., “isGenerating?”)
- A recovery routine: refresh page → restore session → re-send prompt if needed

Expected impact: enables true parallelism without exponential complexity.

### High effort, high impact

If you decide UI automation must remain the core (for Custom GPT Store-only features, UI-only apps, etc.), and you want to go beyond OpenClaw’s ref-based approach:

- Build a **Playwright sidecar** (separate process) that exposes a stable RPC API to your agent:
  - selector-based click/type
  - robust locator strategy (`getByRole`, `getByTestId`)
  - event-driven response capture (MutationObserver → server events)
- Or adopt an existing foundation:
  - Playwright MCP server (generic) citeturn13view4
  - A ChatGPT-specific automation MCP/gateway as a reference (expect maintenance) citeturn14view0turn13view2  

Expected impact: less “ref churn,” but you take on ongoing maintenance as ChatGPT UI evolves.

### Metrics to track so you can prove progress

To keep the roadmap concrete, measure:
- Median and p95 time for: `send`, `waitDone`, `readLast`, `upload`
- Snapshot size (chars) and count per turn (should drop sharply)
- Failure rate per 100 turns (timeouts / element not found / wrong extraction)
- Recovery rate (how often auto-retry succeeds vs requires human intervention)
- API vs UI cost per resolved task (token cost + tool calls vs subscription + infra)

These metrics map directly to the tool capabilities and pricing you can control (e.g., using cheaper cached input tokens in the API where applicable). citeturn16view0