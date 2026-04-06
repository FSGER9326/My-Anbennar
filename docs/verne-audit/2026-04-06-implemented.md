# Verne implemented — 2026-04-06

## What was done
- Repaired live Verne mission localisation in `localisation/verne_overhaul_l_english.yml`.
- Added correct `A33_*` mission title/description keys for a batch of existing missions whose text had been stored under dead lowercase `a33_*_title` / `a33_*_desc` keys instead of the actual mission IDs.
- Covered live mission surfaces across faith, trade, industrial, maritime, wyvern, and prestige lanes, including:
  - `A33_pearlescent_concord`
  - `A33_world_faith_emperor`
  - `A33_establish_trade_network`
  - `A33_vernman_merchant_marine`
  - `A33_spice_route_monopoly`
  - `A33_expand_the_foundry_complex`
  - `A33_khenak_steel_program`
  - `A33_industrial_logistics_chain`
  - `A33_united_under_crimson_wings`
  - `A33_with_sword_and_shield`
- Removed duplicate desc-only entries for three lane-8 missions so the file has a single canonical loc definition for each.

## Why this matters
- EU4 mission loc expects the exact mission ID key.
- The previous lowercase `a33_*_title` entries did not satisfy live `A33_*` mission lookups, so this pass restores proper in-game mission titles and descriptions.
