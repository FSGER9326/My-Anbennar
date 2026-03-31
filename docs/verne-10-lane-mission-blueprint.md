# Verne 10-Lane Mission Tree Blueprint

Status: Active design document
Last updated: 2026-03-31

## Overview

This blueprint defines a 10-lane mission tree for the Verne overhaul. The design preserves existing themes while introducing underrepresented lore (e.g., the Liliac Wars). Missions are grouped into early, mid, and late game phases.

## Lane Summary

| Lane | Theme | Key Systems |
|------|-------|-------------|
| 1 | Court & Oaths | Silver Oaths doctrine, tier-1 reforms |
| 2 | Adventure Network | Merchant/adventurer networks (tiers 1–3) |
| 3 | Maritime Empire | Naval expansion, regatta, estuary companies |
| 4 | Dynastic Machine | Succession, heirs, noble privileges |
| 5 | Trade & Colonisation | Charters, colonial growth, secretariats |
| 6 | Red Court & Arcane | Magical, arcane, arcana education |
| 7 | Military Orders | Dragonwake, Wyvern marshalate, battle mages |
| 8 | Faith & Apostolic Empire | Corinite stewardship, apostolic sea lanes |
| 9 | Industrial Foundries | Khenak, red brass, artillery |
| 10 | Diplomacy & Liliac War Legacy | Diplomatic recovery, alliances, expansion |

## UI Constraints

EU4 mission tree supports ~5 columns max. Current `max_slots_horizontal = 5` in `interface/countrymissionsview.gui`. The 10-lane design requires creative UI work.

## Implementation Priority

1. Liliac War legacy (Lane 10) - entirely new, won't conflict
2. Adventure Network expansion (Lane 2) - extends existing system
3. Industrial Foundries (Lane 9) - connects existing Khenak content
4. Other lanes as existing content allows

## Detailed Lane Specifications

### Lane 1: Court & Oaths (Slot 1)
Early: A33_formalize_silver_oaths - Formalize Silver Oaths
Early: A33_open_marriage_court - Open marriage court
Mid: A33_exalted_lineages - Dynastic heir quality
Late: A33_world_court_ascension - World court reform

### Lane 2: Adventure Network (Slot 2)
Early: A33_seed_adventure_network - Start network
Mid: A33_expand_adventure_network - Expand network
Late: A33_grand_regatta_network - Grand Regatta integration

### Lane 3: Maritime Empire (Slot 3)
Early: A33_secure_port_of_heartspier - Port development
Early: A33_form_estuary_companies - Estuary companies
Mid: A33_fleet_of_the_crimson_wake - Fleet expansion
Late: A33_imperial_sea_court - Sea court reform

### Lane 4: Dynastic Machine (Slot 4)
Early: A33_enact_dynastic_safeguard - Heir protection
Mid: A33_expand_noble_privileges - Noble expansion
Late: A33_exalted_dynasty_machine - Dynasty machine

### Lane 5: Trade & Colonisation (Slot 5)
Early: A33_charter_overseas_companies - Charters
Mid: A33_distant_horizons_expansion - Colonial growth
Late: A33_overseas_commanderies - Commanderies

### Lane 6: Red Court & Arcane (Slot 6)
Early: A33_establish_red_court - Red Court foundation
Mid: A33_dragonwake_ordinance - Dragonwake reforms
Late: A33_battle_mage_collegium - Battle mage collegium

### Lane 7: Military Orders (Slot 7)
Early: A33_muster_wyvern_guard - Wyvern guard
Mid: A33_crimson_eyrie_commandery - Commandery
Late: A33_storm_crowned_hegemony - Storm crown

### Lane 8: Faith & Apostolic Empire (Slot 8)
Early: A33_corinite_stewardship - Stewardship
Mid: A33_pearlescent_concord - Concord
Late: A33_world_faith_emperor - World faith

### Lane 9: Industrial Foundries (Slot 9)
Early: A33_seed_khenak_foundry - Khenak foundation
Mid: A33_red_brass_forge - Red brass forge
Late: A33_controlled_devastation - Controlled devastation

### Lane 10: Diplomacy & Liliac War Legacy (Slot 10)
Early: A33_recount_liliac_defeat - Liliac War reflection
Mid: A33_seek_eastern_allies - Eastern diplomacy
Alt Mid: A33_avenge_liliac_wars - Liliac revenge
Late: A33_unity_through_diplomacy - Diplomatic unity
