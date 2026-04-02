# HOOK.md — anbennar-preflight

## Trigger
- **Event:** `command:new` — runs automatically on every `/new` session start
- **Also:** `session:start` if available

## What it does
1. Runs `python scripts/repo_doctor.py` → writes `automation/reports/preflight_doctor.txt`
2. Runs `python scripts/validate_conflict_hotspots.py` → writes `automation/reports/preflight_hotspots.txt`
3. Detects changed files against `origin/main`
4. If changed files intersect a single-writer hotspot → warns the agent in context

## Output files
- `automation/reports/preflight_doctor.txt`
- `automation/reports/preflight_hotspots.txt`

## Guards / Fail conditions
- None (preflight is informational, does not block session)
- Missing scripts are non-fatal (skip gracefully)

## Requires
- `scripts/repo_doctor.py`
- `scripts/validate_conflict_hotspots.py`
