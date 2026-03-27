# Doctrine Bible

This document covers all idea-related content: Verne's national ideas, the 21 exclusive doctrine groups, and the associated policy layer.

---

## Canonical Systems

### Verne National Ideas

**Status:** IMPLEMENTATION_READY

These are Verne's permanent country ideas, separate from the doctrine groups.

#### Traditions

| Effect | Value |
|--------|------|
| `leader_land_shock` | +1 |
| `diplomatic_relations` | +1 |
| `global_trade_power` | +10% |
| `naval_forcelimit_modifier` | +10% |
| `admiral_maneuver` | +1 |
| `improve_relation_modifier` | +10% |
| `yearly_prestige` | +1 |
| `global_sailors_modifier` | +10% |
| `mages_loyalty_modifier` | +5% |
| `monarch_military_power` | +1 |

#### Ideas

| # | Name | Effects |
|---|------|---------|
| 1 | Legacy of the Wyvern-Kings | `army_tradition_from_battle = +0.25`<br>`cav_to_inf_ratio = +10%`<br>`prestige_from_land = +10%`<br>`free_land_leader_pool = +1`<br>hidden event weighting toward Blood of the Wyvern-Kings |
| 2 | Pearlescent Rivals | `embargo_efficiency = +20%`<br>`capture_ship_chance = +10%`<br>`trade_steering = +10%`<br>`naval_tradition_from_trade = +50%`<br>`morale_of_navies = +5%` |
| 3 | The Heartspier Scale | `global_colonial_growth = +20`<br>`envoy_travel_time = -15%`<br>`range = +20%`<br>`naval_attrition = -10%`<br>`trade_range_modifier = +20%` |
| 4 | Red Brass Ordnance | `artillery_fire = +0.10`<br>`artillery_cost = -10%`<br>`heavy_ship_cost = -10%`<br>`ship_durability = +5%`<br>`global_ship_cost = -5%` |
| 5 | Birthplace of the Regatta | `global_sailors_modifier = +15%`<br>`sailors_recovery_speed = +15%`<br>`navy_tradition = +0.50`<br>`prestige = +0.50`<br>`movement_speed_in_fleet_modifier = +10%` |
| 6 | The First Corinite Emperors | `diplomatic_reputation = +1`<br>`improve_relation_modifier = +10%`<br>`global_missionary_strength = +1%`<br>`yearly_legitimacy = +0.50`<br>`tolerance_own = +1` |
| 7 | Homeland of Great Adventurers | `mercenary_manpower = +25%`<br>`general_cost = -25%`<br>`prestige_from_naval = +10%`<br>`merchants = +1`<br>hidden event weighting toward expedition/artifact outcomes |

#### Ambition

| Effect | Value |
|--------|------|
| `diplomatic_reputation` | +1 |
| `diplomatic_relations` | +1 |
| `morale_of_armies` | +10% |
| `morale_of_navies` | +10% |
| `all_power_cost` | -2.5% |

---

### Doctrine Groups (Verne-Exclusive Idea Groups)

**Status:** CANONICAL (full specifications)

These 21 groups replace the standard idea groups for Verne. They are organized into ADM, DIP, MIL categories. Each group includes 7 ideas and a completion bonus.

The following entries contain the **total package** (sum of all ideas + bonus) as specified in the design. The internal idea-by-idea breakdown is preserved where available.

#### 1. Silver Oaths Ideas (ADM)
**Theme:** Court administration, dynastic statecraft.  
**Role:** Court/Administrative hybrid.

| Effect | Value |
|--------|------|
| `advisor_cost` | -10% |
| `reform_progress_growth` | +15% |
| `diplomatic_reputation` | +1 |
| `yearly_legitimacy` | +1 |
| `advisor_pool` | +1 |
| `free_land_leader_pool` | +1 |
| `all_power_cost` | -2.5% |

