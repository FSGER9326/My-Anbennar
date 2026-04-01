# ChatGPT Browser Bridge

Use ChatGPT through the web UI (free, included in ChatGPT Plus subscription).
No API key needed. Works with any ChatGPT Plus/Team/Enterprise account.

## How It Works

1. Open ChatGPT in the openclaw browser (Falk is logged in via Google)
2. Type prompt into the chat input
3. Wait for response to generate
4. Read response from the DOM
5. Return result to the user

## Usage Pattern

When Falk asks to "ask ChatGPT" or "use GPT for this":

```
1. browser tabs (profile=openclaw) → find the ChatGPT tab
   If no ChatGPT tab, open it: browser open url=https://chatgpt.com profile=openclaw

2. browser snapshot (profile=openclaw, targetId=ChatGPT tab)
   Check if it's on a new chat page or an existing conversation

3. browser act → type into textbox "Chat with ChatGPT" (ref=e48 or similar)
   Use the ref from the snapshot for the textbox
   Press Enter to submit

4. Wait 15-30 seconds for response (longer for complex questions)

5. browser snapshot → read the response paragraph
   The response appears after "ChatGPT said:" heading

6. Extract and return the response text
```

## Mode Selection — Use the Right Tool for the Job

**Model Selector** (click "Model selector" at top of chat):
- Opens model selection menu + Configure dialog
- Shows: Instant 5.3, Thinking 5.4, Pro 5.4
- Configure dialog lets you set thinking effort level (Standard/Extended)

**Instant 5.3** — Fast, everyday chats. No DALL-E.

**Thinking 5.4** — ✅ HAS DALL-E image generation + complex reasoning.
- This is the model that generates images
- Type "Generate an image: [prompt]" and it uses DALL-E
- Set thinking effort to "Standard" for fastest image generation
- Set thinking effort to "Extended" for complex analysis + image gen

**Pro 5.4** — Research-grade text analysis. No DALL-E apparent.
- Good for deep text-only analysis and research

**Deep Research** (click "Deep research" link):
- Multi-source web research
- Takes 5-15 minutes — use for Saturday cron only

**DALL-E / Image generation**:
- MUST use Thinking 5.4 model (select via Model selector)
- Set thinking effort to "Standard" for fastest image generation
- Type "Generate an image: [prompt]" with specific style description
- Wait 30-60 seconds for generation

## Rate Limit Handling

ChatGPT shows message limits like "X messages remaining" or "Limit reached. Resets at HH:MM".

When you hit a limit:
1. Take a snapshot to find the limit message and reset time
2. Note the reset time shown in the UI
3. Stop all generation attempts
4. Wait until reset time (check every 5 min)
5. Resume generation after reset

```bash
# Example: limit resets at 00:15
# Wait 15 minutes then retry
openclaw cron add --schedule "at" --at "2026-03-31T23:15:00Z" --message "ChatGPT limit reset, resume art generation"
```

**Proactive:** Check message count before starting batch. If only 1-2 messages left, skip the batch and wait for reset.

**Limit indicators in UI:**
- "X messages remaining until XX:XX" in chat footer
- "You've reached your limit" dialog
- ChatGPT stops responding to new prompts

## Browser Tab Management — Always Reuse

**IMPORTANT:** Always start chats INSIDE the right project. No post-hoc moving needed.

```
1. Navigate to the project page: https://chatgpt.com/g/g-p-69cc42e831648191ab13873705111e51-verne-art/project
2. Type prompt in the project's "Ask anything" textbox
3. Chat stays in project automatically — no moving needed
```

Project URLs:
- **Verne Art:** `https://chatgpt.com/g/g-p-69cc42e831648191ab13873705111e51-verne-art/project`
- **Modding:** `https://chatgpt.com/g/g-p-69cb9f6f4efc819188e90b492c235334-modding/project`

To start a new chat in a project, just navigate to the project URL and type in its textbox. Done.

To check which model/mode is active:
- Take a snapshot of the banner area
- "Model selector" button shows current model
- "Extended Pro" button indicates extended thinking is ON (click to toggle)

## ⚠️ ALWAYS use profile=openclaw

**NEVER switch to Falk's private Chrome.** Every browser command must include `profile=openclaw`:
- `browser open profile=openclaw url=...`
- `browser snapshot profile=openclaw`
- `browser act profile=openclaw ...`

