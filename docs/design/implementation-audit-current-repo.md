# Verne Overhaul Implementation Audit (Current Repo State)

This file audits the **actual repo implementation state** against the canonical design docs in `docs/design/`.

Goal:
- identify what is already implemented,
- identify where the repo still contains prototype / placeholder content,
- define the most practical next coding slice.

---

## Executive Summary

The repo is no longer in a "mostly prototype" state for the Verne overhaul's core systems.
A substantial systems pass has now been implemented across:
- `common/ideas/anb_country_ideas.txt`
- `common/ideas/verne_doctrine_groups.txt`
- `common/policies/verne_doctrine_policies.txt`
- `common/government_reforms/verne_overhaul_reforms.txt`
- `common/scripted_triggers/verne_overhaul_triggers.txt`
- `common/scripted_effects/verne_overhaul_effects.txt`
- `decisions/verne_overhaul_decisions.txt`
- `events/verne_overhaul_dynasty_events.txt`
- `common/on_actions/verne_overhaul_on_actions.txt`
- `missions/Verne_Missions.txt`
- `localisation/verne_overhaul_l_english.yml`

The repo is still not "finished," but the biggest reality change is:

> Verne now has a serious overhaul backbone in-repo, and future work should treat it as an expanding live system rather than a sketch.

---

## Current State by System

### 1. National ideas

**Repo status:** implemented and substantially reconciled

Files:
- `common/ideas/anb_country_ideas.txt`
- `localisation/anb_powers_and_ideas_l_english.yml`

Observed state:
- A33/Verne national ideas, traditions, and ambition have been updated toward the canonical overhaul design
- shared idea keys were preserved, avoiding unnecessary compatibility churn
- existing flavor text remained broadly compatible with the newer, stronger mechanical package

Assessment:
- this layer is no longer a major blocker
- future work here should be polishing, not structural rescue

---

### 2. Doctrine groups

**Repo status:** substantially expanded

File:
- `common/ideas/verne_doctrine_groups.txt`

Observed state:
- doctrine implementation is no longer just `verne_doctrine_silver_wake`
- the file now includes broad doctrine coverage across court, maritime, diplomatic, overseas, magical, industrial, religious, and elite-military lanes
- implemented families now include at least:
  - `verne_doctrine_silver_wake`
  - `verne_doctrine_red_court`
  - `verne_doctrine_estuary_companies`
  - `verne_doctrine_khenak_foundry`
  - `verne_doctrine_corinite_stewardship`
  - `verne_doctrine_imperial_chancery`
  - `verne_doctrine_vernissage`
  - `verne_doctrine_imperial_sea_court`
  - `verne_doctrine_grand_regatta`
  - `verne_doctrine_overseas_commandery`
  - `verne_doctrine_eastern_correspondence`
  - `verne_doctrine_apostolic_sea_lanes`
  - `verne_doctrine_pearlescent_concord`
  - `verne_doctrine_dragonwake`
  - `verne_doctrine_crimson_wake_order`
  - `verne_doctrine_battle_evocation`
  - `verne_doctrine_red_brass`
  - `verne_doctrine_sea_lance`
  - `verne_doctrine_apostolic_valour`
  - `verne_doctrine_silver_banner`

Assessment:
- doctrine implementation is now one of the strongest expansion areas on the branch
- remaining work is likely completeness/balance review rather than raw absence

---

### 3. Doctrine policies

**Repo status:** actively implemented, no longer scaffold-only

File:
- `common/policies/verne_doctrine_policies.txt`

Observed state:
- the original placeholder scaffold has been replaced
- the file now contains multiple waves of real cross-doctrine policy objects
- implemented policies include first-wave Silver Wake pairings and broader second-wave military/magical/faith/chancery pairings

Assessment:
- this layer is now genuinely real
- future work should focus on coverage review and balance tuning rather than replacing placeholders

---

### 4. Government reforms

**Repo status:** fully expanded through the canonical ladder

File:
- `common/government_reforms/verne_overhaul_reforms.txt`

Observed state:
- the reform ladder has been expanded from a Tier 1 prototype into a full Tier 1-8 Verne-exclusive ladder
- this now covers:
  - foundations of the Vernman state
  - sea-state formation
  - red-court transformation
  - court magnificence / overseas doctrine
  - wyvern military state
  - maritime hegemony
  - faith empire / world court
  - final synthesis

Assessment:
- the reform file is now one of the clearest examples of major systemic overhaul progress
- likely next work is balance and mission/reward integration, not missing content

---

### 5. Scripted triggers

**Repo status:** useful and materially expanded

File:
- `common/scripted_triggers/verne_overhaul_triggers.txt`

