# Verne 10-Lane Implementation Assignments

## Current Priority
- Branch: chore/verne-10-lane-blueprint
- Focus: Lane 10 (Liliac War Legacy) — new content, no conflicts

## Lane Implementation Order
1. **Lane 10: Liliac War Legacy** (slot 10 → slot 5 for now) — entirely new
2. **Lane 6: Adventure Network** (slot 6 → slot 5 for now) — extends existing
3. **Lane 9: Industrial Foundries** (slot 9) — extends Khenak
4. **Lane 7: Vernissage** (slot 7) — extends existing Vernissage chain
5. **Lane 8: Maritime** (slot 8) — extends Regatta/fleet

## File Assignments
- **missions/Verne_Missions.txt** — lane content (sequential, one lane at a time)
- **common/scripted_triggers/** — new route triggers for each lane
- **common/scripted_effects/** — new shared effects for each lane
- **events/** — new events for each lane
- **decisions/** — new decisions for each lane
- **localisation/** — localization for all new content
- **common/event_modifiers/** — new modifiers for each lane

## Checkpoint Rules
After each lane:
1. Verify no syntax errors
2. Check localisation parity
3. Commit to branch
4. Push to GitHub
5. Move to next lane

## Merge to Main
When all 10 lanes are implemented:
1. Final review pass
2. Push to main
3. Continue with UI enablement