The openclaw browser is logged into Falk's ChatGPT account. His private Chrome should never be touched.

## Multi-Tab Parallel Generation (max 3 tabs)

Use 3 tabs to generate 3 images simultaneously:
1. Open 3 ChatGPT tabs: `browser open profile=openclaw url=https://chatgpt.com/` × 3
2. In each tab: select Thinking 5.4, type prompt, submit
3. Wait ~60s for all 3 to generate
4. Screenshot and evaluate each
5. Move all 3 chats to Verne Art project afterward

**Tab management:**
- Track tab IDs from initial `browser open` calls
- Reuse existing tabs — don't open more than 3
- After generation, close extra tabs (keep 1 main tab)

**Why 3 tabs:**
- ChatGPT concurrent limit is ~3 for free tier
- More than 3 = rate limiting risk
- 3 parallel = 3× throughput vs serial

## Project Organization (IMPORTANT — use projects!)

ChatGPT supports Projects with uploaded reference files that inform ALL chats in that project.

### Existing Projects
- **Modding** ✅ — Already exists with 5 strategy chats. Upload code reference files as Sources.

### Projects to Create (click "New project" in sidebar)
- **Verne Art** 🎨 — Upload VerneArtPack + style guides + high-scoring generated images
- **Verne Research** 🔬 — Upload wiki scrapes + game mechanics reference

### How to Create & Use
1. Click "New project" in sidebar → name it → pick icon
2. Upload files via "Sources" tab
3. Navigate to project → start new chat in project textbox

### Why this matters:
- AI reads project Sources for context (style references, existing code)
- Better prompts = better first-try results
- Art generation: uploading existing Verne icons as style reference = consistent aesthetic
- Each project has its own chat history, organized and searchable

See `docs/chatgpt-project-structure.md` for full project guide with file lists.

## Self-Improvement Protocol

After each image generation cycle, log to this file:
1. Which prompt produced high-scoring results (≥4.0)
2. Which prompt keywords consistently fail
3. Which subjects are hardest to generate well
4. Update prompt templates based on learnings

Over time, the prompt library becomes tuned for EU4/Verne aesthetic.

## When to Use Browser Bridge vs Direct AI

**Use ChatGPT (browser bridge) when:**
- **Deep Research** — multi-source web research (5-15 min). Nothing else does this. USE OFTEN.
- **Extended Thinking** — complex reasoning requiring deep logical analysis (deadlocks, circular deps, architecture)
- **Architecture validation** — before implementing major changes, have GPT-4o review for problems
- **Design research** — before adding new lanes/mechanics, research how other mods do it
- **Image generation** — DALL-E via Thinking 5.4 (only model with DALL-E)
- **Comparing approaches** — A/B analysis with web search backing
- **Long-context synthesis** — GPT-4o has a large context window, good for reviewing entire files
- **Falk specifically wants GPT-4o's opinion**
- **Accessing custom GPTs** not available via API
- **Weekly architecture reviews** — cron-scheduled deep analysis

**Use direct AI (me) when:**
- Standard tasks I can handle myself
- Tasks needing file system access (I can read/write files)
- Tasks needing exec/terminal access
- Multi-step workflows requiring tool use
- Speed matters (browser bridge adds ~15-30s overhead)
- Simple Q&A or quick reasoning

### Integration Pattern: "Research First, Then Implement"
For any significant change to the Verne mod:
1. **ChatGPT Deep Research** → gather best practices, examples, potential pitfalls
2. **ChatGPT Extended Thinking** → analyze how it fits our specific architecture
3. **Me (Jordan) implement** → write the actual code/files using what ChatGPT researched
4. **ChatGPT Validate** → have GPT-4o review the implementation for issues
5. **Me commit** → finalize

This pattern leverages ChatGPT's reasoning/research power while keeping me as the implementer with file system access.

## Limitations

- ~15-30 second response time (including browser overhead)
- Can't upload files to ChatGPT via browser (manual only)
- Conversation history doesn't persist between browser sessions (it's a new tab each time)
- Rate limits apply (ChatGPT Plus has message limits)
- Can't access ChatGPT's memory feature via automation

## File Locations
- Bridge guide: `docs/chatgpt-browser-bridge.md` (this file)
- ChatGPT tab is managed via the openclaw browser profile
