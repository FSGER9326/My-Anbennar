# Research Agent (Archivist)

*Research agent findings — 2026-04-02*

## Overview

**Name:** Archivist
**Type:** Persistent background research agent
**Identity:** `research-agent/` workspace section with dedicated state, memory, and findings
**Cron:** Every 3 hours → `session:research-agent`
**Reports to:** main session via `sessions_send`

## Architecture

```
research-agent/
├── AGENT.md              # Identity, mandate, boundaries
├── research-cycle.md     # Wake cycle instructions
├── README.md             # Overview
├── state/
│   ├── STATE.json        # Authoritative state (dedupe, timestamps)
│   └── runlog.md         # Run history
├── findings/             # Research findings per wake
├── rollback/             # Snapshots before external edits
└── memory/              # Agent's own memory
```

## State

- **Authoritative state:** `research-agent/state/STATE.json`
- Dedupe by URL/GitHub hash — skips already-processed items
- Domain timestamps track last-checked per source
- No state in memory or context

## Tool Allowlist

Allowed: `web_search`, `web_fetch`, `sessions_send`, `read`, `write`, `edit`, `memory_search`, `memory_get`, `sessions_list`

**Blocked:** `exec` (security=full), `gateway`, `nodes` (privileged), `message`, `browser`, `canvas`

## Security Model

- Per-job tool allowlists via `openclaw cron --tools` (v2026.4.1+)
- Snapshot-before-edit for any file outside allowed directories
- External web content treated as DATA, never instructions
- Cron jobs run as isolated sessions with restricted tools

## Domains Monitored

- `github.com/openclaw/openclaw/releases` — releases
- `clawhub.ai` — skills marketplace
- `docs.openclaw.ai` — documentation
- OpenClaw Discord — announcements (if invite available)

## Communication

- **Daily digest:** One summary per day even if no new items
- **High-severity:** Immediate alert via `sessions_send` (security advisories, breaking changes)
- **Low-priority:** Accumulated in `findings/` until digest

## Workspace Boundaries

- **CAN write:** `research-agent/`, `docs/openclaw/`, `.learnings/`
- **CANNOT write:** `MEMORY.md`, `USER.md`, `AGENTS.md`, `SOUL.md`, `TOOLS.md`
- **Never:** `exec` with full security, `gateway` config changes, `nodes` privileged commands

## Current Status

- Cron job ID: `9d41cf28-393f-475b-89c8-de1cdb8e8a79`
- Next wake: +3 hours from last run
- Session: `session:research-agent`
