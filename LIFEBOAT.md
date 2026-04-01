# LIFEBOAT — Hard-capped compact state (~400 tokens max)

## Identity
- Jordan · AI assistant · warm/practical · Falk Stürmann

## Current Objective
Verne EU4 mod — 10-lane mission tree implementation

## Next 3 Actions
1. QA S02 variable tooltip fix — re-spawn verifier with tight scope
2. Spawn manifest adoption — use spawn-compiler.ps1 for all workers
3. Skill auto-creation — QA compliance 4th trial will trigger

## Blockers
- npm update -g openclaw → EPERM (needs admin)
- CLI still broken for non-version commands
- memory-lancedb unavailable (vectordb missing)

## Critical Prefs
- Absolute paths only · Paradox tabs not spaces · No semicolons
- profile=openclaw for browser · staging docs before @GitHub
- Decisions → write to daily file immediately

## Memory Keys (pull on demand)
- verne_10_lane_map → docs/design/lanes/
- qa_compliance_pattern → .learnings/ERRORS.md
- subagent_timeouts → docs/subagent-patterns.md Timeout Tuning Table
- skill_candidates → skills/self-improving-agent/ledger.md
- openviking → http://127.0.0.1:1933
