# Verne Cross-Nation Mission Interaction Watchlist

This page tracks cases where **other nations' mission trees** directly reference Verne tag/provinces/areas.

Why this matters:

- teams often work on favorite nations in parallel,
- one mission update can accidentally change another nation's behavior,
- Verne can be affected by neighboring mission logic without touching `missions/Verne_Missions.txt`.

## Quick verdict

Cross-nation coupling exists and is normal in Anbennar, but high-coupling spots should be tracked and smoke-checked.

## Confirmed external references touching Verne context

| External mission file | Interaction type | Verne coupling anchor | Risk note |
|---|---|---|---|
| `missions/Xanzerbexis_Missions.txt` | claims + subject/ownership checks | `verne_area`, `owned_by = A33`, `A33 = { is_subject_of = ROOT ... }` | Medium/High: changes in Verne state can alter Xanzerbexis progression and vice versa. |
| `missions/Viakkoc_Missions.txt` | province-transfer exclusions | `province_id = 376` excluded in cede logic | Medium: province-level handling can create edge behavior for Stingport pathing. |
| `missions/Zokka_Missions.txt` | province-exclusion claim logic | `NOT = { province_id = 376 }` in broad claim spread | Medium: future province-role changes can invalidate assumptions. |

## Coupling categories to watch

1. **Tag coupling**
   - hard checks like `owned_by = A33`, `is_subject_of = A33`.
2. **Province coupling**
   - hard-coded province IDs (for Verne, examples include `376`, `292`, `5763`).
3. **Area/region coupling**
   - broad area claims affecting Verne land (`verne_area`, nearby areas).
4. **State coupling**
   - checks that depend on monument tiers/flags/modifiers set by Verne chains.

## Smoke-check commands (cross-nation)

Run before/after large mission edits:

Automation shortcut:

- Run `./scripts/verne_smoke_checks.sh` for the core Verne helper/index checks, then run the cross-nation grep above for coupling deltas.


1. Cross-file Verne tag/province references in non-Verne trees:
   - `rg -n "A33|owned_by = A33|is_subject_of = A33|province_id = 376|province_id = 292|province_id = 5763|verne_area" missions/*.txt -g '!missions/Verne_Missions.txt'`
2. Verne mission coupling anchors (sanity):
   - `rg -n "verne_overhaul_laments_regatta_anchor_state_ready|kazakesh|kazakesh_stingport|aur_kes_akasik" missions/Verne_Missions.txt common/scripted_triggers/verne_overhaul_triggers.txt common/great_projects/*.txt`
3. Neighbor mission lines near Verne coupling (manual review set):
   - `rg -n "verne_area|owned_by = A33|province_id = 376|is_subject_of = A33" missions/Xanzerbexis_Missions.txt missions/Viakkoc_Missions.txt missions/Zokka_Missions.txt`

## Workflow rule for future sessions

When editing Verne missions/events/helpers:

- also run the cross-nation smoke checks above,
- if hit count changes, add a short note to the PR summary,
- if logic changed intentionally, record it in `docs/wiki/anbennar-base-vs-verne-change-ledger.md`.
