# eu4-bugfix-triage

## Purpose
Classify EU4 script failures into precise buckets so the agent can pick the right repair strategy. Wrong bucket = wrong fix.

## Failure Taxonomy

### 1. syntax_or_scope_error
**Symptoms:** CWTools red, "unexpected token", "expected trigger/effect"
**Repair:** Find the specific line, check scope keywords, validate against EU4 wiki trigger/effect reference
**Examples:** Missing `}`, wrong scope keyword, invalid operator

### 2. missing_or_bad_localisation
**Symptoms:** `Key not found` in game log, grey text in UI
**Repair:** Add/mfix `_title`, `_desc`, `_tt` keys in localisation file; verify UTF-8 BOM
**Examples:** Missing loc key, UTF-8 without BOM, typo in key name

### 3. namespace_or_id_collision
**Symptoms:** "Duplicate event ID", "modifier already defined", "decision key exists"
**Repair:** Check `design/registry/` for existing IDs; rename or confirm collision is intentional
**Examples:** Two events with same namespace.id, two modifiers with same name

### 4. country_tag_or_file_pair_break
**Symptoms:** "No country file for tag XXX", "History file missing"
**Repair:** Verify tag exists in `common/countries/`, history file in `history/countries/`
**Examples:** Added tag without creating all required files

### 5. mission_tree_softlock
**Symptoms:** Mission won't complete, no way to progress, game hangs on mission
**Repair:** Check prerequisite chain, verify all `complete` effects fire, check MTTH on hidden events
**Examples:** Missing `set_mission_flag`, circular prerequisites, impossible trigger conditions

### 6. formable_transition_bug
**Symptoms:** Formable decision doesn't fire, wrong nation appears, flag conflict
**Repair:** Check formable decision triggers, verify flag cleanup on formation
**Examples:** Formable nation has wrong color, flag not set on formation

### 7. cross_file_reference_break
**Symptoms:** "Modifier X referenced but not defined", "Event Y not found"
**Repair:** Verify all referenced IDs exist in their respective files
**Examples:** Event references modifier that doesn't exist in event_modifiers/

### 8. trade_node_or_map_dependency_break
**Symptoms:** Trade nodes broken, province ownership issues, map artifacts
**Repair:** Check trade node definitions, province mappings, terrain files
**Examples:** Trade node references non-existent province

### 9. encoding_or_unicode_contamination
**Symptoms:** Garbled text in game, missing special characters, invisible unicode
**Repair:** Run encoding scan, remove bidirectional/zero-width unicode, ensure UTF-8 BOM on loc files
**Examples:** Smart quotes from copy-paste, invisible zero-width space

### 10. performance_or_event_spam_regression
**Symptoms:** Game runs slowly, events fire too often, console spam
**Repair:** Check MTTH values, add cooldown flags, verify `once_only` on events
**Examples:** Event with MTTH 1 day, no `skip_if_any_active_effect`, no `only_once`

## Triage Workflow

1. **Collect error output** — CWTools errors, game log lines, validator output
2. **Classify** — Pick the closest bucket from above
3. **Isolate** — Find the exact file and line
4. **Repair** — Apply smallest fix for that bucket
5. **Validate** — Re-run CWTools + custom validators
6. **Record** — Log the fix type in the spec

## Classification via llm-task

For ambiguous failures, use llm-task with:
```json
{
  "failure_text": "...",
  "allowed_labels": [
    "syntax_or_scope_error",
    "missing_or_bad_localisation",
    "namespace_or_id_collision",
    "country_tag_or_file_pair_break",
    "mission_tree_softlock",
    "formable_transition_bug",
    "cross_file_reference_break",
    "trade_node_or_map_dependency_break",
    "encoding_or_unicode_contamination",
    "performance_or_event_spam_regression"
  ]
}
```

## Common Verne-Specific Patterns

| Failure | Bucket | Verne Fix |
|---|---|---|
| Missing `_tt` on variable gain | missing_or_bad_localisation | Add custom_tooltip |
| Duplicate modifier name | namespace_or_id_collision | Rename modifier |
| Mission won't complete | mission_tree_softlock | Check flag + complete effect |
| Variable tracking not showing | missing_or_bad_localisation | Check custom_tooltip loc key |
| Liliac War event not firing | mission_tree_softlock | Check flag prerequisites |