**Idea breakdown (from canonical internal package):**
1. Oathbound Households: `advisor_cost = -0.05`
2. Ducal Registries: `reform_progress_growth = 0.10`
3. The Silver Chamber: `diplomatic_reputation = 1`
4. Ceremonial Patronage: `yearly_legitimacy = 0.50`, `prestige = 0.50`
5. The Red Secretariats: `monthly_adm_power = 1`
6. Court of Distinguished Service: `advisor_pool = 1`, `free_land_leader_pool = 1`
7. Dynastic Instruction: hidden heir-quality weighting package

Completion bonus: `all_power_cost = -0.025`

**Dependencies:** Unlocked via Alvar's Reform and related missions.

---

#### 2. Red Court Ideas (ADM)
**Theme:** Magical statecraft, dynastic magic management.  
**Role:** Innovative/magical administration lane.

| Effect | Value |
|--------|------|
| `advisor_pool` | +1 |
| `monthly_adm_power` | +1 |
| `reform_progress_growth` | +10% |
| `possible_policy` | +1 |
| `mages_loyalty_modifier` | +10% |
| hidden heir/magic weighting | - |
| hidden evocation progression | - |

**Idea breakdown:**
1. Tutors of Evocation: `mages_loyalty_modifier = 0.05`
2. The Scarlet Curriculum: `advisor_pool = 1`
3. Court Magisteries: `monthly_adm_power = 1`
4. Arcane Record Offices: `reform_progress_growth = 0.10`
5. The Red Secretariat: `possible_policy = 1`
6. Wards of the Ducal Household: hidden ruler-survival / mage-court quality
7. Bloodline Examinations: hidden heir-mage/evocation weighting

Completion bonus: `mages_loyalty_modifier = 0.05` and hidden evocation advancement support.

**Dependencies:** Unlocked via Red Court mission line.

---

#### 3. Estuary Companies Ideas (ADM)
**Theme:** Mercantile administration, port finance.  
**Role:** Economic/infrastructure maritime lane.

| Effect | Value |
|--------|------|
| `build_cost` | -10% |
| `goods_produced_modifier` | +10% |
| `trade_efficiency` | +10% |
| `global_ship_trade_power` | +15% |
| `light_ship_power` | +10% |
| `global_ship_cost` | -10% |
| `interest` | -1 |
| `development_cost` | -5% |

**Idea breakdown:**
1. Estuary Ledgers: `build_cost = -0.05`
2. Harbor Assessors: `trade_efficiency = 0.05`
3. Licensed Wharf Companies: `global_ship_trade_power = 0.10`
4. Bonded Warehouses: `goods_produced_modifier = 0.05`
5. River-Sea Taxation: `interest = -1`
6. Captains' Accounts: `global_ship_cost = -0.05`
7. Crowned Investors: `development_cost = -0.05`

Completion bonus: `build_cost = -0.05`, `goods_produced_modifier = 0.05`, `light_ship_power = 0.10`

**Dependencies:** Unlocked via The Grand Port of Heartspier.

---

#### 4. Khenak Foundry Ideas (ADM)
**Theme:** Military-industrial state building.  
**Role:** Infrastructure + military industry hybrid.

| Effect | Value |
|--------|------|
| `artillery_cost` | -10% |
| `production_efficiency` | +10% |
| `defensiveness` | +10% |
| `manpower_modifier` | +10% |
| `build_cost` | -5% |
| `artillery_fire` | +0.05 |
| `governing_cost` | -5% |

**Idea breakdown:**
1. Red-Brass Contracts: `build_cost = -0.05`
2. Foundry Apprenticeships: `production_efficiency = 0.05`
3. Powder Magazines: `defensiveness = 0.05`
4. Iron Roads to the Harbours: `development_cost = -0.05`
5. State Artillery Parks: `artillery_cost = -0.10`
6. Master Gunfounders: `artillery_fire = 0.05`
7. Khenak Furnaces: `manpower_modifier = 0.10`

Completion bonus: `production_efficiency = 0.05`, `defensiveness = 0.05`

**Dependencies:** Unlocked via The Riches of the Khenak.

---

#### 5. Vernissage Patronage Ideas (ADM)
**Theme:** State-sponsored culture, spectacle, artifact display, elite institutions.  
**Role:** Prestige-court administration.

