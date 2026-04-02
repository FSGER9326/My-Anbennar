# Bug Report: Recurring Config File Truncation — Separate from UI Patch Incident

**Submitted:** 2026-04-02
**Affected Version:** OpenClaw 2026.4.1 (da64a97)
**Platform:** Windows 10 (node 24.14.1, native)
**Config file:** `~/.openclaw/openclaw.json`

---

## Summary

Config files are repeatedly truncated to ~10KB, creating `openclaw.json.clobbered.*` artifacts.
This is a **separate issue** from the Control UI raw JSON patch incident also observed on the same date.

---

## Timeline

| Time | Event | Config size |
|------|-------|-------------|
| 2026-04-01 18:20:52 | First clobber | 4,433 bytes |
| 2026-04-01 19:05:58 | Second clobber | 9,482 bytes |
| 2026-04-01 19:45:37 – 22:10:50 | 24 more clobbers (gradual size increase to ~10KB) | 9,487–10,008 bytes |
| 2026-04-01 22:13:39 | Final clobber before incident | 10,052 bytes |
| 2026-04-02 00:47:37 | Last clobber (after UI patch incident) | 9,985 bytes |
| 2026-04-02 01:14:10 | Last write (after our fix patch) | 10,156 bytes |

26 `openclaw.json.clobbered.*` files observed in total.

---

## Symptoms

1. `openclaw.json` is overwritten with a truncated version (~10KB vs. ~30KB full config)
2. The truncated file retains all top-level keys but loses substantial content in `plugins` and `agents` sections
3. `openclaw.json.clobbered.<timestamp>.Z` artifacts appear alongside
4. `Config write anomaly: size-drop` warnings appear in logs
5. The gateway continues to run but with reduced plugin configuration

**IMPORTANT — Update:** Analysis of the 29 clobbered files reveals that `openclaw config set` creates clobbered backups as a standard backup behavior on every write. The 29th file (at 23:14:10) was created by our own batch patch. The `Config write anomaly: size-drop` message reflects this backup rotation, not necessarily a bug. The clobbered files may be the normal expected backup mechanism.

---

## What Was Lost in the Truncations

Comparing a full backup (29,693 bytes, `openclaw.json.bak.1`) against a clobbered file (10,052 bytes, `openclaw.json.bak.4`):

- `plugins.allow` — completely removed
- `plugins.slots` — completely removed
- `plugins.entries.<id>.enabled` states — reset to defaults
- Some `agents` sub-fields — simplified
- `lobster` plugin entry — removed

The config retains all 18 top-level keys but the values within are gutted.

---

## Known Separate Issue

On the same date, a **Control UI raw JSON editor** incident also caused config damage:
- Malformed `config.patch` calls (`raw="true"` as string instead of object) were sent from the web UI
- A subsequent patch succeeded but stripped plugin enable states and triggered a restart cascade

The clobbered files predate that UI incident (starting at 18:20 vs. 22:00 for the UI patches), indicating a **distinct root cause**.

---

## Impact

- `plugins.allow` empty → local plugins auto-load without install records
- `plugins.slots.memory` reset → memory backend ambiguity
- Plugin enable states reset → loss of configured plugin preferences
- `openclaw.json.bak.*` rotation eventually replaces the main config with truncated versions

---

## Environment Details

- OS: Windows 10.0.19045 (x64)
- Node: 24.14.1
- OpenClaw: 2026.4.1 (da64a97)
- Gateway: running as Scheduled Task service
- Config storage: `C:\Users\User\.openclaw\openclaw.json`

---

## Suggested Diagnostics to Include

- All `openclaw.json.clobbered.*` files retained for analysis
- Full config backup: `openclaw.json.bak.1` (29,693 bytes, 2026-04-02 00:40:58)
- Sample clobbered file: `openclaw.json.bak.4` (10,052 bytes, 2026-04-01 22:13:36)
- Log file: `openclaw-2026-04-01.log` (12092090 bytes) — contains config write anomalies

---

## Potential Causes (Hypotheses)

1. **Normal backup mechanism** — `openclaw.json.clobbered.*` files are likely created by `openclaw config set` as standard backups before each write. The 29th file (23:14:10) was confirmed to be from our own batch patch. The `Config write anomaly: size-drop` message reflects the size comparison against the previous backup, not a bug.

2. **Actual config truncation at 18:20** — The first clobbered file (4,433 bytes at 18:20) suggests the config was already truncated before the first clobber. The cause of that initial truncation remains unknown — separate from the backup mechanism.

3. **Gradual config erosion** — The clobbered file sizes increase from 4,433 to ~10KB over the following hours, suggesting the config was gradually rebuilt or different sections were touched at different times.

4. **Separate from UI patch incident** — The clobbered files predate the Control UI raw patch errors (18:20 vs. 22:00), confirming they are distinct issues.

---

## Asked to Investigate

- Whether `openclaw config set` or `openclaw config apply` can produce this truncation pattern
- Whether config-watch or any auto-sync mechanism writes back reduced configs
- Whether the 10KB size represents a specific default/minimal config template being written

---

## Workaround Applied

- Using `openclaw config set --batch-file` for targeted patches only
- Keeping explicit `plugins.allow` and `plugins.slots` in config at all times
- Monitoring for new clobbered files
- Preferring CLI `config set` over UI Raw JSON editor for config changes
