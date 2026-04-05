# Verne Architecture Review — 2026-04-05

## Focus Area
Lane 7-9 equivalent late-game reform/endgame chain, with emphasis on the faith/apostolic empire spine:

- `A33_spread_the_word`
- `A33_in_the_name_corin`
- `A33_united_under_crimson_wings`
- `A33_corins_devout_protectors`
- `A33_take_corin_as_state_deity`
- `A33_with_sword_and_shield`
- `A33_the_holy_corinite_empire`
- `A33_world_faith_emperor`
- adjacent convergence points that feed them (`A33_the_vernman_era`, `A33_a_crimson_sea`, `A33_religious_mercantilism`)

---

## Executive Summary
The most serious structural problem is that `A33_world_faith_emperor` is **severely under-gated and weakly integrated** relative to both the preceding chain and the lane design notes: after a demanding HRE-religious empire path, the capstone only asks for 50 owned Corinite provinces, 10 Corinite subjects, prestige, and an external reform hook, making the final faith payoff arrive much too cheaply for a supposed world-conquest-tier religious climax.

---

## Dependency Map

### Mission prerequisites

- `A33_spread_the_word`
  - requires `A33_corins_shield`
- `A33_in_the_name_corin`
  - requires `A33_the_lands_of_adventure`
  - requires `A33_spread_the_word`
- `A33_united_under_crimson_wings`
  - requires `A33_spread_the_word`
  - requires `A33_the_might_of_the_wyvern`
  - requires `A33_a_union_of_crowns`
- `A33_corins_devout_protectors`
  - requires `A33_united_under_crimson_wings`
  - requires `A33_in_the_name_corin`
- `A33_take_corin_as_state_deity`
  - requires `A33_corins_devout_protectors`
- `A33_with_sword_and_shield`
  - requires `A33_corins_devout_protectors`
  - requires `A33_a_crimson_sea`
- `A33_the_holy_corinite_empire`
  - requires `A33_the_vernman_era`
  - requires `A33_take_corin_as_state_deity`
- `A33_world_faith_emperor`
  - requires `A33_the_holy_corinite_empire`

### Flag / state setters and consumers

#### `verne_corinite_syncretism_flag`
- **Set by:** `A33_in_the_name_corin`
- **Consumed by:** no mission trigger in this lane found; appears to be mostly a historical/state marker rather than an active progression gate.
- **Assessment:** low integration. The syncretism mechanic matters locally, but the flag itself does not structurally feed later missions.

#### `verne_dynasty_protected`
- **Set by:** `A33_corins_devout_protectors`
- **Consumed by:** `events/verne_overhaul_crisis_events.txt` (`verne_overhaul_crisis.2`) to suppress emergency dynasty-protection activation.
- **Assessment:** good systemic integration; the mission reward meaningfully stabilizes a later crisis layer.

#### `verne_special_cb_enabled`
- **Set by:** `A33_corins_devout_protectors`
- **Consumed by:** indirectly via `verne.904` event chain fired on mission completion.
- **Assessment:** integrated, but opaque. The mission grants a major religious-war lever through an event instead of a clearly visible follow-up gate.

#### `verne_only_dotf` (global)
- **Set by:** `A33_corins_devout_protectors`
- **Consumed by:** no direct late mission trigger found in reviewed chain.
- **Assessment:** looks more like ruleset/world-state seasoning than progression logic.

#### `verne_no_imperial_rectorate` (global)
- **Set by:** `A33_corins_devout_protectors`
- **Consumed by:** no direct reviewed mission trigger found.
- **Assessment:** same issue as above; flavorful, but structurally detached from the rest of the lane.

#### `verne_corin_state_deity_chosen`
- **Set by:** `A33_take_corin_as_state_deity`
- **Consumed by:** no downstream trigger in reviewed mission chain.
- **Assessment:** surprisingly weak integration. A mission whose title implies permanent state-identity transformation does not actually gate the next faith capstone except through mission completion itself.

#### `30_trade_power_for_propogate_religion`
- **Set by:** `A33_the_holy_corinite_empire`
- **Consumed by:** Corinite order events (`events/Corinite.txt`) and Verne-specific holy-order event snippets (`events/Flavour_Verne_A33.txt`) that add extra MIL power.
- **Assessment:** decent reward integration, but the flag name is typoed (`propogate`) and reads as a technical leftover.

#### `verne_refunding_holy_order_15`
- **Set by:** `A33_the_holy_corinite_empire`
- **Consumed by:** multiple Corinite/Verne holy-order events for repeated +15 MIL injections.
- **Assessment:** mechanically integrated, but the reward pattern is a bit hidden and contributes to the lane feeling more event-buffed than mission-paced.