| Effect | Value |
|--------|------|
| `prestige` | +1 |
| `yearly_innovativeness` | +0.25 |
| `development_cost` | -5% |
| `institution_spread` | +10% |
| `advisor_cost` | -5% |
| `advisor_pool` | +1 |
| hidden artifact/exposition reward enhancement | - |

**Idea breakdown:**
1. Curators of Glory: `prestige = 0.50`
2. Hall-Masters of the Vernissage: `advisor_cost = -0.05`
3. Courtly Patronage Offices: `advisor_pool = 1`
4. Catalogues of Wonder: hidden artifact/exposition reward improvement
5. Guest Galleries: `improve_relation_modifier = 0.10`
6. Urban Grandeur: `development_cost = -0.05`
7. The Memory of the World: `institution_spread = 0.10`

Completion bonus: `yearly_innovativeness = 0.25`

**Dependencies:** Unlocked via The Vernissage mission.

---

#### 6. Corinite Stewardship Ideas (ADM)
**Theme:** Disciplined faith-state administration.  
**Role:** Administrative religious governance.

| Effect | Value |
|--------|------|
| `missionaries` | +1 |
| `global_missionary_strength` | +2% |
| `tolerance_own` | +1 |
| `yearly_legitimacy` | +1 |
| `stability_cost_modifier` | -10% |
| `diplomatic_reputation` | +1 |
| `clergy_loyalty_modifier` | +10% |

**Idea breakdown:**
1. Imperial Catechists: `missionaries = 1`
2. Offices of Pious Instruction: `global_missionary_strength = 0.01`
3. Corinite Record-Keepers: `stability_cost_modifier = -0.10`
4. Tithes of the Crown: `yearly_legitimacy = 0.50`
5. Concord of Oaths and Faith: `tolerance_own = 1`
6. Pilgrim Administration: `diplomatic_reputation = 1`
7. The Emperor’s Example: `clergy_loyalty_modifier = 0.10`

Completion bonus: `yearly_legitimacy = 0.50`, `global_missionary_strength = 0.01`

**Dependencies:** Unlocked via Corinite conversion or related missions.

---

#### 7. Imperial Chancery Ideas (ADM)
**Theme:** Compact imperial governance, dominion over the Empire.  
**Role:** Governing/state maintenance/annexation support.

| Effect | Value |
|--------|------|
| `governing_capacity_modifier` | +15% |
| `state_maintenance_modifier` | -10% |
| `autonomy_change_time` | -10% |
| `diplomatic_annexation_cost` | -10% |
| `administrative_efficiency` | +5% |
| `global_unrest` | -1 |
| `reform_progress_growth` | +10% |

**Idea breakdown:**
1. Ducal Chanceries: `governing_capacity_modifier = 0.10`
2. Crownland Surveyors: `state_maintenance_modifier = -0.10`
3. Imperial Proctors: `global_unrest = -1`
4. Measured Autonomies: `autonomy_change_time = -0.10`
5. Unified Seals: `diplomatic_annexation_cost = -0.10`
6. Auditors of the Marches: `reform_progress_growth = 0.10`
7. Chancery Absolutes: `administrative_efficiency = 0.05`

Completion bonus: `governing_capacity_modifier = 0.05`

**Dependencies:** Unlocked via missions like Old Friends, Old Rivals, Kingdom of Verne.

---

#### 8. Vernissage Ideas (DIP)
**Theme:** Adventure network, prestige-state exploration, overseas courtly display.  
**Role:** Exploration/Expansion hybrid.

| Effect | Value |
|--------|------|
| `range` | +25% |
| `global_colonial_growth` | +20 |
| `colonists` | +1 |
| `envoy_travel_time` | -15% |
| `trade_steering` | +10% |
| `global_trade_power` | +10% |
| `merchants` | +1 |

