# Custom Estates Family and Privilege Framework (Base EU4 vs Anbennar)

## Quick verdict

Compared with base EU4, Anbennar estate implementation is much broader and often acts like a multi-system framework rather than a small fixed estate set.

For Verne work, the safe assumption is:

- estate behavior is distributed across `common/estates`, `common/estate_privileges`, and `events/estate_*`
- nation/race/religion-specific privilege trees can be deeply intertwined with shared systems
- you should adapt existing privilege families before creating brand-new estate frameworks

## Vanilla baseline vs Anbennar delta

### Vanilla-style baseline (simplified)

- small core estate roster
- narrower privilege libraries
- less tag/race-specific estate branching

### Anbennar delta observed in repo

- expanded custom estate roster in `common/estates` (e.g. mages, adventurers, artificers, vampires, command/caste and additional custom estates)
- large privilege library split across generic and estate-specific files in `common/estate_privileges`
- event-driven estate maintenance and interactions in many `events/estate_*` files
- custom privilege ecosystems used to drive other systems (magic, artificery, military, religion, racial content)

## Core anchors (estate definitions)

- `common/estates/97_mages.txt`
- `common/estates/98_adventurers.txt`
- `common/estates/99_artificers.txt`
- `common/estates/100_vampire.txt`
- `common/estates/101_patricians.txt`
- `common/estates/102_wolf_command.txt`
- `common/estates/103_boar_command.txt`
- `common/estates/104_lion_command.txt`
- `common/estates/105_dragon_command.txt`
- `common/estates/106_elephant_command.txt`
- `common/estates/107_tiger_command.txt`
- `common/estates/95_monstrous_tribe.txt`
- `common/estates/96_planetouched.txt`

Representative observation points in core estate files:

- `trigger = { ... }` availability gates
- `country_modifier_happy / neutral / angry`
- dynamic `influence_modifier` and `loyalty_modifier`
- large `privileges = { ... }` lists and estate-specific agendas

## Core anchors (privilege framework)

- `common/estate_privileges/anb_privileges.txt`
- `common/estate_privileges/estate_mages_privileges.txt`
- `common/estate_privileges/estate_artifice_privileges.txt`
- `common/estate_privileges/estate_vampires_privileges.txt`
- `common/estate_privileges/estate_raj_ministries_privileges.txt`
- `common/estate_privileges/estate_planetouched_privileges.txt`

Representative framework traits:

- law/organization privilege lanes
- privilege mutual exclusions and gated upgrades
- scripted effects and tooltips tied to privilege selection
- frequent cross-references to other estates and systems

## Core anchors (estate event layer)

- `events/estate_mages.txt`
- `events/estate_adventurers.txt`
- `events/estate_artificers.txt`
- `events/estate_vampires.txt`
- `events/estate_shirgrii.txt`
- `events/estate_castes_events.txt`

## Practical adaptation notes for Verne

1. Prefer extending existing estate lanes (laws, organizations, action privileges) before inventing new estate objects.
2. Reuse the privilege-gating style (mutual exclusions and upgrade ladders).
3. Treat shared privilege files as high-risk integration points during upstream updates.
4. Keep implementation notes in the change ledger for each non-trivial estate mechanic patch.

## Upstream update risk notes

High-risk zones during Anbennar updates:

- `common/estate_privileges/anb_privileges.txt`
- any large estate-specific privilege file (especially mages/artificers/vampires)
- shared estate event files used by multiple tags

When rebasing/merging upstream, revalidate:

- privilege IDs still exist
- mutual-exclusion rules still hold
- event hooks called by privileges still match current IDs
