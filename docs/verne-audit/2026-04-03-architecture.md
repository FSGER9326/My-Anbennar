# Verne Architecture Review — 2026-04-03

## Focus Area
Lane 7-9 (reforms / endgame) — dependency chains and gate conditions.

## Scope Reviewed
- `missions/Verne_Missions.txt`
  - `A33_seventh_slot`
  - `A33_eighth_slot`
  - `A33_ninth_slot`
- Cross-lane prerequisites and helpers:
  - `A33_across_the_pond`
  - `A33_in_search_of_adventure`
  - `A33_the_lands_of_adventure`
  - `A33_the_riches_of_the_khenak`
  - `A33_expand_the_Vernissage`
  - `A33_the_holy_corinite_empire`
- Helper script:
  - `common/scripted_triggers/verne_overhaul_triggers.txt`
  - `common/scripted_effects/verne_overhaul_effects.txt`

---

## Executive Summary
The main structural problem in lanes 7-9 is that the industrial chain is chained to `A33_the_holy_corinite_empire`, which makes a Khenak/foundry progression depend on a very different faith-imperial endgame. That dependency is not impossible, but it badly distorts pacing and makes the industrial branch feel bolted onto the Corinite victory path instead of being its own coherent late-midgame lane.

---

## Dependency Map

### Lane 7 — Expedition / Overseas support

#### `A33_charter_the_expedition_fleet`
- Requires mission: `A33_across_the_pond`
- Trigger dependencies:
  - `verne_overhaul_has_expedition_capacity`
    - satisfied by **any** of:
      - colonizer route
      - Akasik subject/ally bridge route
      - adventure-network/monument route
  - `sailors = 3000`
  - `treasury = 200`
- Sets / advances:
  - `set_country_flag = verne_unlocked_adventure_system`
  - `verne_overseas_projection +1`
  - modifier `verne_off_to_adventure`

#### `A33_ports_of_adventure_program`
- Requires missions:
  - `A33_charter_the_expedition_fleet`
  - `A33_in_search_of_adventure`
- Trigger dependencies:
  - province `292` variable check: `verne_network_of_adventure >= 6`
- Sets / advances:
  - `verne_overseas_projection +1`
  - modifier `verne_network_of_adventure_tier_1` (temporary 3650 days)

#### `A33_expedition_supply_chain`
- Requires mission: `A33_the_lands_of_adventure`
- Trigger dependencies:
  - scripted trigger `verne_overhaul_has_adventure_network_started`
    - true if either:
      - `has_country_flag = verne_unlock_port_of_adventure_button`
      - `has_country_modifier = verne_network_of_adventure_tier_1`
  - `num_of_merchants = 5`
  - `treasury = 500`
- Sets / advances:
  - `verne_world_network +1`
  - modifier `verne_expedition_supply_chain`
  - `add_merchants = 1`

### Lane 8 — Industrial / Foundry chain

#### `A33_red_brass_forge`
- Requires mission: `A33_the_riches_of_the_khenak`
- Trigger dependencies:
  - scripted trigger `verne_overhaul_has_khenak_foundry_seeded`
    - true if `has_country_flag = verne_seed_khenak_foundry`
  - manufactories institution **or** any manufactory
  - furnace in province `838` or `292` or `291`
  - `treasury = 500`
- Sets / advances:
  - modifier `verne_red_brass_forge`
  - `+0.02` army professionalism
  - `+25 MIL`

#### `A33_controlled_devastation`
- Requires missions:
  - `A33_red_brass_forge`
  - `A33_the_holy_corinite_empire`
- Trigger dependencies:
  - scripted foundry seed state (`verne_seed_khenak_foundry`)
  - doctrine branch OR fallback:
    - `has_idea = verne_doctrine_battle_evocation`
    - `has_idea = verne_doctrine_red_court`
    - OR `has_country_flag = verne_seed_khenak_foundry` and `mil_power = 100`
  - war-state gate:
    - `is_at_war = yes`
    - OR won war vs `A30` or `A01` in last 10 years
- Sets / advances:
  - modifier `verne_controlled_devastation`
  - `add_artillery_cost = -0.10`
  - `add_yearly_manpower = 0.5`
  - costs `100 MIL`

#### `A33_expand_the_foundry_complex`
- Requires mission: `A33_controlled_devastation`
- Trigger dependencies:
  - 3 provinces in `khenak_area` with:
    - `has_building = furnace`
    - `has_building = manufactory`
  - `treasury = 3000`
  - `production_efficiency = 0.5`
- Sets / advances:
  - permanent modifier `verne_foundry_complex`
  - tooltip `verne_expand_foundry_tt`
- Notable implementation issue:
  - effect subtracts only `500` treasury, not `3000`

#### `A33_khenak_steel_program`
- Requires mission: `A33_expand_the_foundry_complex`
- Trigger dependencies:
  - `treasury = 5000`
  - `mil_power = 200`
  - `num_of_manufactories = 10`
  - at least 1 province with:
    - `development = 10`
    - `has_building = furnace`
    - `has_building = production_building`
