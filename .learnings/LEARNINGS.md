# Research Agent Learnings

<!-- Auto-written by research-agent. Append only, never delete. -->

## OpenClaw Platform Findings

### 2026-04-02 — v2026.4.1 Release
- `openclaw cron --tools` added for per-job tool allowlists (exactly what the blueprint needed)
- `/tasks` chat-native background task board added
- SearXNG web search provider bundled
- Configurable webchat chat history truncation (`gateway.webchat.chatHistoryMaxChars`)
- Agent failover with rate-limit profile rotation and cooldowns
- Compaction model resolution now consistent
- Source: github.com/openclaw/openclaw/releases

### 2026-04-02 — Architecture Notes
- OpenClaw uses a gateway daemon model (message router + agent orchestration)
- Agent isolation: each agent has own workspace, SOUL.md, memory
- 20+ channel support (WhatsApp, Telegram, Discord, Slack, iMessage, Feishu, Signal, etc.)
- MIT licensed, Node.js 22+, single npm install
- Key pain point from community reviews: documentation gaps, multi-agent coordination requires manual setup

### 2026-04-02 — Comparison with AutoGPT
- OpenClaw's deterministic execution → more predictable cost than AutoGPT's autonomous approach
- AutoGPT has visual workflow builder in 2025
- AgentGPT = hosted AutoGPT in the cloud
- OpenClaw's strength: channel routing, identity system, self-hosted
- OpenClaw's weakness: multi-agent workflows need more manual coordination than alternatives

## Implementation Learnings

### 2026-04-02 — Tool Allowlists
- `openclaw cron --tools` lets us lock background jobs to specific tools only
- Allows: web_search, web_fetch, sessions_send, read, write, edit (subset)
- Prevents: exec, gateway, nodes, message (privileged tools)
- This is the security boundary for the research agent

### 2026-04-02 — Session Binding
- `session:research-agent` can be used as a cron sessionTarget for persistent context
- `sessionTarget: "isolated"` requires `payload.kind: "agentTurn"`
- `sessionTarget: "session:<custom>"` for persistent named sessions
- thread=true requires channel plugin with subagent_spawning hooks (not available in this setup)

### 2026-04-02 — Gateway Bind
- Gateway bound to loopback (127.0.0.1) — limits remote companion pairing
- To enable external access: change `gateway.bind` from "loopback" to "public" (security consideration)
- Alternative: Tailscale mode for secure remote access

## EU4 Modding Findings

### 2026-04-02 — Verne Mission Bugs
- Slots 6-10 in Verne_Missions.txt all say `slot = 5` (copy-paste error)
- `A33_project_holohana` — "Holohana" is Hawaiian, not Verne/Anbennar setting
- `A33_fifth_sloth` typo → should be `A33_fifth_slot`
- 58 missions, 80 edges, 0 orphans, 0 cycles — structure sound
- 7 terminal missions, 6 root missions
- 41/80 edges are cross-slot (intentional lane interconnections)
