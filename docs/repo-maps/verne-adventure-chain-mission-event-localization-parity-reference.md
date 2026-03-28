# Verne Adventure Chain Mission/Event/Localization Parity Reference

This reference maps the Verne adventure chain naming across three layers:

1. mission IDs,
2. event IDs,
3. localization keys.

Goal: reduce break risk when editing text or wiring by keeping script names and localized names in sync.

## Quick verdict

The core chain is wired correctly and already usable. This pass does **not** rebalance bonuses or implement new effects.

What this pass establishes:

- where the adventure missions call events,
- where the counter variables are read,
- and which localization keys must remain aligned.

## Core chain map (mission -> event -> localization)

| Mission ID | Event call in mission | Event title key | Mission title key |
|---|---|---|---|
| `A33_the_vernissage` | `verne.105` | `verne.105.t` | `A33_the_vernissage_title` |
| `A33_zenith_of_the_eastern_princes` | `verne.110` | `verne.110.t` | `A33_zenith_of_the_eastern_princes_title` |
| `A33_the_halanni_exposition` | `verne.111` | `verne.111.t` | `A33_the_halanni_exposition_title` |
| `A33_the_grand_vernissage` | `verne.112` | `verne.112.t` | `A33_the_grand_vernissage_title` |
| `A33_a_most_prized_item` | `verne.114` | `verne.114.t` | `A33_a_most_prized_item_title` |
| `A33_laments_regatta` | `verne.123` | `verne.123.t` | `A33_laments_regatta_title` |
| `A33_project_holohana` | `verne.128` | `verne.128.t` | `A33_project_holohana_title` |
| `A33_the_heart_of_darkness` | `verne.1004` | `verne.1004.t` | `A33_the_heart_of_darkness_title` |

## Adventure progression variables and unlock keys

Key shared state:

- `verne_number_of_adventures_completed`
- `verne_network_of_adventure`

Key unlock/localization anchors:

- `verne_unlock_network_of_adventure`
- `verne_unlock_sarhali_adventures`
- `verne_needs_6_ports_of_adventure_tt`
- `verne_needs_11_ports_of_adventure_tt`
- `verne_needs_20_ports_of_adventure_tt`

## Practical smoke-check parity checks

Run these after touching Verne mission/event text or IDs:

1. Mission-to-event wiring
   - `rg -n "id = verne\.(105|110|111|112|114|123|128|1004)|country_event = \{ id = verne\.(105|110|111|112|114|123|128|1004) \}" missions/Verne_Missions.txt events/Flavour_Verne_A33.txt`
2. Mission title localization presence
   - `rg -n "A33_(the_vernissage|zenith_of_the_eastern_princes|the_halanni_exposition|the_grand_vernissage|a_most_prized_item|laments_regatta|project_holohana|the_heart_of_darkness)_title" localisation/Flavour_Verne_A33_l_english.yml`
3. Adventure counter/localization presence
   - `rg -n "verne_number_of_adventures_completed|verne_network_of_adventure|verne_unlock_network_of_adventure|verne_unlock_sarhali_adventures" missions/Verne_Missions.txt events/Flavour_Verne_A33.txt localisation/Flavour_Verne_A33_l_english.yml`

## Safe editing notes

- You can freely polish mission/event prose in localization without changing balance.
- Do not rename script IDs (`A33_*` mission IDs or `verne.*` event IDs) unless all three layers are migrated together.
- If a mission starts calling a new event ID, add the localization key checks in the same commit.


## Regression checks for helper refactors

When mission/event logic is moved from inline blocks into scripted helpers, run these checks before merge:

1. **Definition exists**
   - `rg -n "verne_overhaul_enable_adventure_network_tier_1|verne_overhaul_apply_regatta_spire_swap|verne_overhaul_laments_regatta_anchor_state_ready" common/scripted_effects common/scripted_triggers`
2. **Live call sites exist**
   - `rg -n "verne_overhaul_enable_adventure_network_tier_1|verne_overhaul_apply_regatta_spire_swap|verne_overhaul_laments_regatta_anchor_state_ready" missions/Verne_Missions.txt events/Flavour_Verne_A33.txt`
3. **Anchor IDs still exist**
   - `rg -n "kazakesh|kazakesh_stingport|aur_kes_akasik" common/great_projects/*.txt`
4. **No stale duplicate block remains at call sites**
   - `rg -n "destroy_great_project|add_great_project|verne_unlock_port_of_adventure_button|verne_network_of_adventure_tier_1" missions/Verne_Missions.txt events/Flavour_Verne_A33.txt || true`
   - Expectation: no matches in these two files after helper migration.

If all four checks pass, refactor risk is usually acceptable for this chain.


## Route-note: `A33_the_lands_of_adventure` gate refactor (2026-03-28)

### Intent

Keep the adventure route focused on overseas projection proof instead of forcing every run through the internal-development `A33_the_vernissage` gate.

### Prior behavior

- `A33_the_lands_of_adventure` required **both**:
  - `A33_the_vernissage`, and
  - `A33_in_search_of_adventure`.
- Result: even players already satisfying expedition-capacity route checks still had to clear the vernissage branch first.

### New behavior

- Structural mission dependency is now only `A33_in_search_of_adventure`.
- Trigger-level route gate now accepts:
  - completed `A33_the_vernissage` (legacy path preserved), **or**
  - any validated expedition-capacity route (`colonizer`, `subject/ally projection`, `network/monument`).

### Why this is safer for future edits

- Route logic is centralized in scripted trigger `verne_overhaul_lands_of_adventure_entry_route`.
- Mission wiring and localization tooltip now state route intent directly, reducing accidental re-railroading in future refactors.

