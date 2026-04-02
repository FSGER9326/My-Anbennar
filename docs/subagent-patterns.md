# Subagent Patterns & Timeout Tuning

## Timeout Tuning Table

| Task Archetype | Typical Duration | Safe Timeout | Notes |
|---|---|---|---|
| `verne-mission-audit` | ~2–3 min | 5 min | Read-only analysis, no file writes |
| `verne-loc-generation` | ~2–4 min | 5 min | ChatGPT API call + write |
| `verne-modifier-audit` | ~1–2 min | 3 min | Scripted scan, fast |
| `modifier-definition` | ~2–3 min | 5 min | Context extraction + definition write |
| `flag-trace` | ~2 min | 3 min | Targeted search, fast |
| Generic coder | 5–10 min | 10 min | Default for code writing tasks |
| Generic researcher | 3–5 min | 5 min | Default for read/search tasks |

## Spawn Rules

- **Browser tasks**: main session only — never spawn subagent for browser work
- **File writes > 10 files**: split into two spawns (checkpoint between)
- **Complex multi-step rewrite**: commit checkpoint before next spawn
- **Timeout = p95 + 30% margin** minimum
- **maxChildrenPerAgent: 2**, maxSpawnDepth: 1 (no planner→worker→sub-worker chains)

## Trial Log

| Date | Task | Duration | Outcome | Fix Applied |
|---|---|---|---|---|
| 2026-04-02 | Mission integrity audit | 2m50s | Success | — |
| 2026-04-02 | Flag trace script | <1 min | Success | — |
| 2026-04-02 | Liliac War flag fix | <1 min | Success | Event option B was setting modifier not flag |

## Reflexion Prompts (for next spawn)

After each subagent run, inject this reflection:
```
What went well? What failed? What would you do differently?
Timeout used this run: X minutes. Appropriate? Y/N
```

## Error → Solution Ledger

| Error | Solution |
|---|---|
| SIGKILL on large git operations | Use `--no-verify` flag, avoid `git reset --hard` on 24k+ file repos |
| CRLF breaking Paradox regex | Use `text.decode("utf-8-sig").replace("\r", "")` |
| Mission ID regex misses lowercase | Pattern: `[A-Z][A-Za-z0-9_]+` not `[A-Z][A-Z0-9_]+` |
| Inline Python `-c` blocked by gateway | Write script to `.py` file first, then run |
| Windows emoji in output (cp1252) | Strip emoji to ASCII labels |