- Sets / advances:
  - permanent modifier `verne_khenak_steel`
  - tooltip `verne_khenak_steel_tt`
  - costs `200 MIL`

### Lane 9 — Vernissage / administrative consolidation

#### `A33_vernissage_secretariat`
- Requires mission: `A33_expand_the_Vernissage`
- Trigger dependencies:
  - province `292`:
    - `development = 45`
    - `edict_advancement_effort`
  - `num_of_merchants = 4`
  - `treasury = 1500`
  - `dip_power = 100`
  - one of:
    - `has_reform = verne_vernissage_secretariat_reform`
    - `has_reform = verne_charter_of_the_vernissage_reform`
    - `verne_number_of_adventures_completed >= 8`
- Sets / advances:
  - modifier `verne_vernissage_secretariat`
  - `add_merchants = 1`
  - `verne_world_network +1`

---

## Findings

### 1) Industrial lane is over-gated by the Corinite imperial win-state
**Severity:** High

`A33_controlled_devastation` requires `A33_the_holy_corinite_empire`.

That is a massive thematic and pacing jump:
- industrial setup starts from Khenak development,
- then metallurgy/furnaces,
- then suddenly the next core step is locked behind effectively unifying or politically resolving the Corinite HRE sphere.

This is not a circular dependency, but it is a structural hard pivot. It forces a player pursuing industry to also complete one of Verne's biggest faith-imperial milestones before the foundry branch can mature.

**Why it matters**
- Makes lane 8 feel subordinate to lane 8-faith/endgame instead of parallel.
- Delays military-industrial payoff until very late compared with the effort invested in `A33_the_riches_of_the_khenak` and `A33_red_brass_forge`.
- Produces an odd player story: “I built furnaces and industrial doctrine, but cannot operationalize the foundry war-state until I solve the empire's religious destiny.”

**Suggested fix**
Replace `A33_the_holy_corinite_empire` as a hard prerequisite with one of:
- `A33_take_corin_as_state_deity`, if a faith tie is desired but not full endgame closure;
- `A33_corins_devout_protectors`, if the intent is “militarized Corinite state”; or
- no mission prerequisite at all, and keep the existing doctrine/war trigger as the real gate.

Best option: make `A33_the_holy_corinite_empire` an alternate reward amplifier rather than a prerequisite. Example: base mission always completable after `A33_red_brass_forge`, with extra modifier strength if the empire mission is done.

### 2) Lane 7 has redundant progression checks instead of escalating gates
**Severity:** Medium

`A33_ports_of_adventure_program` and `A33_the_lands_of_adventure` both hinge on essentially the same network threshold: `verne_network_of_adventure >= 6`.

This means lane 7's new middle mission does not create much new progression texture; it mostly re-reads a state already demanded by its neighboring chain.

**Why it matters**
- The lane risks feeling like a reward checkpoint, not a mission arc.
- There is weak differentiation between “network established” and “network professionalized.”

**Suggested fix**
Change one gate so the sequence escalates:
- `ports_of_adventure_program`: keep `>= 6` ports/adventures.
- `expedition_supply_chain`: require `>= 8` or `>= 10`, plus merchants/trade-company footprint.

Or let `ports_of_adventure_program` set a dedicated flag such as `verne_ports_program_established`, and have `expedition_supply_chain` require that flag plus trade thresholds.

### 3) `A33_charter_the_expedition_fleet` duplicates unlock state already granted earlier
**Severity:** Medium

It sets `verne_unlocked_adventure_system`, but `A33_across_the_pond` already sets the same flag.

**Why it matters**
- Not harmful by itself, but it suggests lane 7 is partially replaying an earlier unlock rather than extending it.
- Makes the mission feel less like a distinct structural stage.

**Suggested fix**
Let `A33_charter_the_expedition_fleet` set a new fleet-specific flag or modifier instead:
- `verne_expedition_fleet_chartered`
- or increase adventure capacity through a dedicated scripted effect

Keep `verne_unlocked_adventure_system` as the initial unlock from `A33_across_the_pond` only.

### 4) `A33_expand_the_foundry_complex` has a trigger/effect cost mismatch
**Severity:** High

Trigger demands `treasury = 3000`, but effect only does `add_treasury = -500`.

**Why it matters**
- Players pay the opportunity cost of stockpiling 3000, but the mission actually consumes far less.
- This breaks expectation-setting and makes the mission read as either unfinished or accidentally under-costed.

**Suggested fix**
If 3000 is intended, change effect to `add_treasury = -3000`.
If 500 is intended, reduce the trigger gate to 500 or 1000.

### 5) Lane 9 is structurally clean, but it is under-connected to the rest of the reform game
**Severity:** Low

`A33_vernissage_secretariat` works mechanically, but it consumes reforms rather than producing a new stateful handoff. It ends as a bonus mission, not a structural hub.

