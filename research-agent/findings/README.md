# Research Findings

## Files Created by Research Agent

### 2026-04-02 (Session 1)

- `clawhub-status-2026-04-02.md` — Clawhub.ai audit (empty/inactive)
- `existing-skills-audit-2026-04-02.md` — 52 npm skills + 23 workspace skills catalogued
- `github-repo-search-2026-04-02.md` — GitHub repo search results
- `openclaw-docs-structure-2026-04-02.md` — OpenClaw docs structure audit

### 2026-04-02 (Build Day)

- `openclaw-releases-2026-04-02.md` — v2026.4.1 release notes + analysis
- `openclaw-enhancement-ideas-2026-04-02.md` — Web research: improvement ideas from community

## Findings Summary

### OpenClaw v2026.4.1 (released 01 Apr 2026)
- `/tasks` chat-native task board
- `openclaw cron --tools` for per-job tool allowlists ← KEY for research agent security
- SearXNG bundled web search provider
- Configurable webchat chat history truncation
- Agent failover with rate-limit profile rotation
- Z.AI provider: glm-5.1 and glm-5v-turbo added

### Enhancement Ideas (from community research)
1. **Browser automation** — open-tabs, multi-step form fills, persistent browsing sessions
2. **Persistent memory** — vector store integration (LanceDB noted but disabled in config)
3. **Tailscale/remote gateway** — current loopback bind limits remote access
4. **Cron session persistence** — custom sessions maintain context across wakes (implemented)
5. **Multi-agent orchestration** — shared knowledge base between agents
6. **Skills marketplace** — Clawhub.ai is live but empty; opportunity to publish

### Workspace Status
- `docs/openclaw/` — created during this session
- `.learnings/` — initialized
- Cron job active: `9d41cf28-393f-475b-89c8-de1cdb8e8a79`
