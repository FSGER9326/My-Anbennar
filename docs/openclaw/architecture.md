# OpenClaw Architecture

*Research agent findings — 2026-04-02*

## Gateway Model

OpenClaw is a **self-hosted AI assistant gateway**. The gateway is a single Node.js daemon that:
- Routes messages between chat channels and AI agents
- Manages agent lifecycle, session state, and tool access
- Handles cron scheduling, heartbeat, and task queuing
- Enforces authentication and channel routing rules

**Start:** `openclaw gateway start` | **Stop:** `openclaw gateway stop`

## Agent Model

Each agent is defined by:
- `SOUL.md` — identity, personality, mandate
- `AGENTS.md` — boot sequence and agent registry
- `workspace/` — agent's own working directory
- `tools/` — tool preferences and allowlists

**Agent isolation:** Agent A cannot read Agent B's context by default. Cross-agent communication uses `sessions_send`.

## Channel Routing

20+ channels supported: WhatsApp, Telegram, Discord, Slack, iMessage, Feishu, Signal, IRC, Matrix, Synology Chat, Nostr, etc. Each channel has its own plugin. Routing is per-channel-peer by default.

## Session Model

- `agent:main:main` — the primary interactive session
- `session:<name>` — named persistent sessions that maintain context across turns
- Cron sessions: `sessionTarget: "session:<name>"` for background agents
- `thread=true` requires channel plugin with `subagent_spawning` hooks (not available in this setup)

## Tool Access

| Tool | Availability |
|------|-------------|
| web_search, web_fetch | All agents |
| exec | Configurable security level |
| gateway, nodes (privileged), message | Restricted |
| cron, sessions_send, sessions_list | All agents |
| read/write/edit | All agents |

**Cron tool allowlists** (v2026.4.1+): `openclaw cron --tools` locks background jobs to specific tools only.

## Memory

- `memory/` — session transcripts and semantic memory
- `memory-search` — configurable extraPaths + hybrid search + temporal decay
- LanceDB plugin available but **disabled** in current config
- `nomic-embed-text` via Ollama for embeddings

## Cron

- Jobs persist across gateway restarts
- Runs are task-tracked
- Per-job tool allowlists available (v2026.4.1+)
- `session:research-agent` used for background research sessions

## Security

- Gateway auth via token (`gateway.auth.token`)
- Per-channel DM policies (pairing required for Telegram)
- Node pairing with deny-lists for sensitive device commands
- Tool allowlists on cron jobs prevent privilege escalation
