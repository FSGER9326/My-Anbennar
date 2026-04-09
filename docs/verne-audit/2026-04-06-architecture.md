# Verne Architecture Review — 2026-04-06

## Focus area
**Lane 1-3 (founding / early expansion) structural soundness**

Primary files reviewed:
- `missions/Verne_Missions.txt`
- `common/scripted_triggers/verne_overhaul_triggers.txt`
- `common/scripted_effects/verne_overhaul_effects.txt`
- `docs/status/verne-live-implementation-status.md`

---

## Executive summary
The early Verne spine is mostly **functionally connected** — I did not find a circular mission dependency or an outright impossible prerequisite chain in the slot graph itself — but it has one major structural bug and two clear architecture issues:

1. **`A33_pearlescent_concord` appears effectively mis-scoped / near-impossible** because it uses `all_of_countries` with `religion = corinite`, which reads like a global all-countries gate rather than an ally-set gate.
2. **Early state-formation is over-coupled to off-lane military progress**, especially through `A33_a_matter_of_pride` requiring `A33_break_the_queen_of_the_hill` from slot 5 before the lane-3 political identity branch can advance.
3. **Reward scaling is back-loaded**: the early/mid founding missions often pay in claims/modest modifiers, then `A33_the_kingdom_of_Verne` spikes very hard, making the pre-capstone stretch feel under-rewarded relative to its complexity.

---

## Mission/flag dependency map

### Slot 1 / overseas-foundation-adjacent early spine
- `A33_the_vernman_renaissance`
  - sets no key progression flags
  - grants institution/dev/general rewards
- `A33_the_grand_port_of_heartspier`
  - requires: `A33_the_riches_of_the_khenak`, `A33_the_vernman_renaissance`
  - **sets:** `verne_seed_estuary_companies`
  - **increments:** `verne_overseas_projection +1`
- `A33_the_vernissage`
  - requires: `A33_the_grand_port_of_heartspier`
  - **checks:** `verne_number_of_adventures_completed >= 3`
  - **increments:** `verne_world_network +1`

### Slot 2 / founding + early expedition spine
- `A33_alvars_reforms`
  - **triggered by hidden helper state:**
    - `verne_overhaul_has_chosen_adventurer_support`
    - `verne_overhaul_has_foreign_doctrine_support`
  - **sets / seeds:**
    - `verne_dynasty_protected`
    - `verne_defavored_adventurers` (foreign-doctrine branch)
    - `verne_seed_silver_oaths`
    - `verne_unlock_tier1_reforms`
  - **sets variable:** `verne_world_network = 1` via helper
- `A33_the_riches_of_the_khenak`
  - requires: `A33_alvars_reforms`
  - **sets / seeds:** `verne_seed_khenak_foundry`
  - **increments:** `verne_world_network +1`
- `A33_across_the_pond`
  - requires: `A33_the_grand_port_of_heartspier`
  - **checks helper:** `verne_overhaul_has_early_akasik_access_route`
  - **increments:** `verne_overseas_projection +1`
  - **sets:**
    - `verne_akasi_bulwari_adventures_unlocked`
    - `verne_unlocked_adventure_system`
    - re-seeds `verne_seed_silver_oaths`
- `A33_in_search_of_adventure`
  - requires: `A33_across_the_pond`
  - **checks helpers:**
    - `verne_overhaul_in_search_subject_projection_route`
    - `verne_overhaul_in_search_network_or_monument_route`
    - `verne_overhaul_has_expedition_capacity`
  - **increments:**
    - `verne_overseas_projection +2`
    - `verne_world_network +1`
  - **sets:**
    - `verne_unlock_port_of_adventure_button`
    - `verne_sarhali_adventures_unlocked`
    - re-seeds `verne_seed_khenak_foundry`
- `A33_the_lands_of_adventure`
  - requires: `A33_the_vernissage`, `A33_in_search_of_adventure`
  - **consumes:**
    - `verne_defavored_adventurers` (changes privilege threshold)
    - `verne_network_of_adventure >= 6`
  - **sets:** `verne_taychendi_kheionai_adventures_unlocked`

### Slot 3 / diplomatic-political early spine
- `A33_old_friends_old_rivals`
  - **seeds:** `verne_seed_silver_oaths`
- `A33_corinite_stewardship`
  - requires: `A33_old_friends_old_rivals`
  - no key progression flags set
- `A33_pearlescent_concord`
  - requires: `A33_corinite_stewardship`
  - no key progression flags set
- `A33_a_matter_of_pride`
  - requires:
    - `A33_alvars_reforms`
    - `A33_old_friends_old_rivals`
    - `A33_break_the_queen_of_the_hill` (slot 5)
