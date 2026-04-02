# Research Agent (Archivist)

Persistent background research agent for the OpenClaw workspace.

## What It Does

- Wakes every 3 hours via cron
- Scans OpenClaw GitHub releases, Clawhub.ai, and docs for new items
- Audits the workspace for stale docs and broken references
- Reports findings to the main session via `sessions_send`
- Never touches MEMORY.md, USER.md, or bootstrap files

## Architecture

```
research-agent/
├── AGENT.md          # Identity, mandate, boundaries
├── research-cycle.md # Wake cycle instructions
├── state/
│   ├── STATE.json    # Authoritative state (dedupe, timestamps)
│   └── runlog.md     # Run history
├── findings/         # New items found per wake cycle
├── rollback/        # Snapshots before any external edits
└── memory/          # Research agent's own memory
```

## State

All state in `state/STATE.json` — no state in memory or context.
Dedupe by URL/GitHub hash to avoid re-processing items.

## Tool Allowlist

`web_search`, `web_fetch`, `sessions_send`, `read`, `write`, `edit`, `memory_search`, `memory_get`

## Cron Job

- ID: `9d41cf28-393f-475b-89c8-de1cdb8e8a79`
- Interval: every 3 hours
- Session: `session:research-agent`
- Timeout: 600s per wake

## Contact

Reports to main session (`agent:main:main`) via `sessions_send`.
