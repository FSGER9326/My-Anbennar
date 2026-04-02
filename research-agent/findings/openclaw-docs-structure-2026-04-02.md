# OpenClaw Docs Structure — 2026-04-02

## Summary
The `docs/` directory is entirely EU4/Anbennar/Verne modding focused. No OpenClaw-specific documentation exists in `docs/openclaw/`.

## Docs Directory Structure

```
docs/
├── automation/       # (not listed - check)
├── design/          # (not listed - check)
├── lore/            # (not listed - check)
├── references/      # EU4 wiki scrapes
│   └── eu4-wiki/   # ~750 files (wiki page assets)
├── repo-maps/       # 30 files — Verne/Anbennar system mapping
├── status/          # verne-live-implementation-status.md (authoritative)
├── theorycrafting/  # lorent/ and verne/ country design docs
└── wiki/            # 15 files — maintenance docs, playbooks, ledgers
```

## Missing: OpenClaw Documentation

`docs/openclaw/` does not exist. The workspace has no OpenClaw operational documentation such as:
- OpenClaw agent configuration
- Cron setup for background agents
- Skill management / installation guide
- Channel configuration (Discord, Telegram, webchat)
- Gateway/daemon management commands
- Subagent spawning patterns
- Memory structure guide

## Implications

1. **Research-agent should not look for OpenClaw docs in `docs/`** — they're simply not there.
2. **OpenClaw operational knowledge lives in**:
   - The npm package at `C:\Program Files\nodejs\node_modules\openclaw`
   - AGENTS.md / SOUL.md / TOOLS.md (workspace bootstrap files)
   - Skill SKILL.md files
3. **Creating `docs/openclaw/`** could be a valuable self-improvement contribution — documenting the actual OpenClaw setup here would help future sessions.

## Action Item

**[SUGGESTED] Create `docs/openclaw/`** with:
- `openclaw-architecture.md` — session structure, tool access, cron patterns
- `openclaw-operations.md` — gateway commands, skill management
- `openclaw-research-agent-setup.md` — this agent's design and status

Requires main session approval per research-agent mandate.