- `A33_the_allure_of_the_luna`
  - requires: `A33_a_matter_of_pride`
- `A33_the_kingdom_of_Verne`
  - requires: `A33_the_allure_of_the_luna`, `A33_the_rogue_duchy`
  - **consumes flags from event path:**
    - `verne_won_support_full`
    - `verne_won_support_partial`
    - `verne_attacked`
    - `verne_backed_down`
  - **increments:** `verne_world_network +1`
  - calls scripted elector-transfer effect

---

## Findings

### 1) `A33_pearlescent_concord` has a likely broken / near-impossible global gate
**Severity: High**

Trigger excerpt of concern:
- `num_of_allies = 3`
- `all_of_countries = { limit = { not_tag = ROOT } religion = corinite }`
- `diplomatic_reputation = 3`
- `dip_power = 100`

### Why this is a problem
`all_of_countries` here does not appear scoped to allies; it reads as “all countries except ROOT are Corinite.” If that interpretation is correct, the mission is not just slow — it is structurally mis-specified for an early-lane diplomatic concord mission.

### Why this matters architecturally
This branch is placed in the early political/founding lane, so its gate should test **Verne’s alliance bloc**, not the entire world or an effectively global religion state. As written, it breaks lane identity and pacing.

### Suggested fix
Replace the global scope with an ally-scoped condition, for example one of:
- `calc_true_if` over `all_ally` with `religion = corinite`
- `num_of_allies = 3` plus `all_ally = { religion = corinite }`
- or require 3 Corinite allies explicitly if the design is meant to be stricter

### Lore-mechanics coherence
The idea is good: Verne as organizer of a Corinite diplomatic bloc. The current implementation reads less like “Pearlescent Concord” and more like “the whole setting already converted,” which is not the fantasy this mission title promises.

---

### 2) The founding/political lane is over-coupled to the military conquest lane
**Severity: Medium-High**

`A33_a_matter_of_pride` requires `A33_break_the_queen_of_the_hill` from slot 5 before the early diplomatic-political branch can proceed.

### Why this is a problem
This means early political legitimacy is not just informed by military success; it is **hard-blocked** by it. That makes the first three lanes less like three early approaches and more like one fused super-lane with mandatory militarized Khenak progress.

### Structural consequence
The player cannot cleanly pursue:
- reform/state formation,
- diplomatic positioning,
- and HRE/court identity
without first resolving a separate conquest lane node.

That compresses branch identity and weakens the “founding” theme. It also makes `A33_old_friends_old_rivals` feel less like a meaningful alternate entry vector, because its downstream payoff stalls behind a lane-5 war gate anyway.

### Suggested fixes
Best options:
1. **Soft-gate** `A33_a_matter_of_pride` with either `A33_break_the_queen_of_the_hill` **or** a diplomatic-equivalent prestige/power-projection condition.
2. Move the military prerequisite one step later, so `A33_the_allure_of_the_luna` or `A33_the_rogue_duchy` absorbs it instead.
3. Keep the current dependency but strengthen rewards on `A33_break_the_queen_of_the_hill` / `A33_a_matter_of_pride` so the mandatory detour feels like a true capstone step rather than a tax.

### Lore-mechanics coherence
Verne proving itself through force makes sense. Verne being **unable to articulate a matter of pride at all** until a specific Khenak war node is complete is less convincing.

---

### 3) `A33_alvars_reforms` is structurally opaque because both entry conditions are hidden helper bundles
**Severity: Medium**

`A33_alvars_reforms` opens from either:
- adventurer-support estate/merc setup, or
- foreign-doctrine diplomatic setup.

Mechanically valid, but both are hidden behind scripted triggers with no visible in-mission decomposition.

### Why this is a problem
For the architecture layer this is not broken, but it is fragile and readability-poor:
- the opening identity choice is important,
- yet the mission itself does not surface those subconditions in a player-readable way,
- so the mission can feel arbitrary or “why is this still red?” early on.

### Suggested fix
Add explicit custom tooltips to expose the two route packages in mission UI, or split route checks into visible nested requirements.

### Lore-mechanics coherence
The design itself is integrated: Verne can found itself through adventurer populism or imported doctrine. Good idea. It just needs clearer delivery.

---

### 4) Reward scaling is flatter than gate complexity until `A33_the_kingdom_of_Verne`
**Severity: Medium**

