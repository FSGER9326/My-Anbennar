---
name: autonomous-skill-creator
description: Detects repeated patterns in conversation history, trial logs, and learnings files. When a pattern occurs 3+ times with high reusability score, this skill autonomously creates, installs, and logs a new skill. Use after subagent trials, after background worker cycles, or when the self-improvement-detector cron fires. Triggers on: pattern detected 3+ times, same task type scored 4+/5 repeatedly, same multi-step procedure done manually 3+ times.
---

# Autonomous Skill Creator

Monitors for patterns that indicate a new skill should be created, then creates and installs one autonomously.

## Detection Sources

Run the detector script against these sources, in order of priority:

1. **Subagent trial log** — `docs/subagent-patterns.md` → Trial Log section
2. **Learnings files** — `.learnings/LEARNINGS.md`, `.learnings/ERRORS.md`
3. **Background worker history** — `docs/background-worker.md` → completed tasks
4. **Session transcripts** — `sessions_list` + `sessions_history` for recent patterns

## Detection Script

```powershell
# Run pattern detection (returns JSON array of pattern candidates)
powershell -ExecutionPolicy Bypass -File "C:\Users\User\.openclaw\workspace\skills\autonomous-skill-creator\scripts\detect-patterns.ps1"
```

## Pattern Candidate Format

Each candidate includes:
- `pattern_key`: stable deduplication key (e.g., `qa_modifier_check`)
- `category`: `repeated_action | code_template | multi_step_procedure | error_pattern`
- `occurrences`: number of times detected (min 3)
- `reusability_score`: 1–10 (min 9 for autonomous creation)
- `files_involved`: which files/scripts contain this pattern
- `description`: what the skill should do
- `trigger_phrase`: natural language that would trigger this skill

## Skill Creation Criteria

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Same action in chat history | 3+ times | Log as candidate |
| Trial reusability score | 9+/10, 3+ occurrences | Log as candidate |
| Background worker same task | 3+ times | Log as candidate |
| Code template copied | 3+ times, >80 lines each | Log as candidate |
| Multi-step procedure | 3+ times | Log as candidate |
| **Autonomous creation** | All criteria met + score ≥9 | **Create skill now** |
| **Human review** | Score 7–8 | Suggest to human first |

## Skill Creation Workflow

### 1. Initialize Skill Directory

```powershell
$name = "qa-modifier-check"  # derived from pattern_key
$path = "C:\Users\User\.openclaw\workspace\skills\$name"
New-Item -ItemType Directory -Force -Path "$path\scripts", "$path\references"
```

### 2. Write SKILL.md

```markdown
---
name: qa-modifier-check
description: Checks all modifiers referenced in Verne mission files exist in the modifier definitions file. Use when auditing mission code for dangling modifier references. Triggers on: QA check, modifier audit, pre-commit validation.
---

# QA Modifier Check

## What It Checks
- Every modifier in `missions/Verne_Missions.txt` exists in `common/event_modifiers/verne_overhaul_modifiers.txt`
- No duplicate modifier definitions
- All modifier keys are properly namespaced (`verne_` prefix)

## How to Run

Read `missions/Verne_Missions.txt` and `common/event_modifiers/verne_overhaul_modifiers.txt`, then report any dangling references.
```

### 3. Write Helper Script (if applicable)

```powershell
# scripts/run-check.ps1
$modFile = "C:\Users\User\Documents\GitHub\My-Anbennar\common\event_modifiers\verne_overhaul_modifiers.txt"
$missionFile = "C:\Users\User\Documents\GitHub\My-Anbennar\missions\Verne_Missions.txt"
# ... validation logic
```

### 4. Install the Skill

The skill is installed simply by existing in `skills/` — OpenClaw auto-discovers skills via workspace context.

### 5. Log to Ledger

Append to `skills/self-improving-agent/ledger.md`:
```markdown
## [YYYY-MM-DD] Skill Created: qa-modifier-check
- Pattern: repeated modifier reference check (3 occurrences)
- Score: 9/10
- Trigger: QA audit subagent run
- Skill path: skills/qa-modifier-check/
```

### 6. Update Memory

Add skill description to `memory/YYYY-MM-DD.md` and `MEMORY.md` key facts section.

## Post-Creation

After creating a skill:
1. Verify the skill directory is complete (SKILL.md + any scripts)
2. Update `docs/subagent-patterns.md` with the new skill as a known pattern
3. Announce to human only if the skill changes the workflow significantly

## Files

- `scripts/detect-patterns.ps1` — main detection logic
- `references/pattern-rules.md` — scoring criteria and thresholds
