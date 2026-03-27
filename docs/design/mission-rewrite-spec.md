# Mission Rewrite Specification

This document defines the rewritten mission tree for Verne, focusing on route flexibility, projection scores, and doctrine sensitivity.

---

## Canonical Systems

### Projection Scores

**Status:** CANONICAL

Three country variables track Verne's global reach and maturity:

| Variable | Purpose | Increase Sources (examples) |
|----------|---------|----------------------------|
| `verne_overseas_projection` | Ability to operate abroad | Port of Adventure creation, monument tiers, overseas allies/subjects, relevant idea groups, flagship upgrades, expedition decisions |
| `verne_world_network` | Mature international system | Multiple overseas regions reached, major artifacts/exposition milestones, trade-port web, colonies/Trade Companies, order/commandery projection |
| `verne_dynastic_magic_machine` | Maturation of Red Court / heir shaping | Red Court decisions, Athanaeum upgrades, reform selections, missions involving mages or Type 2 Wyverns |

**Thresholds (planning targets):**

- Early: projection ≥ 2 (beginning), ≥ 4 (durable reach); world_network ≥ 2 (beginnings); dynastic_magic ≥ 2 (doctrine exists)
- Mid: projection ≥ 6 (serious capability); world_network ≥ 5 (recognizable network); dynastic_magic ≥ 5 (becoming institution)
- Late: projection ≥ 9 (world-projecting); world_network ≥ 8 (full network); dynastic_magic ≥ 8 (mature)

---

### Route Families

**Status:** CANONICAL

Major overseas missions can be completed via any of these families:

- **Route A – Classical Colonizer:** colonists, explorers, colonial nations, overseas provinces, Trade Companies.
- **Route B – Subject and Ally Projection:** subjects/allies in target regions, royal-diplomatic reach, overseas footholds via diplomacy.
- **Route C – Adventure Network:** Ports of Adventure, Network of Adventure score, completed expedition chains.
- **Route D – Monument and Institution Projection:** Twin Harbours tier, Kazakesh tier, Vernissage tier, Chapterhouse tier, flagship stage.
- **Route E – Verne Idea-Doctrine Projection:** Vernissage Ideas, Overseas Commandery Ideas, Eastern Correspondence Ideas, Grand Regatta Ideas, Imperial Sea Court Ideas.

---

### Early-Game Doctrine Precursor Flags

**Status:** CANONICAL

To avoid early missions depending on unavailable idea groups, these flags are set by reforms, estate privileges, and early mission outcomes:

- `verne_path_courtly_state`
- `verne_path_great_captains`
- `verne_path_ducal_muster`
- `verne_path_maritime_court`
- `verne_path_estuary_finance`
- `verne_path_regatta_state`

Later missions can read either these flags or the full doctrine groups once unlocked.

---

### First-Wave Mission Specifications

**Status:** IMPLEMENTATION_READY

The following 10 missions are the priority rewrite. Each entry includes identity, completion logic, rewards, and doctrine sensitivity.

#### 1. Old Friends, Old Rivals

**Identity:** Diplomatic-court opener, dynastic-legitimacy opener.

**Completion Logic:** (Standard mission triggers – no idea checks)

**Base Rewards:**
- `diplomatic_relations = 1` for 25 years (or permanent via linked reform)
- `improve_relation_modifier = 0.15` for 25 years
- 50 reform progress
- Set `verne_dynasty_protected`
- Unlock Tier 1 reform triplet
- Set one early precursor flag via followup choice

**Early Conditional Rewards (based on state, not idea groups):**
- If 2+ royal marriages: prestige + legitimacy package
- If Court of Silver Oaths path chosen: extra `diplomatic_reputation = 1` for 20 years
- If Charter of Great Captains path chosen: `verne_overseas_projection = +1`
- If Ducal Muster of Armoc path chosen: `army_tradition = 0.25` and Nobles loyalty
- If allied to two meaningful regional partners: opinion/trust reward event

**Later Retrospective Hook:** If matching doctrine groups unlocked later, followup events/decisions provide upgrades.

---

#### 2. Alvar’s Reform

**Identity:** State-foundation mission.

**Base Rewards:**
- Unlock Tier 1 reforms (Court of Silver Oaths, Charter of Great Captains, Ducal Muster of Armoc)
- Set flag unlocking Silver Oaths Ideas
- Set `verne_seed_silver_oaths`
- 25-year modifier: `reform_progress_growth = 0.15`, `yearly_legitimacy = 1`

**Early Conditional Rewards:**
- If Court of Silver Oaths chosen: extra legitimacy/dip rep
- If Charter of Great Captains chosen: `verne_overseas_projection = +1`
- If Ducal Muster of Armoc chosen: army tradition/nobles loyalty
- If Silver Oaths Ideas already active (edge case): one free idea or 75 reform progress.

---

#### 3. The Grand Port of Heartspier

**Identity:** First true sea-state mission.

**Base Rewards:**
- Unlock Twin Harbours of Heartspier monument
- Unlock flagship stage I
- Permanent Heartspier Estuary Works area modifier
- Set `verne_seed_estuary_companies`
- `verne_overseas_projection = +1`

**Early Conditional Rewards:**
- If maritime-court precursor: `diplomatic_reputation = 1` for 20 years
- If estuary-finance precursor: `goods_produced_modifier = 0.05` for 20 years
- If regatta-state precursor: `global_sailors_modifier = 0.10`, `navy_tradition = 0.25` for 20 years
- If Estuary Companies Ideas active later: followup event/decision upgrade.