### Pattern observed
- `A33_alvars_reforms` has strong foundational payoff.
- `A33_the_riches_of_the_khenak` is solid and integrated.
- `A33_old_friends_old_rivals`, `A33_a_matter_of_pride`, and parts of `A33_the_allure_of_the_luna` are comparatively light for what they ask.
- `A33_the_kingdom_of_Verne` then delivers a major spike: rank-up, permanent modifier, elector-seat logic, permanent PP, monarch-point burst, legitimacy/prestige burst.

### Why this matters
The player spends several missions doing high-friction diplomacy / conquest / positioning work for rewards that often feel transitional, then gets an oversized payout all at once.

### Suggested fixes
- Add one more durable state reward in the middle stretch, especially on `A33_a_matter_of_pride` or `A33_the_allure_of_the_luna`.
- Alternatively trim `A33_the_kingdom_of_Verne` slightly if the intention is to keep the earlier missions modest.

---

## Missing gates / circular deps / impossible paths

### Circular dependency check
I did **not** find a circular dependency in the lane-1-3 graph reviewed here.

### Impossible path check
- **Likely impossible / mis-scoped:** `A33_pearlescent_concord` because of the apparent global `all_of_countries` religion gate.
- No other outright impossible path stood out in this review slice.

### Missing-gate / weak-gate notes
- `A33_the_kingdom_of_Verne` depends heavily on event-generated support flags (`verne_won_support_full`, `verne_won_support_partial`, `verne_attacked`, `verne_backed_down`) rather than a strongly mirrored mission-side narrative buildup. Mechanically legal, but the gate is more event-state-heavy than mission-state-heavy.
- Early `verne_world_network` seeding occurs from multiple founding missions (`A33_alvars_reforms`, `A33_the_riches_of_the_khenak`, later `A33_the_kingdom_of_Verne`) before the player fully experiences the overseas/network identity. This is not broken, but the abstraction arrives before the fantasy is fully legible.

---

## Pacing vs vanilla Anbennar

### Current pacing read
Verne’s lane 1-3 opening is **slower and more compound-gated** than a typical strong Anbennar major tree opening.

### Why
Compared with many vanilla/Anbennar nation openers, Verne stacks more of the following before its early political payoff lands:
- estate package setup,
- specific diplomatic relationships,
- regional conquest and coring,
- dev/building thresholds,
- expedition/network variables,
- event-flag outcomes,
- and in one case likely a mis-scoped religious bloc requirement.

### Verdict
- **Too slow in the early political branch**, especially if `A33_pearlescent_concord` is truly global-scoped.
- **Acceptably ambitious** in the overseas branch, because those gates at least reinforce Verne’s distinct identity.
- The founding branch would feel healthier if one or two gates were simplified or if mid-branch rewards were more durable.

---

## Tacked-on vs integrated mechanics

### Feels integrated
- `A33_in_search_of_adventure` -> `A33_the_lands_of_adventure`
  - strong thematic continuity
  - network variables, ports of adventure, colonial reach, and exploration capacity all point the same way
- `A33_the_riches_of_the_khenak`
  - nicely ties economy, mercs, and industrial identity together
- `A33_alvars_reforms`
  - genuinely integrated with reform/dynasty helper infrastructure

### Feels tacked-on or under-explained
- Early `verne_world_network` increments from founding-state missions
  - mechanically useful, but player-facing fantasy is not yet fully visible
- `A33_pearlescent_concord` in current form
  - structurally mismatched to its lane fantasy
- `A33_a_matter_of_pride` consuming a slot-5 conquest prerequisite
  - feels like another lane’s homework intruding into the founding branch

---

## Recommended fix order

### Priority 1
**Fix `A33_pearlescent_concord` trigger scope.**
This is the one finding that most strongly looks like a real architecture bug rather than a balance opinion.

### Priority 2
**Reduce or soften the slot-5 hard gate on `A33_a_matter_of_pride`.**
This would make lanes 1-3 feel more like lanes and less like a braided mandatory gauntlet.

### Priority 3
**Improve mid-branch reward pacing before `A33_the_kingdom_of_Verne`.**
A small permanent modifier, legitimacy/governance buff, or diplomatic-state reward would smooth the curve.

### Priority 4
**Expose hidden opening route conditions on `A33_alvars_reforms`.**
Not a mechanics fix, but a major readability/UX improvement.

---

## Bottom line
The lane 1-3 foundation is **structurally coherent enough to function**, but it is carrying one likely broken mission (`A33_pearlescent_concord`) and a broader design tendency to over-braid diplomacy, conquest, and helper-state setup too early. The best version of this branch is already visible in the overseas/adventure spine; the political/founding spine just needs the same clarity and pacing discipline.
