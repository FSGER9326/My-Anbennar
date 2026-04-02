# SKILL.md — eu4-anbennar-autopilot

## Name
eu4-anbennar-autopilot

## Trigger phrases
- "implement a Verne mission branch"
- "add a doctrine / reform / event to Verne"
- "create a mod spec for this"
- "make a mission about X"
- "open a PR for Verne"
- "validate Verne changes"

## Description
The autonomous My-Anbennar modding pipeline skill. Converts prose requirements → schema-valid mod-spec.json → deterministic code changes → pre-PR validation. Follows the same runbook every time.

## Body

### Step 1 — Spec First
**Before writing any code**, produce a schema-valid mod spec:
1. Read `schemas/mod-spec.schema.json`
2. Read `docs/wiki/verne-canonical-vs-legacy-file-registry.md`
3. Read `docs/mod-spec.md`
4. Ask: what country tag? What feature? What files will be touched?
5. Write `automation/agent_state/current_spec.json` (valid JSON, schema-compliant)
6. Run: `python scripts/registry_expand.py --registry-md docs/wiki/verne-canonical-vs-legacy-file-registry.md --out automation/registries/verne_file_registry.json --fail-on-legacy-edit-risk`

### Step 2 — File Plan Enforcement
For each file in `filePlan[].path`:
- If `policy: "legacy-no-extend"` → **STOP**, do not edit
- If `policy: "canonical"` → edit only if mission/event ID is in spec objects
- If `policy: "shared-touchpoint"` → coordinate with owner, add to conflict_hotspots.yaml awareness

### Step 3 — Mission Truth Audit (always)
After any mission change:
```
python scripts/mission_truth_audit.py --missions missions/Verne_Missions.txt --loc localisation/verne_overhaul_l_english.yml
```
Fix all missing localisation keys before continuing.

### Step 4 — Legacy Interaction Audit
If touching `events/Flavour_Verne_A33.txt` or any legacy file:
```
python scripts/legacy_interaction_audit.py --legacy events/Flavour_Verne_A33.txt --missions missions/Verne_Missions.txt --registry automation/registries/verne_file_registry.json
```
Fix all orphan refs and zzz_* stub references.

### Step 5 — Write Code
Use Paradox script conventions:
- Tabs not spaces
- `#` for comments
- No semicolons
- `trigger = { }` not `trigger = {;}`
- Localisation keys: `{mission_id}_title`, `{mission_id}_desc`, `{modifier_id}_desc`

### Step 6 — Pre-PR Gate
```
python scripts/pre_pr_gate.sh
```
Must pass before opening PR. If it fails → fix until green.

### Step 7 — PR Draft
Run the PR draft generator (via `gh` CLI or manual artifact):
- Summary of changes
- Spec reference: link `automation/agent_state/current_spec.json`
- Validation report: link `automation/reports/`

## Files this skill touches
- `schemas/mod-spec.schema.json` (read)
- `docs/wiki/verne-canonical-vs-legacy-file-registry.md` (read)
- `docs/mod-spec.md` (read)
- `automation/agent_state/current_spec.json` (write)
- `automation/registries/verne_file_registry.json` (write)
- `automation/reports/mission_truth_report.json` (write)
- `automation/reports/legacy_interaction_report.json` (write)
- `scripts/mission_truth_audit.py` (run)
- `scripts/legacy_interaction_audit.py` (run)
- `scripts/registry_expand.py` (run)
- `scripts/pre_pr_gate.sh` (run)

## Key constraints
- **Never** edit a `legacy-no-extend` file without explicit human approval
- **Never** skip the mission truth audit after changing missions
- **Always** run pre_pr_gate.sh before PR
- Mod specs must name explicit object IDs (mission IDs, event IDs, modifier IDs, localisation keys)
