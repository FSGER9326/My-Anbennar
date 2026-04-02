# Verne 10-Lane Implementation Plan

Status: Implementation planning document
Last updated: 2026-03-31
Source: Falk's planning session

## Step 1: UI Enablement

### Current State
- `interface/countrymissionsview.gui`: `max_slots_horizontal = 5`
- `slotsize = { width = 104 height = 152 }`
- Listbox: `size = { x=518 y=402 }`
- Entry window: `size = { x=530 y=500 }`

### Required Changes
1. Set `max_slots_horizontal = 10`
2. Reduce `slotsize.width` from `104` to `88`
3. Increase listbox width to `900`
4. Increase entry window width to `920`
5. Verify parent window and button placement

### Smoke Test
1. Add dummy `slot = 6` with `always = yes` trigger
2. Launch EU4, verify column 6 renders
3. Remove dummy once confirmed

## Step 2: Slot 6 Adventure Network Module

### Module Layout
```
Slot 6 (Adventure Network)
├── pos 1: A33_across_the_pond (existing, migrate)
├── pos 2: (new) A33_charter_the_expedition_fleet
├── pos 3: A33_in_search_of_adventure (existing, migrate)
├── pos 4: (new) A33_ports_of_adventure_program
├── pos 5: A33_the_lands_of_adventure (existing, migrate)
└── pos 6: (new) A33_expedition_supply_chain
```

### New Missions to Implement
1. `A33_charter_the_expedition_fleet` - Build expedition capacity
2. `A33_ports_of_adventure_program` - Scale Port of Adventure
3. `A33_expedition_supply_chain` - Logistics + upkeep

## Step 3: Lane Headers

Add non-completable headers for slots 6-10:
- `A33_sixth_slot_header` (Adventure Network)
- `A33_seventh_slot_header` (Vernissage Diplomacy)
- `A33_eighth_slot_header` (Maritime State)
- `A33_ninth_slot_header` (Wyvern State)
- `A33_tenth_slot_header` (Global Capstones)

## Step 4: Lane-by-Lane Migration

### Migration Order
1. Slot 6: Adventure Network (proven by step 2)
2. Slot 7: Vernissage & Cultural Diplomacy
3. Slot 8: Maritime State & Regatta
4. Slot 9: Wyvern Revival & Mages
5. Slot 10: Global Capstones
6. Slot 1-5: Existing content (reorganize)

### Migration Rules
- Preserve ALL mission IDs
- Change only `slot` and `position`
- Adapt `required_missions` to stay within-lane
- Keep cross-lane links to 1-3 per lane

## Step 5: Cross-Lane Dependency Reduction

### Current State
Many missions have cross-lane `required_missions` chains

### Target State
- Most dependencies within-lane
- Cross-lane only via:
  - Shared flags/variables (projection/network)
  - 1-3 explicit hub missions per late-game phase

## Testing Checklist

### Local Tests
1. Run `bash scripts/verne_smoke_checks.sh`
2. Run `bash scripts/pre_pr_gate.sh`
3. Launch EU4 and verify mission tree renders

### CI Tests
1. `.github/workflows/verne-validation.yml`
2. Event ID audit
3. Localisation audit
4. CWTools validation

## PR Checklist
- UI patch: small, isolated, no mission content
- Smoke test: temporary slot 6, verify then remove
- Headers: one PR per 2-3 lane headers
- Migration: one PR per lane module
- Dependencies: one PR for cross-lane reduction
