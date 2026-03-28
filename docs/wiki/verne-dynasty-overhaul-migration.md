# Verne Dynasty Overhaul Consolidation Migration Note

## Objective

Consolidate Verne dynasty safeguard implementation to one authoritative `verne_overhaul_*` path and retire duplicate `zz`/`zzz` implementation files that previously created split ownership across events, on_actions, triggers, and localisation.

## Ownership Migration (old -> new)

| System | Legacy owner (retired/inactive) | Authoritative owner (active) |
|---|---|---|
| Dynasty event implementation | `events/zzz_verne_overhaul_dynasty_events.txt` | `events/verne_overhaul_dynasty_events.txt` |
| Dynasty on_actions hook | `common/on_actions/zzz_verne_overhaul_dynasty_on_actions.txt` and scaffold shell in `common/on_actions/zz_verne_overhaul_on_actions.txt` | `common/on_actions/verne_overhaul_on_actions.txt` |
| Dynasty safeguard scripted triggers | `common/scripted_triggers/zzz_verne_overhaul_dynasty_triggers.txt` | `common/scripted_triggers/verne_overhaul_triggers.txt` |
| Dynasty safeguard localisation | `localisation/zzz_verne_overhaul_dynasty_l_english.yml` and scaffold duplicate in `localisation/verne_overhaul_scaffold_l_english.yml` | `localisation/verne_overhaul_dynasty_l_english.yml` |

## Behavior Change Summary

### Prior behavior (before consolidation)

- The nominal non-`zzz` event file (`events/verne_overhaul_dynasty_events.txt`) was a no-op scaffold (`always = no`) and did not execute safeguard logic.
- Live safeguard behavior existed in `zzz` files (event, on_actions, triggers, localisation), creating dual sources of truth and maintenance drift risk.
- Dynasty localisation keys existed in both scaffold and `zzz` files with conflicting text, so text ownership was ambiguous.

### New behavior (after consolidation)

- Live dynasty safeguard behavior is owned by non-`zzz` authoritative files only.
- `on_new_heir` now hooks through `common/on_actions/verne_overhaul_on_actions.txt`, which dispatches `verne_overhaul_dynasty.1`.
- `verne_overhaul_dynasty.1` now contains the active heir recovery logic in `events/verne_overhaul_dynasty_events.txt`.
- Dynasty safeguard triggers are consolidated into `common/scripted_triggers/verne_overhaul_triggers.txt`.
- Dynasty event localisation now has one owner: `localisation/verne_overhaul_dynasty_l_english.yml`.
- Legacy `zz`/`zzz` files are kept as inert retired stubs to document migration and prevent accidental reactivation.

## Canon / Design Intent Classification

- **Mechanics**: Project-canon implementation detail for Verne overhaul stability hardening.
- **Lore fit**: Inferred from existing Verne court/dynasty framing; the safeguard preserves `síl Verne` succession continuity for invalid heir states.
- **Departure from previous repo behavior**: Yes. Ownership and active logic location moved from `zzz` files to stable `verne_overhaul_*` files.

## Validation Expectations

Run the existing Verne smoke/profile checks after edits:

- `python scripts/verne_checklist_audit.py`
- `python scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json`
- optional wrapper: `bash scripts/verne_smoke_checks.sh`

