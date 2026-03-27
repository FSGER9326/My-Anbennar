# Government Mechanics Library (Base EU4 vs Anbennar)

## Quick verdict

Anbennar has a much larger government-mechanic library than vanilla expectations, with many tag/region-specific mechanic files and custom wiring through reforms and GUI.

## Core anchors

- `common/government_mechanics/*.txt`
- `common/government_mechanics/anb_*.txt`
- `common/government_reforms/*.txt`
- `interface/government_mechanics/*`

Representative Anbennar-specific mechanic files:

- `common/government_mechanics/anb_adventurer_unity.txt`
- `common/government_mechanics/anb_allclan_pandemonium.txt`
- `common/government_mechanics/anb_harpylen_queendom.txt`
- `common/government_mechanics/anb_rezankand_exemplar.txt`
- `common/government_mechanics/anb_taychend_reform.txt`

## Delta from vanilla-style baseline

- more nation- and region-specific mechanic objects
- deeper reform-to-mechanic activation paths
- heavier use of custom mechanic state in scripted/event content

## Verne adaptation note

For Verne mechanics, prefer adding minimal mechanic bars/interactions first, then wiring through reforms, then mission/event hooks.

## Upstream risk

High risk in:

- `common/government_mechanics/anb_*.txt`
- reforms that add/remove `government_abilities`


## Object-ID appendix (first pass)

Representative mechanic IDs/files to monitor:

- `anb_adventurer_unity`
- `anb_allclan_pandemonium`
- `anb_harpylen_queendom`
- `anb_rezankand_exemplar`
- `anb_taychend_reform`
