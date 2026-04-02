# Pattern Detection Rules

## Scoring

| Score | Meaning |
|-------|---------|
| 10 | Perfect reusable pattern — template, script, or skill clearly warranted |
| 9 | High reusability — definitely create skill autonomously |
| 7-8 | Medium reusability — suggest to human first |
| 5-6 | Marginal — log as candidate, don't create |
| <5 | Noise — ignore |

## Threshold Table

| Category | Occurrences | Score | Action |
|----------|-----------|-------|--------|
| repeated_action | 3+ | 9+ | Create skill autonomously |
| repeated_action | 3+ | 7-8 | Suggest to human |
| code_template | 3+ | 8+ | Create skill autonomously |
| multi_step_procedure | 3+ | 8+ | Create skill autonomously |
| error_pattern | 2+ | 9+ | Create skill autonomously |
| any | <3 | any | Log only, don't create |

## Pattern Categories

### repeated_action
Same user request or agent action appearing multiple times.
Example: "Check modifier references" appearing in 3+ subagent trials.

### code_template
Same code pattern copied across 3+ files, each >80 lines.
Example: EU4 mission structure copied with minor variable swaps.

### multi_step_procedure
Same 3+ step procedure manually executed 3+ times.
Example: QA modifier check → log result → update standards tracker.

### error_pattern
Same error occurring 2+ times with same root cause.
Example: "git commit hook failed" appearing in errors log twice.

## Verne-Specific Examples (Known Patterns)

| Pattern Key | Category | Occurrences | Score | Status |
|------------|----------|------------|-------|--------|
| qa_modifier_check | repeated_action | 3 | 4.7 | Close to threshold |
| verne_mission_flag_chain | code_template | 1 | — | Not yet |
| upstream_sync_report | multi_step_procedure | 2 | — | Not yet |
| subagent_timeout_tuning | repeated_action | 1 | — | Not yet |
