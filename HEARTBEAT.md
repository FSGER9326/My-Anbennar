# HEARTBEAT.md

## Background Worker (when idle)
1. Check `openclaw tasks list` — any running subagents?
2. If NO running tasks AND human not active → spawn background subagent
3. Read `docs/verne-roadmap.md` for current priority
4. Read `docs/background-worker.md` for task queue
5. Spawn subagent for highest priority pending task
6. If task completed: update roadmap, log trial, check for skill candidate
7. If critical finding: announce to human
8. If nothing pending or human is active: reply HEARTBEAT_OK
Note: See `docs/self-enhancement-architecture.md` for full integration