**Idea breakdown:**
1. Captains of the Vernissage: `range = 0.15`
2. Ports of Adventure: `global_colonial_growth = 10` (plus hidden projection increment)
3. The Heartspier Scale: `envoy_travel_time = -0.10`
4. Eastern Princes’ Correspondence: `improve_relation_modifier = 0.10`
5. Expedition Ledgers: `trade_steering = 0.10`
6. Regatta Laurels: `navy_tradition = 0.50`, `global_sailors_modifier = 0.10`
7. Worlds on Display: `merchants = 1`

Completion bonus: `colonists = 1`, `range = 0.10`

**Dependencies:** Unlocked via The Vernissage mission.

---

#### 9. Imperial Sea Court Ideas (DIP)
**Theme:** Fleet-backed diplomacy, prestige projection.  
**Role:** Diplomatic + naval prestige hybrid.

| Effect | Value |
|--------|------|
| `diplomatic_reputation` | +1 |
| `diplomatic_relations` | +1 |
| `improve_relation_modifier` | +15% |
| `morale_of_navies` | +10% |
| `naval_tradition_from_trade` | +50% |
| `prestige` | +0.50 |
| `global_ship_trade_power` | +10% |
| `light_ship_power` | +10% |

**Idea breakdown:**
1. Sea-Borne Envoys: `diplomatic_reputation = 1`
2. Oath Harbours: `diplomatic_relations = 1`
3. Pearl-Wreathed Audiences: `improve_relation_modifier = 0.10`
4. Admirals of Ceremony: `naval_tradition_from_trade = 0.25`
5. Convoys of Prestige: `prestige = 0.50`
6. Embassies of the Wake: `envoy_travel_time = -0.10`
7. Thrones Across the Waves: `global_ship_trade_power = 0.10`, `light_ship_power = 0.10`

Completion bonus: `morale_of_navies = 0.10`, `naval_tradition_from_trade = 0.25`

**Dependencies:** Unlocked via early diplomatic/maritime missions.

---

#### 10. Grand Regatta Ideas (DIP)
**Theme:** Maritime competition, sailors, logistics, speed, sea-culture mastery.  
**Role:** Maritime/Naval utility.

| Effect | Value |
|--------|------|
| `global_sailors_modifier` | +20% |
| `sailors_recovery_speed` | +20% |
| `movement_speed_in_fleet_modifier` | +10% |
| `navy_tradition` | +0.50 |
| `trade_efficiency` | +10% |
| `morale_of_navies` | +5% |
| `prestige` | +0.50 |
| `light_ship_power` | +10% |

**Idea breakdown:**
1. Racing Harbours: `global_sailors_modifier = 0.10`
2. Laurels of the Helm: `prestige = 0.50`
3. Master Tidemaps: `movement_speed_in_fleet_modifier = 0.05`
4. Sailors’ Guilds: `sailors_recovery_speed = 0.10`
5. Longwake Navigation: `navy_tradition = 0.25`
6. Regatta Drills: `morale_of_navies = 0.05`
7. Sea-Lords’ Festivals: `trade_efficiency = 0.10`, `light_ship_power = 0.10`

Completion bonus: `global_sailors_modifier = 0.10`, `movement_speed_in_fleet_modifier = 0.05`

**Dependencies:** Unlocked via The Lament's Regatta or similar.

---

#### 11. Overseas Commandery Ideas (DIP)
**Theme:** Strategic footholds, island stations, subject-supported expansion.  
**Role:** Expansion/subject-colonial support.

| Effect | Value |
|--------|------|
| `range` | +20% |
| `global_tariffs` | +10% |
| `governing_capacity_modifier` | +10% |
| `diplomatic_annexation_cost` | -10% |
| `trade_range_modifier` | +20% |
| `liberty_desire_from_subject_development` | -10% |
| `hostile_fleet_attrition` | +1 |

**Idea breakdown:**
1. Fortified Havens: `hostile_fleet_attrition = 1`
2. Ducal Factors Abroad: `trade_range_modifier = 0.10`
3. Commandery Charters: `range = 0.10`
4. Garrisoned Wharves: `naval_forcelimit_modifier = 0.10`
5. Loyal Captains Overseas: `liberty_desire_from_subject_development = -0.10`
6. Island Magazines: `governing_capacity_modifier = 0.10`
7. The Long Hand of Verne: `diplomatic_annexation_cost = -0.10`