---

#### 4. The Riches of the Khenak

**Identity:** Industrial foundation mission.

**Base Rewards:**
- Permanent Khenak Red-Brass Foundries area modifier
- Set flag unlocking Khenak Foundry Ideas
- Set `verne_seed_khenak_foundry`
- `artillery_cost = -0.10` for 20 years

**Early Conditional Rewards:**
- If estuary-finance precursor: `build_cost = -0.05` for 20 years
- If ducal-muster precursor: manpower or defensiveness package
- If Khenak Foundry Ideas active later: `production_efficiency = 0.10` for 20 years
- If Red Brass Ideas active later: `artillery_fire = 0.05` for 20 years.

---

#### 5. The Vernissage

**Identity:** Cultural-international institution unlock.

**Base Rewards:**
- Set flag unlocking Vernissage Ideas
- Unlock Present the Heir at the Vernissage decision
- Unlock Grand Galerie of the Vernissage monument path
- `verne_world_network = +1`

**Doctrine-Sensitive Rewards:**
- If Vernissage Patronage Ideas (≥3 ideas): capital gets stronger prestige/dev package
- If Silver Oaths Ideas (≥3): gain 50 reform progress
- If Eastern Correspondence Ideas (≥3): `improve_relation_modifier = 0.10` for 20 years.

---

#### 6. Across the Pond

**Identity:** First flexible overseas threshold mission.

**Completion Logic (any one):**
- Classic overseas foothold route
- `verne_overseas_projection >= 3`
- Overseas Commandery Ideas completed
- One subject/ally foothold in required region AND one active Port of Adventure

**Base Rewards:**
- `verne_overseas_projection = +1`
- Unlock Commission a Vernissage Expedition
- Overseas logistics modifier for 20 years

**Doctrine-Sensitive Rewards:**
- If Vernissage Ideas (≥3): `+1` additional projection
- If Overseas Commandery Ideas (≥3): `trade_range_modifier = 0.10` for 20 years
- If Imperial Sea Court Ideas (≥3): `diplomatic_reputation = 1` for 15 years.

---

#### 7. In Search of Adventure

**Identity:** Makes overseas expansion non-railroaded.

**Completion Logic (any one):**
- Colonist + explorer route
- Vernissage Ideas completed
- `verne_overseas_projection >= 4` and one Port of Adventure

**Base Rewards:**
- Unlock adventure-state systems
- `verne_overseas_projection = +2`
- `verne_world_network = +1`

**Doctrine-Sensitive Rewards:**
- If Vernissage Ideas (≥3): `global_colonial_growth = 10` for 20 years
- If Eastern Correspondence Ideas (≥3): `envoy_travel_time = -0.10` for 20 years
- If Grand Regatta Ideas (≥3): `movement_speed_in_fleet_modifier = 0.05` for 20 years.

---

#### 8. Binding the Beast

**Identity:** Wyvern-state founding mission.

**Base Rewards:**
- Unlock mythical cavalry / rider line
- Unlock reform triplet at Tier 3
- Set flag unlocking Dragonwake Ideas
- Set `verne_seed_dragonwake`, `verne_seed_chapterhouse_orders`
- Set flag allowing Chapterhouse of the Crimson Wake monument
- `verne_dynastic_magic_machine = +1`

**Conditional Rewards:**
- If ducal-muster or noble rider branch: `army_tradition = 0.25` for 20 years
- If Red Court infrastructure already active: `+1` dynastic-magic score
- If battle-mage path already active: `possible_war_wizard = 1` for 20 years
- If Dragonwake or Crimson Wake Order Ideas taken later: followup upgrades.

---

#### 9. Expand the Wyvern Nests

**Identity:** Turns nests into real infrastructure.

**Base Rewards:**
- Upgrade Crimson Eyries area logic
- `verne_dynastic_magic_machine = +1`
- `verne_overseas_projection = +1` (only if Sea-Nest line active later)

**Doctrine-Sensitive Rewards:**
- If Dragonwake Ideas (≥3): `cavalry_power = 0.05` for 20 years
- If Crimson Wake Order Ideas (≥3): cheaper order upkeep
- If Sea-Lance Doctrine Ideas (≥3): prep bonus for Sea Nest path.

---

#### 10. The Lament’s Regatta

**Identity:** True maritime-international prestige mission.

**Base Rewards:**
- Unlock Tier 6 maritime reform triplet
- Strengthen Kazakesh, the Wyvern’s Sting monument path
- `verne_world_network = +1`
- `verne_overseas_projection = +1`

**Doctrine-Sensitive Rewards:**
- If Grand Regatta Ideas (≥3): `navy_tradition = 0.50` for 20 years
- If Imperial Sea Court Ideas (≥3): `diplomatic_reputation = 1` for 20 years
- If Vernissage Ideas (≥3): `merchants = 1` for 20 years.

---

## Active Design Questions

None – the above specifications cover the first-wave missions. The remaining missions (38) follow similar patterns, but are not yet detailed.

---

## Source Merge Note

Mission specifications were extracted from the "Mission flexibility overhaul" and "First-wave mission rewrite matrix" sections. Route families, projection scores, and precursor flags are all included.