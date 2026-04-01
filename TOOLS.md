# TOOLS.md

## Subagent Learning
- ALWAYS read `docs/subagent-patterns.md` BEFORE spawning
- NEVER spawn for browser tasks (main session only)
- ALWAYS use absolute workspace paths
- ALWAYS set runTimeoutSeconds

## ChatGPT Browser Bridge
**See `docs/chatgpt-ui-reference.md` for the complete UI reference.**
- **Models:** Instant (everyday/fast) / Thinking (o3/o4-mini reasoning) / Pro (research-grade, NO DALL-E)
- **Extended Pro** = Extended Thinking + Pro model (best reasoning, NO image gen)
- **Deep Research** = multi-step web research, 5-15 min
- **Navigation:** Use `https://chatgpt.com/` for new chats (fast). Project pages crash browser tool.
- **Input:** `div[contenteditable="true"]` NOT textarea. Wait 8s after load.
- **Deep Research download:** Playwright sidecar (`scripts/download-deep-research.js`) — don't use browser tool
- **Critical:** Project pages crash, sidebar blocks clicks, use `load` not `networkidle`
- **Projects:** Modding (Verne), Openclaw (agent), Verne Art (DALL-E)
- ALWAYS `profile=openclaw`. NEVER `profile=user`.

## CLI Quick Reference
- `openclaw memory search "query"` | `openclaw tasks list` | `openclaw cron run <id>`
- `openclaw security audit --fix` | `openclaw doctor --fix`
- `openclaw status --all` | `openclaw logs --follow` | `openclaw memory index --force`

## Modding
- Repo: `C:\Users\User\Documents\GitHub\My-Anbennar`
- Branch: `chore/verne-10-lane-blueprint`
- Lane designs: `docs/design/lanes/`

## Key Files
- `docs/chatgpt-browser-bridge.md` — full bridge guide
- `docs/chatgpt-project-structure.md` — project org
- `docs/subagent-patterns.md` — spawning guide
- `docs/verne-standards-tracker.md` — quality standards
- `docs/art-pipeline.md` — art generation pipeline
- `docs/modding-qa-protocol.md` — QA checklist
- `docs/verne-roadmap.md` — living project roadmap
- `docs/eu4-modding-reference.md` — modding reference
- `docs/eu4-wiki-scrape.md` — wiki scrape (33KB)
- `docs/eu4-game-reference.md` — game mechanics (25KB)
- `docs/inspiration-bank.md` — mod inspiration
- `.learnings/` — error/learning tracking (self-improving)

## OpenViking
- Server: `http://127.0.0.1:1933` (auto-starts with Windows)

## Obsidian Vault
- Path: `C:\Users\User\Documents\Crab Memory`
- Structure: Daily Notes, Knowledge Base, Projects, Learnings, Templates, Archive
- Use [[wikilinks]] for cross-references
- Sync daily notes and learnings to vault
- Use #jordan tag for synced content