Completion bonus: `range = 0.10`, `trade_range_modifier = 0.10`

**Dependencies:** Unlocked via later overseas missions.

---

#### 12. Eastern Correspondence Ideas (DIP)
**Theme:** Embassies, eastern courts, cosmopolitan prestige, negotiated access abroad.  
**Role:** Outward diplomatic network.

| Effect | Value |
|--------|------|
| `improve_relation_modifier` | +15% |
| `diplomatic_reputation` | +1 |
| `envoy_travel_time` | -15% |
| `merchants` | +1 |
| `prestige` | +0.50 |
| `trade_steering` | +5% |
| `years_of_nationalism` | -5 |

**Idea breakdown:**
1. Letters of Introduction: `envoy_travel_time = -0.10`
2. Translators of the Wake: `improve_relation_modifier = 0.10`
3. Embassy Hosts: `prestige = 0.50`
4. Pearl Road Agents: `trade_steering = 0.05`
5. Courtly Interpreters: `diplomatic_reputation = 1`
6. Overseas Correspondents: `merchants = 1`
7. Princes’ Exchanges: `years_of_nationalism = -5`

Completion bonus: `improve_relation_modifier = 0.05`

**Dependencies:** Unlocked via missions like Halanni Exposition.

---

#### 13. Apostolic Sea-Lanes Ideas (DIP)
**Theme:** Faith spread through maritime and diplomatic reach.  
**Role:** Religious-diplomatic maritime lane.

| Effect | Value |
|--------|------|
| `missionaries` | +1 |
| `global_missionary_strength` | +1% |
| `diplomatic_relations` | +1 |
| `morale_of_navies` | +5% |
| `trade_efficiency` | +10% |
| `naval_forcelimit_modifier` | +10% |
| `prestige` | +0.50 |

**Idea breakdown:**
1. Missionary Captains: `missionaries = 1`
2. Pilgrim Convoys: `morale_of_navies = 0.05`
3. Sacred Harbours: `trade_efficiency = 0.05`
4. Apostolic Chartmakers: `naval_forcelimit_modifier = 0.10`
5. Bannered Convictions: `diplomatic_relations = 1`
6. Sea-Lane Preachers: `global_missionary_strength = 0.01`
7. The Wake of Corin: `prestige = 0.50`

Completion bonus: `trade_efficiency = 0.05`, `morale_of_navies = 0.05`

**Dependencies:** Unlocked via Corinite imperial missions.

---

#### 14. Pearlescent Concord Ideas (DIP)
**Theme:** Alliance webs, prestige diplomacy, imperial arbitration, league-building.  
**Role:** Influence/alliance-management.

| Effect | Value |
|--------|------|
| `diplomatic_relations` | +1 |
| `diplomatic_reputation` | +1 |
| `diplomatic_annexation_cost` | -10% |
| `liberty_desire_in_subjects` | -10 |
| `improve_relation_modifier` | +10% |
| `prestige` | +0.50 |
| `envoy_travel_time` | -10% |

**Idea breakdown:**
1. Concords of the Pearl: `diplomatic_relations = 1`
2. Crowned Mediators: `diplomatic_reputation = 1`
3. Wedding Fleets: `prestige = 0.50`
4. Trusted Envoys: `improve_relation_modifier = 0.10`
5. Oath-Bound Vassals: `liberty_desire_in_subjects = -10`
6. Feasts of Reconciliation: `envoy_travel_time = -0.10`
7. The Prince’s Word: `diplomatic_annexation_cost = -0.10`

Completion bonus: `improve_relation_modifier = 0.05`

**Dependencies:** Unlocked via diplomatic missions.

---

#### 15. Dragonwake Ideas (MIL)
**Theme:** Wyvern aristocracy, martial dynastic excellence.  
**Role:** Aristocratic + Quality hybrid.

| Effect | Value |
|--------|------|
| `cav_to_inf_ratio` | +20% |
| `cavalry_cost` | -10% |
| `cavalry_power` | +15% |
| `army_tradition` | +0.50 |
| `leader_land_shock` | +1 |
| `yearly_army_professionalism` | +0.005 |
| `morale_of_armies` | +10% |

