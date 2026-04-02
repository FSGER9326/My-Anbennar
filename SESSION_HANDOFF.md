# SESSION_HANDOFF.md — 2026-04-02 01:55

## What Happened
OpenClaw gateway instability investigated and resolved. Two distinct events:

1. **18:20 (2026-04-01)** — Config first truncated to 4,433 bytes. Likely update-related (openclaw update + doctor runs at startup). NOT fully proven. 26 subsequent clobbered backups created as config eroded/rebuilt. Root cause still open.

2. **22:00 (2026-04-01)** — Control UI sent malformed `config.patch` calls (`raw="true"` string instead of object). A subsequent patch succeeded but stripped `plugins.allow`, `plugins.slots`, and disabled 3 plugins. This triggered a restart cascade: 2 active embedded runs blocked drain → 90s timeout → forced restart at 00:52.

## What Was Fixed
- `plugins.allow` restored: `["browser-lease-manager","browser-signal-registry","browser","minimax"]`
- `plugins.slots.memory` set to `"memory-core"`
- Gateway restarted cleanly at 01:25:49

## Current State
- Gateway: running healthy (node 20484, 426MB, since 01:25:49)
- HTTP 200 on port 18789
- Telegram: connected
- 9 cron jobs active
- Config stable at ~10KB (reduced from ~30KB but all critical sections present)

## Open Issues
- **First truncation at 18:20** — root cause unconfirmed. Leading hypothesis: update-time doctor/migration wrote a partial config. Monitor for recurrence.
- **memory-lancedb** — disabled but config still present. Harmless, can be cleaned up later.

## Documents
- Bug report: `docs/openclaw-bug-report-clobbered-config.md`
- Clobbered files: 29 total in `~/.openclaw/` (mostly normal backup rotation)

## Operational Rules Established
- No Raw JSON config edits during active embedded runs
- Always validate after manual config changes: `openclaw config validate`
- Use `openclaw config set --batch-file` for targeted patches
- Watch for new clobbered files with size < 9KB (recurrence indicator)