**Why it matters**
- For a mission named “Secretariat,” it does not really create an administrative machine for later content.
- It feels more like a merchant reward than a reform-capstone.

**Suggested fix**
Have it set a durable flag or enable follow-on mechanics, e.g.:
- `set_country_flag = verne_secretariat_established`
- unlock a decision/event line for diplomatic corps, colonial offices, or imperial commissions

That would make lane 9 feel integrated into Verne's state-building identity.

---

## Circular Dependency / Impossible Path Check

### No true circular dependencies found
I did not find a hard circular dependency inside lanes 7-9.

### No strictly impossible paths found
All reviewed missions appear technically completable, assuming helper systems and reforms exist as intended.

### Soft-risk / edge-case notes
- `A33_controlled_devastation` is only practical once both a late industrial state and a major faith-imperial mission are complete; this is a pacing problem rather than an impossibility.
- `A33_vernissage_secretariat` depends on reforms that may be easy to miss if the player chooses different reform paths, but the fallback `8 adventures completed` clause prevents deadlock.
- `A33_expedition_supply_chain` relies on `verne_overhaul_has_adventure_network_started`, which is currently satisfied by either a permanent helper flag (`verne_unlock_port_of_adventure_button`) or a temporary modifier (`verne_network_of_adventure_tier_1`). Because the flag is permanent, the trigger is safe, but the mixed-state design is a little messy.

---

## Reward Scaling Review

### Lane 7
- `charter_the_expedition_fleet`: modest setup reward, appropriate.
- `ports_of_adventure_program`: modest network reward, acceptable.
- `expedition_supply_chain`: +1 merchant and world-network growth, stronger and correctly later.

**Assessment:** broadly fine, but the rewards outscale the mission identity more than the trigger complexity does.

### Lane 8
- `red_brass_forge`: strong and appropriate for a midgame industrial milestone.
- `controlled_devastation`: meaningful military reward, but locked too late for its actual power level.
- `expand_the_foundry_complex` / `khenak_steel_program`: permanent modifiers and heavy economy gates fit endgame scaling.

**Assessment:** reward scaling is mostly good, but delivery is late and compressed because the chain bottlenecks on `the_holy_corinite_empire`.

### Lane 9
- `vernissage_secretariat`: +1 merchant, world-network growth, timed modifier.

**Assessment:** power is reasonable, maybe slightly conservative for a mission gated by 45 dev capital province, 1500 ducats, 4 merchants, 100 DIP, and reform/adventure completion. It reads more like a mid-late support node than a real endgame capstone.

---

## Vanilla Anbennar Pacing Comparison

Compared with a typical strong Anbennar mission lane:
- Lane 7 feels roughly on pace or slightly slower, but acceptable.
- Lane 8 feels **too slow** because it couples infrastructure progression to a major religious-imperial resolution.
- Lane 9 feels **slightly slow for its payoff**, especially because the reward is mostly merchant/trade-administration support rather than a transformational state milestone.

Overall, Verne's lane 7-9 pacing is back-loaded harder than vanilla-style mission design usually wants. The player does a lot of setup before getting structural state change.

---

## Tacked-on vs Integrated Mechanics

### Integrated well
- Khenak foundry seed system (`verne_seed_khenak_foundry`) is clean and reusable.
- Adventure-network helper triggers are sensible and modular.
- Vernissage continuing to care about merchants and completed adventures fits Verne's identity.

### Feels tacked-on
- `A33_controlled_devastation` requiring `A33_the_holy_corinite_empire`.
- `A33_charter_the_expedition_fleet` re-setting `verne_unlocked_adventure_system` after that system is already unlocked.
- `A33_vernissage_secretariat` not handing off into any further administrative or diplomatic state.

---

## Lore–Mechanics Coherence Notes

- **Expedition lane:** coherent. Fleet chartering, port networks, and supply chains all belong together.
- **Industrial lane:** coherent until the Corinite empire gate is inserted. At that point the fiction shifts from industrial militarization to civilizational religious hegemony.
- **Vernissage secretariat:** conceptually strong. A cultural-commercial institution maturing into bureaucracy is very Verne. Mechanically, though, it needs one more downstream consequence to really sell the “secretariat” idea.

---

## Recommended Fix Order

1. **Remove or soften `A33_the_holy_corinite_empire` as a prerequisite for `A33_controlled_devastation`.**
2. **Fix the treasury mismatch on `A33_expand_the_foundry_complex`.**
3. **Differentiate lane 7 progression with a dedicated handoff flag or higher late threshold.**
4. **Give `A33_vernissage_secretariat` a durable state unlock or follow-on mechanic.**

---

## Bottom Line
The lane 7-9 section is technically functional, but lane 8 in particular is structurally over-coupled to the Corinite imperial endgame, which makes Verne's industrial branch arrive too late and feel less integrated than the surrounding mission architecture deserves.
