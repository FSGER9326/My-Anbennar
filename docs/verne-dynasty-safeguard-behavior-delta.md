# Verne Dynasty Safeguard Behavior Delta (Post-Authority Unification)

Date: 2026-03-28
Status: Implemented in canonical files

## Why this delta exists

The dynasty safeguard logic previously lived in split `zzz_` files used to reduce add/add merge conflicts during branch churn.
After authority unification, the project now needs a single canonical implementation path to avoid duplicate event IDs, trigger drift, and review ambiguity.

## Canonicalization change

- Canonical on-action hook: `common/on_actions/zz_verne_overhaul_on_actions.txt`
- Canonical event chain: `events/verne_overhaul_dynasty_events.txt`
- Canonical trigger definitions: `common/scripted_triggers/verne_overhaul_triggers.txt`
- Canonical localization source for dynasty safeguard text: `localisation/verne_overhaul_scaffold_l_english.yml`

Legacy split `zzz_` dynasty files were removed in this pass.

## Behavioral delta vs previous scaffold/split state

1. **`on_new_heir` is now live in canonical on_actions**
   - Before: placeholder no-op in canonical file, active logic in split file.
   - Now: canonical file dispatches hidden safeguard event.

2. **Safeguard chain now has two stages**
   - `verne_overhaul_dynasty.1`: policy gate (when to correct).
   - `verne_overhaul_dynasty.2`: correction executor (how to correct).

3. **Correction policy now honors dynasty authority state**
   - Missing/placeholder heir: always corrected.
   - Wrong-dynasty heir + `verne_dynasty_exalted_lineage`: always corrected.
   - Wrong-dynasty heir + `verne_dynasty_protected_court`: 70% correction chance.
   - Wrong-dynasty heir with no authority modifier: 25% baseline correction chance.

4. **Marriage-court prestige rider now applied on successful correction**
   - If `verne_marriage_court_protocol` is active and legitimacy is at least 75,
     correction grants +5 prestige.

5. **Inline intent comments added in canonical script files**
   - Comments explain why each safeguard branch exists, not just what it does.

## Risk notes

- This pass intentionally centralizes authority to reduce multi-file drift risk.
- The `heir_dynasty = "síl Verne"` check is explicit by design; if project canon later allows alternate lawful cadet dynasties, update trigger policy first.