**Idea breakdown:**
1. Noble Riders of Armoc: `cav_to_inf_ratio = 0.10`, `cavalry_cost = -0.05`
2. Sky-Lance Discipline: `cavalry_power = 0.10`
3. The Dragonwake Muster: `army_tradition = 0.25`
4. Aerial Reconnaissance: `leader_land_manuever = 1`
5. Storm-Crowned Nobility: `yearly_army_professionalism = 0.005`
6. Red Wake Shock Doctrine: `leader_land_shock = 1`
7. Knights of the Crimson Wing: hidden martial-heir weighting

Completion bonus: `morale_of_armies = 0.10`, `cavalry_power = 0.05`

**Dependencies:** Unlocked via Binding the Beast.

---

#### 16. Crimson Wake Order Ideas (MIL)
**Theme:** Institutional knightly orders, elite state riders.  
**Role:** Mercenary elite force lane.

| Effect | Value |
|--------|------|
| `mercenary_cost` | -10% |
| `merc_maintenance_modifier` | -10% |
| `free_leader_pool` | +1 |
| `army_tradition` | +0.25 |
| `cav_to_inf_ratio` | +15% |
| `reinforce_cost_modifier` | -10% |
| hidden order-founding discount | - |

**Idea breakdown:**
1. Knightly Chapter Rolls: `mercenary_cost = -0.05`
2. Order Muster-Houses: `merc_maintenance_modifier = -0.05`
3. Bannered Retinues: `free_leader_pool = 1`
4. Oath-Trained Lances: `cav_to_inf_ratio = 0.10`
5. Ducal Subsidies: `reinforce_cost_modifier = -0.10`
6. Marshal-Chaplains: `army_tradition = 0.25`
7. Permanent Commanderies: hidden order-founding discount

Completion bonus: `mercenary_cost = -0.05`, hidden order-upgrade package

**Dependencies:** Unlocked via Binding the Beast and Chapterhouse.

---

#### 17. Battle-Evocation Ideas (MIL)
**Theme:** War-mage command, battlefield sorcery doctrine.  
**Role:** Offensive/magical Quality hybrid.

| Effect | Value |
|--------|------|
| `leader_land_fire` | +1 |
| `morale_of_armies` | +10% |
| `artillery_fire` | +0.10 |
| `siege_ability` | +10% |
| `possible_war_wizard` | +1 |
| hidden ruler/heir evocation weighting | - |
| hidden battle-mage event package | - |

**Idea breakdown:**
1. Arcane Officer Schools: `leader_land_fire = 1`
2. Field Evocations: `morale_of_armies = 0.05`
3. Red Wake Battlemagi: `possible_war_wizard = 1`
4. Spell-Guided Batteries: `artillery_fire = 0.05`
5. Stormline Doctrine: `siege_ability = 0.05`
6. War-Court Coordination: hidden battle-mage event enhancement
7. The Prince in the Van: hidden ruler/heir evocation weighting

Completion bonus: `morale_of_armies = 0.05`, `artillery_fire = 0.05`

**Dependencies:** Unlocked via Red Court and military missions.

---

#### 18. Red Brass Ideas (MIL)
**Theme:** Artillery, fleet gunnery, engineered war.  
**Role:** Artillery-heavy quality lane.

| Effect | Value |
|--------|------|
| `artillery_fire` | +0.10 |
| `artillery_cost` | -10% |
| `heavy_ship_cost` | -10% |
| `ship_durability` | +10% |
| `defensiveness` | +10% |
| `military_tech_cost_modifier` | -5% |
| `land_forcelimit_modifier` | +10% |

**Idea breakdown:**
1. State Gunparks: `artillery_cost = -0.10`
2. Foundry Calibration: `artillery_fire = 0.05`
3. Powder Discipline: `defensiveness = 0.05`
4. Siege Engineers: `siege_ability = 0.05`
5. Red-Brass Hull Guns: `heavy_ship_cost = -0.10`
6. Gunnery Instructors: `military_tech_cost_modifier = -0.05`
7. Ironwilled Crews: `ship_durability = 0.10`