#### Reform hook: `verne_the_crimson_world_order_reform`
- **Required by:** `A33_world_faith_emperor`
- **Set by mission chain?:** no direct grant found in reviewed mission path.
- **Assessment:** this is an external gate, not a mission-tree gate. It is valid as a design choice, but currently under-signposted and makes the capstone feel partially detached from mission progression.

---

## Findings

### 1) `A33_world_faith_emperor` is under-gated for a capstone
**Severity:** High

#### Why it matters
After the player has already:
- locked or dominated the HRE on Corinite terms,
- converged multiple late branches into `A33_the_vernman_era`,
- completed `A33_the_holy_corinite_empire`,

…the final faith capstone only asks for:
- 50 owned Corinite provinces,
- 10 subjects,
- all subjects Corinite,
- 90 prestige,
- `verne_the_crimson_world_order_reform`.

That is far below what the title “World Faith Emperor” implies, and far below the design note in `docs/design/lanes/lane8-faith.txt`, which describes a much more world-scale gate (`3000` Corinite provinces and 10 Corinite vassals/PUs).

#### Structural consequence
The lane’s difficulty curve collapses at the end:
- `A33_the_holy_corinite_empire` is the real test.
- `A33_world_faith_emperor` then becomes cleanup rather than culmination.

#### Suggested fixes
- Raise the territorial faith requirement dramatically.
  - At minimum: total owned + subject Corinite provinces, not just owned.
  - Preferably: global Corinite footprint or a much larger threshold tied to actual world faith spread.
- Replace `num_of_subjects = 10` with a more thematic gate:
  - `calc_true_if` over Corinite subjects with minimum development,
  - or a count of Corinite great-power allies/subjects,
  - or mandate control across multiple superregions.
- Add a network/religious-economy gate using existing Verne variables:
  - `verne_world_network`
  - `verne_network_of_adventure`
- Consider requiring both `A33_with_sword_and_shield` and `A33_religious_mercantilism` or equivalent late faith/trade synthesis state, not just `A33_the_holy_corinite_empire`.

---

### 2) The final reform gate is mechanically valid but poorly integrated
**Severity:** Medium

`A33_world_faith_emperor` requires `has_reform = verne_the_crimson_world_order_reform`, but the reviewed mission chain does not itself grant, unlock, or even visibly tutor the player toward that reform.

#### Why it matters
This creates an odd structure:
- the mission chain appears to culminate naturally in `A33_world_faith_emperor`,
- but the actual blocker is partly outside the mission-tree grammar.

That is not an impossible path, but it is a **soft disconnect** between narrative progression and systemic progression.

#### Suggested fixes
- Add explicit tooltip text on `A33_the_holy_corinite_empire` or its predecessor that points to the needed reform path.
- Or gate `A33_world_faith_emperor` through an earlier Verne reform mission / event that directly upgrades into `verne_the_crimson_world_order_reform`.
- Or require a mission-granted permanent modifier instead of a government reform if the intent is strictly narrative progression.

---

### 3) Several flags are set as prestige/world-state markers but do not feed later mission logic
**Severity:** Medium

Examples:
- `verne_corinite_syncretism_flag`
- `verne_corin_state_deity_chosen`
- `verne_only_dotf`
- `verne_no_imperial_rectorate`

These do real things or imply real things, but from a mission-architecture perspective they mostly do **not** create later branching, soft locks, or alternate reward states.

#### Why it matters
This makes parts of the lane feel authored as isolated cool moments rather than as a tightly chained machine. The player gets rewards, but not many subsequent checks that say “because you chose/achieved X, the tree now evolves differently.”

#### Suggested fixes
- Let `verne_corin_state_deity_chosen` feed at least one late trigger, event option, or reward variant.
- Use `verne_corinite_syncretism_flag` to unlock a softer diplomatic/religious branch reward later, especially in overseas faith content.
- Replace one or two purely decorative globals with actual conditional reward variants in `A33_the_holy_corinite_empire` or `A33_world_faith_emperor`.

---

### 4) Reward scaling is uneven: the lane’s hardest mission has a modest permanent reward, while side systems carry more of the power
**Severity:** Medium

#### Observed reward staircase
- `A33_corins_devout_protectors`
  - strong package: dynasty protection, merc unlock, special CB, anti-Ravelian cleanup, event chain
- `A33_take_corin_as_state_deity`
  - comparatively small: permanent `verne_corins_pride`, +5 prestige
- `A33_with_sword_and_shield`
  - good permanent/temporary mix: `verne_apostles_of_corin`, oceanic command, world-network progression
- `A33_the_holy_corinite_empire`
  - permanent modifier + hidden holy-order event enhancements + possible color change
- `A33_world_faith_emperor`
  - just two permanent modifiers

#### Problem
The reward logic is not absurdly weak, but the *perceived* scaling is off:
- the middle missions feel busier and more transformative,
- the final capstone is mostly numbers.

