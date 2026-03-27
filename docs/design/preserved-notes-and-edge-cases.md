# Preserved Notes and Edge Cases

This file contains stray notes, edge cases, alternative variants, and partial fragments that did not fit neatly into the canonical design files but are still worth keeping.

## Preserved Side Notes

### Doctrine Group Policy Generation Rule
- The full policy matrix should be generated using role mapping: each doctrine group maps to a functional vanilla/basic role, and each role-pair gets a Verne-flavored analogue policy.
- Flavor families include:
  - court/dynasty
  - shipping/regatta
  - commandery/order
  - red court/magical discipline
  - foundry/artillery
  - Corinite imperial
  - world-court/exposition
- Policies should usually be smaller than a full idea group and often remain 2-line thematic modifiers with occasional hidden event hooks.

### Province Specialization Programs
The staged provincial-program concept is important even though it is not fully specified yet.

Model:
- mission unlocks the right to create the program
- a decision establishes the first permanent local modifier
- later missions or monuments upgrade it

Possible examples:
- Heartspier Naval Yards
- Khenak Musterfields
- Stingport Dock Quarter
- Red Court Schools
- Vernissage Exhibition Wards

### Artifact and Relic Integration
- The Vernissage, Halanni Exposition, and "A Most Prized Item" lines should interact more explicitly with artifacts and relics.
- Artifacts should function as prestige objects, exposition milestones, world-network contributors, and possible ruler/heir/court event hooks.
- Exact artifacts and specific mechanical triggers still need more design work.

### Mercantilism and Light Ships
- Verne should receive small but repeatable mercantilism gains from selected missions, decisions, and monument upgrades.
- Suggested amounts remain small, such as `add_mercantilism = 1` or `2`.
- Light ships should be supported especially in:
  - Estuary Companies
  - Grand Regatta
  - Imperial Sea Court

## Edge Cases and Implementation Warnings

### Early Missions and Idea Groups
- Do not let a mission both unlock a doctrine group and immediately check progress inside that same group.
- Early missions should use precursor flags, reforms, marriage-state logic, alliances, legitimacy, and other state checks instead of unavailable doctrine progress checks.

### Province-Scoped Logic Avoidance
- Prefer country flags, country variables, and mission completion over province-292-only pseudo-state logic.
- Exception: the Port of Adventure system already uses some province-scoped logic and should be preserved carefully rather than discarded blindly.

### Mercenary Company Manpower
- Do not try to mutate a mercenary company's manpower pool live during play.
- Prefer direct founding costs, global `mercenary_manpower` support where appropriate, and later upgraded variants.

### Corinite Center of Reformation Fallback
- If the capital cannot legally host the center, fall back to a random valid owned province.

## Variant Concepts

### Witch-King Temptation Route
- Keep this as a low-priority optional temptation route, not the mainline fantasy.
- Risky versions of Red Court or battle-mage decisions may offer stronger immediate military/magical output in exchange for greater witch-king pressure and diplomatic/social cost.

### Artificers Integration
- Staged integration concept:
  1. unlock or strengthen access to the Artificers estate and GUI
  2. mission rewards grant artificery capacity, speed research, or specific inventions
  3. tie select inventions into Verne flavor
- Suggested invention fits:
  - `commercial_sky_galleons`
  - `magic_missile_deployer`
  - `portable_turrets`
  - `sparkdrive_rifles`
  - `arcane_battery_capital_complex`

## Partial Design Fragments

### Mission Threshold Examples
- The projection-score threshold numbers are planning targets, not final balance.
- They are still worth preserving as the current planning baseline.

### Scripted Triggers and Effects
- The original source proposed a large trigger/effect catalog.
- That material is now preserved in [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md).

### Event Namespaces and Skeletons
- The original source proposed dynasty, advisor, magic, cleansing, and order-event namespaces plus first skeleton objects.
- That material is now preserved in [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md).

### Port of Adventure Modernization
- Preserve the current Port of Adventure button, province modifier, mission flavor, and event flavor where possible.
- Mirror the older province-scoped state into country-level tracking through:
  - `verne_overseas_projection`
  - `verne_world_network`
- The goal is to preserve flavor while making the wider overhaul cleaner.

### Mercenary-Order Manpower Integration
- Mercenary companies already have static `manpower_pool` values in their definitions.
- The cleaner design is not to mutate one live company repeatedly.
- Preferred approaches:
  - use country `mercenary_manpower` support broadly
  - unlock stronger order variants later
  - unlock sister companies as the Chapterhouse grows
  - apply order-specific economic or maintenance reductions
- Founding a wyvern order should still cost manpower directly in the founding decision or event layer.

## Scope Cautions

- Do not rewrite GUI unnecessarily.
- Keep the overhaul inside real EU4/Anbennar systems.
- First-wave coding should start with:
  - 7 doctrine groups
  - Tier 1-3 reforms
  - dynasty layer
  - first 10 missions

## Notes Awaiting Future Consolidation

- The full policy matrix is not yet designed beyond the first-wave set.
- The second-wave doctrine groups were fully specified in the original source and are largely already reflected in the doctrine bible.
- The repository-verified implementation anchors from the source should be consulted during coding.
- The original restructured master plan remains the deepest preservation source if a detail seems missing from the design set.

## Source Merge Note

This file keeps design fragments that are still useful but not yet fully absorbed into the canonical sections.

Important limitation:

- the first imported draft did not fully preserve every engineering-heavy section from the original source
- the missing implementation-facing material is now preserved in [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md)