Completion bonus: `land_forcelimit_modifier = 0.10`, `artillery_fire = 0.05`

**Dependencies:** Unlocked via The Riches of the Khenak and related.

---

#### 19. Sea-Lance Doctrine Ideas (MIL)
**Theme:** Integrated air-sea warfare, expeditionary strike capacity.  
**Role:** Naval-military hybrid.

| Effect | Value |
|--------|------|
| `movement_speed_in_fleet_modifier` | +10% |
| `leader_land_manuever` | +1 |
| `morale_of_navies` | +10% |
| `naval_forcelimit_modifier` | +10% |
| `land_attrition` | -10% |
| `naval_attrition` | -10% |
| `transport_power` | +10% |

**Idea breakdown:**
1. Flight Deck Routines: `movement_speed_in_fleet_modifier = 0.05`
2. Deck-Lance Escorts: `morale_of_navies = 0.05`
3. Sea-Nest Coordination: `leader_land_manuever = 1`
4. Aerial Spotters: `siege_ability = 0.05`
5. Strike Convoys: `land_attrition = -0.10`
6. Wakeborne Assaults: `naval_attrition = -0.10`
7. Oceanic Pursuit: `naval_forcelimit_modifier = 0.10`

Completion bonus: `movement_speed_in_fleet_modifier = 0.05`, `transport_power = 0.10`

**Dependencies:** Unlocked via Sea Nest and maritime missions.

---

#### 20. Apostolic Valour Ideas (MIL)
**Theme:** Corinite knightly militarism, righteous imperial warfare.  
**Role:** Religious + Offensive martial lane.

| Effect | Value |
|--------|------|
| `morale_of_armies` | +10% |
| `prestige_from_land` | +10% |
| `army_tradition` | +0.50 |
| `global_missionary_strength` | +1% |
| `discipline` | +2.5% |
| `war_exhaustion` | -0.02 |
| `yearly_devotion` | +0.25 (or equivalent) |

**Idea breakdown:**
1. Corin’s Example: `morale_of_armies = 0.05`
2. Bannered Devotion: `prestige_from_land = 0.10`
3. March Sermons: `global_missionary_strength = 0.01`
4. Sacred Drill: `army_tradition = 0.25`
5. Righteous Charges: `discipline = 0.025`
6. Commanderies of Valour: hidden holy-order synergy
7. The Emperor’s Sword: `war_exhaustion = -0.02`

Completion bonus: `morale_of_armies = 0.05`, `army_tradition = 0.25`

**Dependencies:** Unlocked via Corinite missions.

---

#### 21. Silver Banner Ideas (MIL)
**Theme:** Compact elite army, disciplined court field force, imperial dominance.  
**Role:** Pure quality/professionalism lane.

| Effect | Value |
|--------|------|
| `discipline` | +5% |
| `yearly_army_professionalism` | +0.005 |
| `army_tradition` | +0.50 |
| `infantry_combat_ability` | +10% |
| `cavalry_combat_ability` | +10% |
| `land_forcelimit_modifier` | +10% |
| `reinforce_speed` | +10% |

**Idea breakdown:**
1. Household Banners: `discipline = 0.025`
2. Ducal Drillmasters: `yearly_army_professionalism = 0.005`
3. Parade Ground Standards: `army_tradition = 0.25`
4. Veteran Cadres: `infantry_combat_ability = 0.10`
5. Chosen Captains: `cavalry_combat_ability = 0.10`
6. The Silver Line: `land_forcelimit_modifier = 0.10`
7. Imperial Reserve Companies: `reinforce_speed = 0.10`

Completion bonus: `discipline = 0.025`, `army_tradition = 0.25`

**Dependencies:** Unlocked via early military missions.

---

### Policies

**Status:** CANONICAL (first-wave exact packages)

The policy layer provides two-way synergies between doctrine groups. Policies are named with Verne flavor (e.g., court decrees, admiralty ordinances). The following is the first-wave set; the full matrix should eventually cover all pairs.

