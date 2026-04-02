# Existing Skills Audit — 2026-04-02

## Summary
The OpenClaw deployment has 52 npm-published skills + 23 workspace skills. Several are directly relevant to the research-agent's mission.

## Relevant Skills for Research-Agent

### Directly Applicable

| Skill | Location | Relevance |
|---|---|---|
| `self-improving-agent` | workspace/skills | Core self-improvement loop. Already installed. |
| `autonomous-skill-creator` | workspace/skills | Detects patterns and creates skills autonomously. Already installed. |
| `browser-lease-manager` | workspace/skills | Browser session management for long-running tasks |
| `browser-lease-recovery` | workspace/skills | Browser recovery patterns |
| `clawflow` | npm | Multi-step background job orchestration |
| `clawflow-inbox-triage` | npm | Example ClawFlow pattern for routing/inbox work |
| `gh-issues` | npm | GitHub issue monitoring and PR workflow |

### EU4/Modding Related (Secondary Interest)

| Skill | Relevance |
|---|---|
| `eu4-modding` | EU4 modding workflow guidance |
| `eu4-scope-rules` | EU4 trigger/effect scope rules |
| `eu4_events_decisions_missions` | EU4 event/DM patterns |
| `security-auditor` | Code security review |

## Existing Browser Skills (值得注意)

These workspace skills suggest significant prior work on browser automation:
- `browser-chat-streaming`
- `browser-completion-signals`
- `browser-lease-manager`
- `browser-lease-recovery`
- `browser-selector-contract`
- `browser-signal-registry`
- `browser-vision-fallback`

**Implication**: The deployment already has browser automation infrastructure. Research-agent should investigate these before reinventing patterns.

## Notable Gap

**No dedicated OpenClaw ecosystem monitoring skill** exists yet. The `gh-issues` skill is for GitHub issues but no skill for:
- clawhub.ai monitoring
- Discord announcement scraping
- Release note tracking
- Competitor framework research

This is an opportunity for the research-agent to create a monitoring workflow.

## Self-Improving-Agent Integration

The `self-improving-agent` skill is already installed and has:
- `.learnings/` directory structure (needs to be initialized at `~/.openclaw/workspace/.learnings/`)
- Promotion workflow to AGENTS.md, SOUL.md, TOOLS.md
- Pattern detection via simplify-and-harden feed

**Action**: Verify `.learnings/` directory exists in workspace root.
