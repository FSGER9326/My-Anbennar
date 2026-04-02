# Research Agent — Research Cycle Task

**Run this file's instructions each time you wake.**

## Phase 1: Load State

1. Read `research-agent/state/STATE.json` → note lastRun, dedupe ledger
2. Read `research-agent/state/runlog.md` → note recent runs
3. Read `research-agent/AGENT.md` → confirm identity

## Phase 2: Scan Domains (skip if dedupe says already processed)

### OpenClaw GitHub Releases
- Fetch `https://github.com/openclaw/openclaw/releases` — look for new releases since `state.domains.openclaw.lastChecked`
- For each new release: record version, date, key changes, breaking changes
- Store new findings in `research-agent/findings/openclaw-releases-YYYY-MM-DD.md`

### Clawhub.ai Skills
- Fetch `https://clawhub.ai` — look for new or updated skills since `state.domains.clawhub.lastChecked`
- Store new skills in `research-agent/findings/clawhub-skills-YYYY-MM-DD.md`

### OpenClaw Docs
- Fetch `https://docs.openclaw.ai` — note any new doc sections or changed pages
- Store findings in `research-agent/findings/openclaw-docs-YYYY-MM-DD.md`

### OpenClaw Discord (if accessible)
- Search for "OpenClaw discord invite" or known invite link
- Note: we cannot read private Discord channels without an invite

## Phase 3: Workspace Self-Audit

Check for:
- [ ] Broken links in `docs/` (reference files that don't exist)
- [ ] Missing documentation for new skills or systems
- [ ] Stale entries in `docs/status/` that should be updated
- [ ] `docs/openclaw/` — does it exist? If not, create basic structure
- [ ] `.learnings/` — does it exist? If not, initialize
- [ ] Any `slot = 5` copy-paste errors remaining in mission files (from prior audit)

## Phase 4: Update State

1. Update `research-agent/state/STATE.json`:
   - Set `lastRun` to now (ISO)
   - Add run entry to `runs[]`
   - Update dedupe ledger with newly processed URLs
   - Update `domains.*.lastChecked` timestamps
2. Append to `research-agent/state/runlog.md`

## Phase 5: Report

- If any HIGH severity items (security advisory, breaking change, data loss risk):
  - `sessions_send(sessionKey="main", message="[RESEARCHER ALERT] <brief summary of high-severity item>")`
- If new informational findings:
  - `sessions_send(sessionKey="main", message="[RESEARCHER DIGEST] <summary of new findings>")`
- If no new items:
  - `sessions_send(sessionKey="main", message="[RESEARCHER] Wake cycle complete. No new items.")`
  - Only send if this is the daily digest time (check if last digest was >20h ago)

## Phase 6: Snapshot Before Edit (safety)

Before editing ANY file outside `research-agent/`, `docs/openclaw/`, `.learnings/`:
1. Read the current file
2. Write a snapshot to `research-agent/rollback/<original-filename>-<timestamp>.bak`
3. Then proceed with edit

---

**END OF CYCLE**