Observed state:
- continues to contain dynasty safeguard triggers
- now also contains more reusable first-wave and path-state checks
- supports the new early-state and helper-flag model much better than before

Assessment:
- still a support layer rather than a marquee feature, but no longer notably underbuilt relative to the first-wave mission work

---

### 6. Scripted effects

**Repo status:** meaningfully expanded

File:
- `common/scripted_effects/verne_overhaul_effects.txt`

Observed state:
- now includes reusable first-wave seed and activation effects for:
  - Silver Oaths path
  - Khenak path
  - Dragonwake path
  - dynasty protection
  - marriage-court support
  - adventure network state
- still contains shared special-case helpers like the Regatta spire swap

Assessment:
- this is now a real helper layer, not just a stub file
- more effects may still be useful later, but it is no longer obviously skeletal

---

### 7. Dynasty safeguard

**Repo status:** implemented and integrated better than before

Files:
- `decisions/verne_overhaul_decisions.txt`
- `events/verne_overhaul_dynasty_events.txt`
- `common/on_actions/verne_overhaul_on_actions.txt`

Observed state:
- the original safeguard system remains intact
- decision-side integration has improved by connecting it to helper-state activation
- the dynasty/court layer now feels more like part of the wider overhaul state machine

Assessment:
- this remains one of the strongest functional slices in the repo

---

### 8. Mission tree

**Repo status:** heavily implemented and substantially more aligned to canonical systems

File:
- `missions/Verne_Missions.txt`

Observed state:
- the mission tree remains the highest-risk file in the project
- however, a large number of missions have now been patched to interact with the canonical score/state model instead of staying entirely legacy-reward driven
- integrated missions now include broad portions of:
  - early first-wave missions
  - overseas opening and expansion missions
  - imperial / kingdom / Corinite mid-tree missions
  - late hegemonic nodes

Notable integrated mission families now include:
- `Old Friends, Old Rivals`
- `Alvar's Reform`
- `The Grand Port of Heartspier`
- `The Riches of the Khenak`
- `The Vernissage`
- `Expand the Vernissage`
- `Across the Pond`
- `In Search of Adventure`
- `The Lands of Adventure`
- `Lament's Regatta`
- `New Verne`
- `Binding the Beast`
- `Expand the Wyvern Nests`
- `Kingdom of Verne`
- `A Union of Crowns`
- `Corin's Devout Protectors`
- `Holy Corinite Empire`
- `Born of Valour`
- `With Sword and Shield`
- `The Verne Halann`
- `All Roads Lead to Verne`
- `Type 2 Wyverns`
- `A Crimson Sea`

Assessment:
- the mission tree is still not fully rewritten to the canonical design
- but it is no longer accurate to describe it as only lightly aligned
- future work should focus on structured audit/closure, not broad blind rewrites

---

## Key Reality Shift

The single biggest project reality is now:

> Verne's overhaul backbone exists across multiple systems, and the main challenge is no longer "create the systems" but "finish coverage, refine integration, and preserve coherence while scaling outward."

That means future work should increasingly ask:

**Which large remaining gaps matter most to gameplay visibility, and which are now only polish/balance problems?**

---

## Best Next Coding Slice

The most practical next implementation slice is now:

### Mission audit / completion pass against the canonical rewrite spec

Specifically:
1. map the currently touched mission set against `docs/design/mission-rewrite-spec.md`
2. mark each mission as:
   - canonically aligned enough
   - partially aligned
   - still legacy-heavy
3. close the biggest remaining gaps in grouped batches
4. only after that, consider deeper polish passes on balance, doctrine completeness, or late-game event layering

Why this slice first:
- the systems backbone is now strong enough to support more of the tree
- more gameplay-visible value now comes from mission integration than from endlessly adding backend systems
- it provides the clearest reviewable bridge between design docs and actual player experience

---

## Recommended Work Order

### Near-term
1. mission rewrite-spec audit and closure pass
2. doctrine/policy completeness review (identify what canonical pairs or doctrine families still remain)
3. balance sanity pass for NI / reforms / doctrines / policies

### After that
4. deeper late-tree mission integration
5. dynastic-state and Red Court event-layer enrichment
6. optional cleanup / deduplication passes where old legacy rewards and new score-model rewards overlap too messily

---

## Working Rule

For Verne in this repo, prefer:

- **preserve and deepen** when an overhaul system is already substantially implemented,
- **batch integration work into coherent reviewable chunks** rather than scattered one-offs,
- and treat `missions/Verne_Missions.txt` as the main remaining high-value integration surface, with systems files now largely serving as support infrastructure rather than the primary bottleneck.
