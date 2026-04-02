# eu4-content-compiler

## Purpose
Compile a validated mod-spec.yaml into actual EU4 file changes. This is the最后一环 of the spec → files workflow.

## Input
A completed mod-spec.yaml with:
- `meta` block (mod_id, risk_tier, validated_against_upstream_sha)
- `sources` block (repo precedents, wiki references)
- `registrations` block (allocated IDs from registry)
- `content` block (what to generate)

## Output
Generated EU4 files, ready for validation.

## Workflow

### 1. Validate Spec Completeness
Before compiling, verify:
- [ ] `meta.mod_id` is set
- [ ] `meta.risk_tier` is set (low/medium/high/critical)
- [ ] `meta.validated_against_upstream_sha` is set
- [ ] `registrations` has all new IDs allocated
- [ ] `content` specifies files and changes
- [ ] Source precedent is cited for each content item

### 2. Set Up File Plan
For each item in `content`:
```
File: missions/Verne_Missions.txt
Change: ADD (new mission to slot 3)
Blast radius: medium
Precedent: lines 1200-1250 (existing slot 3 missions)
```

### 3. Generate Each File

#### Missions
- Use precedent mission as template
- Apply `content.missions[].changes` to the template
- Verify scope correctness (triggers inside `potential`, effects inside `effect`)
- Add variable tracking (flag + change_variable pairs)
- Add tooltip localization

#### Events
- Use precedent event as template
- Set namespace + ID from `registrations`
- Verify trigger scope
- Set MTTH appropriately
- Add chain links if `.2`, `.3` etc.

#### Modifiers
- Check `design/registry/modifiers.json` for existing names
- Register new modifier if needed
- Apply with `add_permanent_modifier` or `add_country_modifier`

#### Localisation
- Key format: `{loc_prefix}_{id}_title`, `{loc_prefix}_{id}_desc`
- Always UTF-8 BOM
- Add `_tt` tooltip keys for variable/tooltop content

### 4. Encoding Check
Every file write:
- [ ] Localisation → UTF-8 with BOM
- [ ] Script files → Windows-1252
- [ ] No mixed encodings

### 5. Validate Output
After generation:
1. Run CWTools on generated files
2. Run encoding scan
3. Verify all referenced IDs exist
4. Check for placeholder loc (`TODO`, `FIXME`)

## Template Variables

These are replaced during compilation:

| Variable | Replaced With |
|---|---|
| `{MOD_ID}` | `meta.mod_id` |
| `{NAMESPACE}` | `registrations.event_namespace` |
| `{LOC_PREFIX}` | `registrations.loc_prefix` |
| `{RISK_TIER}` | `meta.risk_tier` |
| `{UPSTREAM_SHA}` | `meta.validated_against_upstream_sha` |

## Example mod-spec.yaml

```yaml
meta:
  mod_id: verne_lane7_vernissage
  target_repo_mode: dev
  risk_tier: medium
  validated_against_upstream_sha: "6e2ca48ec6c78c67abd8de9878d5649a4566e0d6"

sources:
  repo_precedents:
    - path: "missions/Verne_Missions.txt"
      lines: "2000-2100"
      pattern: "slot 7 Vernissage Secretariat mission"
  wiki_precedents: []

registrations:
  event_namespace: verne_vernissage
  loc_prefix: verne_vss_

content:
  missions:
    - id: verne_vernissage_secretariat
      slot: 7
      changes:
        - type: add_mission
          after: verne_seventh_slot_previous

localisation:
  language: english
  keys_to_add:
    - key: verne_vss_secretariat_title
      value: "The Vernissage Secretariat"
```

## Common Compilation Errors

### Missing Scope Wrapper
```bash
# WRONG - effect outside scope
effect = { add_devastation = 1 }

# RIGHT
effect = {
    country_scope = {
        add_devastation = 1
    }
}
```

### Unregistered ID
```bash
# WRONG - not in registry
add_modifier = verne_unregistered_modifier

# RIGHT - register first
# After: add_modifier = verne_registered_modifier
```

### Typo in Loc Key Reference
```bash
# WRONG
name = verne_vss_scrtariat_title  # typo

# RIGHT
name = verne_vss_secretariat_title
```