For a named endgame identity mission, it needs a more unmistakable “I changed the campaign” reward.

#### Suggested fixes
- Add one visible world-order effect to `A33_world_faith_emperor`, e.g.:
  - automatic opinion/relation layer with Corinite nations,
  - extra missionary or clergy/holy-order system hook,
  - special diplomatic action / edict / reform discount,
  - empire-wide subject integration or liberty desire reduction for Corinite subjects.
- If keeping reward numbers-only, then at least make the trigger much steeper so the current payout feels earned.

---

### 5) Compared with vanilla/Anbennar late-mission pacing, Verne’s faith finale lands too early after its true peak
**Severity:** High

Vanilla-style end caps usually do one of two things:
1. ask for a genuinely global state change, or
2. cap a long convergence chain with one last extremely thematic obstacle.

This Verne lane already has that real obstacle in `A33_the_holy_corinite_empire`.
The next mission should escalate from empire-scale faith dominance to world-scale faith order, but instead it de-escalates into a relatively manageable subject/reform checklist.

#### Assessment
- `A33_the_holy_corinite_empire` pacing: appropriate late-game
- `A33_world_faith_emperor` pacing: too fast / too cheap

---

### 6) Some mechanics feel integrated, some feel tacked on
**Severity:** Mixed

#### Well-integrated
- `verne_dynasty_protected` interacting with crisis content
- `verne_refunding_holy_order_15` feeding holy-order events
- `A33_corins_devout_protectors` blending HRE faith authority, military order unlock, and conversion-CB logic

#### Feels tacked-on / weakly integrated
- `A33_take_corin_as_state_deity`
  - thematically huge, mechanically just a modest permanent buff and a mostly-unused flag
- `A33_world_faith_emperor`
  - depends on an external reform but does not obviously grow out of mission-state variables
- `verne_corinite_syncretism_flag`
  - flavorful local effect, but almost no architectural follow-through in the late game

---

## Circular Dependency / Impossible Path Check

### Circular dependencies
No actual circular mission dependency found in the reviewed chain.

### Impossible progression
No hard impossible path found in script logic.

### Soft-risk gates
These are not impossible, but they are structurally risky:
- `A33_world_faith_emperor` relying on `verne_the_crimson_world_order_reform` without mission-side guidance.
- `A33_corins_devout_protectors` depending on HRE religious lock / reform state can become highly campaign-variable; acceptable for a capstone-adjacent mission, but it means the lane is heavily anchored to one geopolitical outcome.
- `A33_in_the_name_corin` mixes colonial-nation requirements with a specific province (`6559`) and relation state around `H67`; workable, but brittle compared with broader region/subject logic.

---

## Lore–Mechanics Coherence Notes

### Strong coherence
- `A33_corins_devout_protectors` is the best-designed piece in the chain: it feels like Verne becoming the armed shield of Corinite order, and the mechanics support that.
- `A33_with_sword_and_shield` also lands well: military scale + African Corinite presence = a clear apostolic-imperial fantasy.

### Weak coherence
- `A33_take_corin_as_state_deity` should be a constitutional/spiritual transformation, but right now it behaves more like a small permanent buff node.
- `A33_world_faith_emperor` says “the faith of the world” while only checking a modest owned-province threshold. The title oversells the actual gate.

---

## Recommended Fix Package

### Priority 1
Rework `A33_world_faith_emperor` trigger to be truly world-scale.

Suggested direction:
- require much larger Corinite province footprint,
- count owned + subjects,
- add `verne_world_network` threshold,
- optionally require one additional late convergence mission (`A33_with_sword_and_shield` or `A33_religious_mercantilism`).

### Priority 2
Make `A33_take_corin_as_state_deity` feed later content.

Suggested direction:
- use `verne_corin_state_deity_chosen` in one downstream trigger or reward variant,
- or attach a special reform unlock / clergy-state interaction.

### Priority 3
Improve player-facing guidance for the reform gate.

Suggested direction:
- explicit tooltip on the mission or predecessor,
- or move the reform requirement into a more direct mission-driven unlock.

---

## Severity Summary
- **High:** `A33_world_faith_emperor` under-gated and too fast for its place in the tree
- **High:** late pacing collapse after `A33_the_holy_corinite_empire`
- **Medium:** reform gate is detached from mission-tree language
- **Medium:** several flags do not meaningfully feed later structure
- **Medium:** `A33_take_corin_as_state_deity` feels under-realized for its narrative weight

---

## Bottom Line
The late Verne faith branch is **not broken**, but it peaks one mission too early: `A33_the_holy_corinite_empire` feels like the real finale, while `A33_world_faith_emperor` currently reads as a lightly-gated epilogue instead of the campaign-defining religious endgame it is named to be.
