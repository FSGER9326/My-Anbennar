# Deep Research: Background Research Agent for OpenClaw

## Your Mission
Research and produce a complete implementation blueprint for a persistent, autonomous background research and self-improvement AI agent. This agent runs on the OpenClaw platform (openclaw.ai) and continuously improves its host environment by monitoring external sources and applying best-in-class agent techniques.

---

## Part 1: Understand the Platform

### What Is OpenClaw?
OpenClaw is a desktop AI agent runtime (Windows/macOS/Linux). Key capabilities:
- **Sessions**: Isolated conversational contexts with message history
- **Subagents**: Spawned child sessions for parallel or isolated tasks
- **Cron scheduling**: Jobs run on cron expressions or intervals, can wake sessions
- **Toolset**: web_search, web_fetch, browser, exec, file read/write/edit, Git, message, nodes, cron, memory, tts, image
- **Memory**: Markdown files at workspace root — MEMORY.md, memory/*.md (semantic search via memory_search)
- **Skills**: SKILL.md files define specialized tool usage instructions
- **Channels**: Webchat, Discord, Telegram, Signal — agent communicates via these

### Current Setup
- Host machine: Windows PC (DESKTOP-FOASM6G)
- Workspace: C:\Users\User\.openclaw\workspace\
- Current agent model: MiniMax M2.7-highspeed (fast), MiniMax M2.1 (cheap)
- Primary user: Falk (German, European timezone)
- Primary project: Europa Universalis IV modding (Anbennar/Verne submod)
- Secondary: OpenClaw optimization and automation

### Existing Agent Architecture
- Main session (this one): High-agency implementation partner for EU4 modding
- Subagent pattern: Short-lived spawned sessions for one-off tasks (audits, research, code gen)
- No persistent background agent yet — the goal of this research

---

## Part 2: Research Tasks

### Task 1: OpenClaw Ecosystem Research
Search and fetch:
- https://docs.openclaw.ai — full documentation index
- https://github.com/openclaw/openclaw — recent releases, commits, issues
- https://clawhub.ai — available skills, especially: memory, browser, self-improvement, automation
- OpenClaw Discord (#announcements, #showcase, #help)

**Questions to answer:**
- What features did OpenClaw ship in the last 3-6 months?
- Are there existing patterns or examples for persistent background agents?
- What skills exist that a research agent should be using?
- Any known limitations or gotchas with cron + session persistence?

### Task 2: Competitor Agent Research
Search for:
- "Hermes AI agent" — architecture, memory, tools, persistence
- "AutoGPT architecture" — self-improvement patterns
- "Claude agent tool use patterns" — best practices for web search + fetch
- "AI agent memory management patterns 2025" — how persistent agents structure memory
- "AI agent self-improvement loops" — techniques for agents that improve themselves

**Questions to answer:**
- What architectural patterns do best-in-class AI agents use for continuous background operation?
- How does Hermes handle memory persistence between sessions?
- What techniques do production agents use to avoid redundant work?
- What's the state-of-the-art for agent self-modification without breaking themselves?

### Task 3: Browser Automation Best Practices
Search for:
- "Playwright best practices long-running sessions"
- "Browser agent automation tips"
- "Playwright session management browser contexts"
- "headless browser automation stability techniques"

**Questions to answer:**
- How do you keep a browser session stable over hours of intermittent use?
- What Playwright options maximize reliability for an AI agent?
- How should the agent manage browser state between tasks?

### Task 4: Reddit & Community Research
Search:
- Reddit: r/OpenClaw, r/LocalLLaMA, r/AIAgents, r/ClaudeAI
- Search: "OpenClaw tips", "AI agent productivity system prompt", "persistent AI agent setup"

**Questions to answer:**
- What do users wish their agents could do?
- What productivity workflows are people sharing?
- Any common pain points with OpenClaw specifically?

---

## Part 3: Synthesis

Produce a comprehensive document with these sections:

### 1. Recommended Agent Architecture
- Session model: How should the agent persist? (Main + cron? Isolated + cron? Main + heartbeat?)
- Communication: How does it report to the user?
- Initialization: What does it do on first startup?
- Wake cycle: What happens on each cron wake?

### 2. Memory & Knowledge Schema
- Recommended `memory/` folder structure
- Content templates for each memory file type
- How to track "already researched" vs "needs review"
- Version/expiration strategy for findings

### 3. Cron Schedule
- Recommended intervals for each research domain (clawhub, GitHub, Discord, Reddit)
- How to balance freshness vs API usage
- What to prioritize on each wake cycle

### 4. Self-Improvement Protocol
- Which files to audit: AGENTS.md, HEARTBEAT.md, docs/, skills/, TOOLS.md
- How often to audit each
- Change validation: how to verify a change didn't break something
- Rollback procedure if something goes wrong

### 5. Complete Agent System Prompt
Write the full system prompt (the complete briefing) that the research-agent should run with. Include:
- Identity and role
- Operating constraints
- Research task list
- Reporting format
- Self-improvement mandate
- Safety rules

### 6. Safety & Rollback Protocol
- What changes require user approval before implementing?
- What can the agent change autonomously?
- How to test changes safely?
- Rollback steps if something breaks

### 7. Recommended Skills
- Which existing OpenClaw skills should it use?
- Any skills it should install from clawhub?
- Any new skills it should create for itself?

### 8. OpenClaw Limitations & Workarounds
- What OpenClaw can't do yet that this agent needs?
- Current known bugs or gotchas?
- What features should be requested for future OpenClaw versions?

### 9. Implementation Priority Order
- Phase 1: Minimum viable research agent (what to build first)
- Phase 2: Memory and self-improvement loops
- Phase 3: Advanced features (browser optimization, competitor monitoring)

### 10. Risk Assessment
- What could go wrong with a continuously-running background agent?
- How does it avoid consuming too many resources?
- How to prevent it from making unwanted changes?
- What failure modes exist and how to mitigate each?

---

## Part 4: Output Format

Return everything as a single well-structured markdown document:
- `research-agent/DEEP_RESEARCH.md` — the full synthesis
- `research-agent/AGENT_PROMPT.md` — the ready-to-use system prompt for the research agent
- `research-agent/IMPLEMENTATION_PLAN.md` — prioritized build steps

Use clear headers, code blocks for prompts/config, and bullet points for recommendations.

Cite your sources (which pages you fetched, which searches returned useful results).

---

## Constraints
- The agent cannot truly daemonize — OpenClaw isolated sessions have idle limits
- Must use only OpenClaw's native tools (web_search, web_fetch, sessions_send, cron, file tools)
- Must not modify MEMORY.md or USER.md
- Bootstrap file changes (AGENTS.md, SOUL.md, HEARTBEAT.md) require user approval
- No external API keys or services beyond OpenClaw's built-in tools

---

## Your Goal
Produce a blueprint so complete that implementing the research agent is mostly a copy-paste operation. The user will take your output and feed it to their OpenClaw agent to build the real system.