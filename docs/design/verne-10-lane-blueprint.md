# Verne 10-Lane Mission Tree Blueprint

Status: Active design document
Last updated: 2026-03-31
Source: Falk's planning session

## Overview

A 10-column, lane-based mission tree for the Verne overhaul. Each lane represents a coherent theme with early/mid/late missions. Cross-lane dependencies use flags/variables rather than `required_missions` spaghetti.

## Lane Map

| Slot | Lane | Theme |
|------|------|-------|
| 1 | Court foundation & reforms | Government reform ladder + Silver Oaths |
| 2 | Renaissance & capital modernization | Institutions + capital development |
| 3 | Luna/HRE politics & legitimacy | Imperial diplomacy + dynasty legitimacy |
| 4 | Faith & Corinite hegemony | Defender of Faith + conversion |
| 5 | Khenak industry & red brass | Foundry economy + artillery doctrine |
| 6 | Adventure network & expedition | Overseas projection via multiple routes |
| 7 | Vernissage & cultural diplomacy | Prestige + soft power |
| 8 | Maritime state, regatta, naval | Fleet + naval hegemony |
| 9 | Wyvern revival, nests, mages | Military-mage state |
| 10 | Global integration capstones | Cross-lane endgame hub |

## UI Requirements

- `max_slots_horizontal = 5` → `10`
- `slotsize.width = 104` → `88` (shrink to fit)
- Listbox width `518` → `900`
- Entry window width `530` → `920`

## Implementation Order

1. UI enablement (smoke-test slot 6)
2. Slot 6 adventure network module (first proof)
3. Lane headers (one per column)
4. Lane-by-lane migration (preserve mission IDs)
5. Cross-lane dependency reduction

## Key Files

- `missions/Verne_Missions.txt` — mission spine
- `interface/countrymissionsview.gui` — UI column control
- `common/scripted_triggers/verne_overhaul_triggers.txt` — route families
- `common/scripted_effects/verne_overhaul_effects.txt` — projection scores
- `common/government_reforms/verne_overhaul_reforms.txt` — reform gates
- `common/ideas/verne_doctrine_groups.txt` — doctrine gates

## Risk Notes

- UI overrides conflict with other mods
- Mid-save changes require `swap_non_generic_missions`
- Lane-by-lane migration preserves save compatibility
