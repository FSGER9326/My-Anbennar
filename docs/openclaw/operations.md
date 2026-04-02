# OpenClaw Operations Reference

*Research agent findings — 2026-04-02*

## Gateway Commands

```bash
openclaw gateway status       # Check if running, port, bind address
openclaw gateway start        # Start as service
openclaw gateway stop         # Stop service
openclaw gateway restart      # Restart
openclaw status               # Full diagnostics
openclaw help                 # All commands
```

## Cron Management

```bash
openclaw cron list                    # List all cron jobs
openclaw cron list --include-disabled # Include disabled jobs
openclaw cron runs <jobId>            # Get job run history
openclaw cron run <jobId>            # Trigger immediately
openclaw cron --tools <tool1,tool2>  # Per-job tool allowlist (v2026.4.1+)
```

**Cron job schema (from cron tool):**
```json
{
  "schedule": { "kind": "every" | "at" | "cron", "everyMs": 10800000 },
  "payload": { "kind": "agentTurn", "message": "...", "timeoutSeconds": 600 },
  "sessionTarget": "isolated" | "main" | "current" | "session:<name>",
  "delivery": { "mode": "announce" | "none" | "webhook" }
}
```

## Config

- **Gateway config:** `~/.openclaw/openclaw.json`
- **Workspace:** `C:\Users\User\.openclaw\workspace\`
- **Gateway port:** 18789 (loopback only in this setup)

Key config paths:
- `gateway.bind` — loopback | public | tailscale
- `gateway.tailscale.mode` — off | on | resetOnExit
- `agents.defaults.workspace` — workspace root
- `agents.defaults.memorySearch.extraPaths` — memory search paths
- `agents.defaults.subagents.maxConcurrent` — parallel subagent limit

## Skills

```bash
openclaw skills list         # List available skills
# Skills live in: ~/AppData/Roaming/npm/node_modules/openclaw/skills/
# Workspace skills: .openclaw/workspace/skills/
```

## Plugins

```bash
openclaw plugins list        # List plugins
openclaw plugins enable <name>
openclaw plugins disable <name>
```

Current active plugins: duckduckgo, browser, memory-core, minimax
Disabled: memory-lancedb (configured but disabled)

## Updating

```bash
openclaw update.run          # Update OpenClaw
# After update: gateway auto-restarts
```