| Policy Name | Pair | Power | Effects |
|-------------|------|-------|---------|
| Articles of the Silver Admiralty | Silver Oaths + Imperial Sea Court | DIP | `diplomatic_reputation = 1`<br>`morale_of_navies = 0.05` |
| Charter of Overseas Audiences | Silver Oaths + Vernissage | DIP | `envoy_travel_time = -0.10`<br>`improve_relation_modifier = 0.10` |
| Ordinance of Noble Service | Silver Oaths + Dragonwake | MIL | `army_tradition = 0.25`<br>`yearly_legitimacy = 0.50` |
| Statutes of Arcane Instruction | Silver Oaths + Red Court | ADM | `advisor_pool = 1`<br>hidden heir-quality/mage weighting |
| Heartspier Shipping Code | Estuary Companies + Grand Regatta | DIP | `light_ship_power = 0.10`<br>`trade_efficiency = 0.05` |
| Convoys of State | Estuary Companies + Imperial Sea Court | DIP | `global_ship_trade_power = 0.15`<br>`diplomatic_reputation = 1` |
| Audit of Chartered Harbours | Estuary Companies + Imperial Chancery | ADM | `yearly_corruption = -0.05`<br>`build_cost = -0.05` |
| Accords of the Eastern Princes | Vernissage + Eastern Correspondence | DIP | `range = 0.10`<br>`diplomatic_reputation = 1` |
| Regatta of Distant Harbours | Vernissage + Grand Regatta | DIP | `movement_speed_in_fleet_modifier = 0.10`<br>`global_sailors_modifier = 0.10` |
| Articles of Remote Command | Vernissage + Overseas Commandery | DIP | `trade_range_modifier = 0.15`<br>`governing_capacity_modifier = 0.05` |
| Capitular Articles of the Wake | Dragonwake + Crimson Wake Order | MIL | `mercenary_cost = -0.05`<br>`cavalry_power = 0.10` |
| Storm-Crowned Doctrine | Dragonwake + Battle-Evocation | MIL | `leader_land_shock = 1`<br>`possible_war_wizard = 1` |
| Articles of the Silver Line | Dragonwake + Silver Banner | MIL | `discipline = 0.025`<br>`cavalry_combat_ability = 0.10` |
| Sea-Nest Command Statutes | Crimson Wake Order + Sea-Lance Doctrine | MIL | `movement_speed_in_fleet_modifier = 0.05`<br>hidden order-upgrade support |
| Protocols of Controlled Devastation | Battle-Evocation + Red Court | ADM | `artillery_fire = 0.05`<br>magical-infamy containment support |
| Foundry War Ordinances | Red Brass + Khenak Foundry | MIL | `artillery_cost = -0.10`<br>`defensiveness = 0.10` |
| Concord of Seals and Oaths | Imperial Chancery + Pearlescent Concord | DIP | `diplomatic_annexation_cost = -0.10`<br>`liberty_desire_in_subjects = -5` |
| Pilgrim Convoy Articles | Corinite Stewardship + Apostolic Sea-Lanes | DIP | `global_missionary_strength = 0.01`<br>`morale_of_navies = 0.05` |
| Capitular Ordinance of Corin | Corinite Stewardship + Apostolic Valour | MIL | `morale_of_armies = 0.05`<br>`yearly_legitimacy = 0.50` |

**Implementation note:** Policies should be generated for all doctrine pairs using a structured role mapping. The above are exact first-wave packages.

---

## Active Design Questions

None for doctrine groups – all are fully specified. However, see the open questions file for any repo-specific integration needs.

---

## Source Merge Note

The doctrine section consolidated:
- National ideas from multiple scattered sections into one canonical table.
- All 21 doctrine groups from various parts of the source (including partial lists, effect-only lists, and internal idea breakdowns) into unified entries. In each case, the total package was derived from the most complete description, and the internal idea list was preserved where provided.
- First-wave policies from the detailed policy matrix and the exact packages section.

No numeric values were changed.