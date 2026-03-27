# Orders, Monuments, and Mercenaries

This document covers the Chapterhouse monument, wyvern order companies, unlock flow, costs, and upgrade paths.

---

## Canonical Systems

### Monuments

**Status:** CANONICAL

Core monuments that unlock systems:

| Monument | Purpose |
|----------|---------|
| **The Chapterhouse of the Crimson Wake** | Keystone order integration; tiers unlock order companies and upgrades |
| **The Twin Harbours of Heartspier** | Maritime infrastructure |
| **The Hall of Silver Oaths** | Dynastic court |
| **Kazakesh, the Wyvern's Sting** | Wyvern military |
| **The Eyries of the Crimson Wake** | Order support |
| **The Red Court Athanaeum** | Magical court |
| **The Grand Galerie of the Vernissage** | Prestige exposition |

**Chapterhouse Tier Logic:**
- Tier 1: unlocks first order decision
- Tier 2: unlocks second order decision
- Tier 3: unlocks third order decision and strongest order bonuses

---

### Wyvern Order Companies

**Status:** CANONICAL

Three elite mercenary companies representing different branches of the wyvern orders.

#### 1. The Crimson Wake Lances
- **Role:** Most elite noble shock-rider order
- **Size philosophy:** smallest but strongest
- **Use case:** decisive battles

**Draft Company Profile:**
- `regiments_per_development = 0.025`
- `cavalry_weight = 1.0`
- `artillery_weight = 0`
- `cavalry_cap = 16`
- `cost_modifier = 0.70`
- `mercenary_desc_key = FREE_OF_ARMY_PROFESSIONALISM_COST`

**Draft Modifier Package:**
- `cav_to_inf_ratio = 1.0`
- `cavalry_power = 0.25`
- `movement_speed = 0.15`
- `shock_damage = 0.10`

#### 2. The Heartspier Skyguard
- **Role:** Balanced court-guard and escort order
- **Size philosophy:** medium
- **Use case:** main army support and prestige warfare

**Draft Company Profile:**
- `regiments_per_development = 0.04`
- `cavalry_weight = 0.75`
- `artillery_weight = 0`
- `cavalry_cap = 20`
- `cost_modifier = 0.65`
- `mercenary_desc_key = FREE_OF_ARMY_PROFESSIONALISM_COST`

**Draft Modifier Package:**
- `cav_to_inf_ratio = 1.0`
- `cavalry_power = 0.20`
- `movement_speed = 0.15`
- `land_morale = 0.10`

#### 3. The Khenak Talons
- **Role:** Frontier hard-rider order
- **Size philosophy:** medium-large relative to others
- **Use case:** repeated campaigning and difficult terrain

**Draft Company Profile:**
- `regiments_per_development = 0.05`
- `cavalry_weight = 0.85`
- `artillery_weight = 0`
- `cavalry_cap = 24`
- `cost_modifier = 0.60`
- `mercenary_desc_key = FREE_OF_ARMY_PROFESSIONALISM_COST`

**Draft Modifier Package:**
- `cav_to_inf_ratio = 1.0`
- `cavalry_power = 0.20`
- `movement_speed = 0.10`
- `shock_damage_received = -0.10`

---

### Founding Costs and Logic

**Status:** CANONICAL

Each order requires a founding decision that consumes resources and unlocks the mercenary company.

**Founding Requirements:**
- Chapterhouse at required tier (Tier 1 for first order, etc.)
- Money, manpower, and possibly MIL power or army tradition
- Not already founded

**Cost Direction (suggested):**

| Order | Ducats | MIL | Manpower |
|-------|--------|-----|----------|
| Crimson Wake Lances | 250-300 | 50 | 3000 |
| Heartspier Skyguard | 225-275 | 40 | 3500 |
| Khenak Talons | 200-250 | 50 | 4500 |

**Implementation:** Use `unlock_merc_company = { merc_company = ... free_merc = yes }` after paying costs. Manpower removal via direct effect.

---

### Upgrade Path

**Status:** CANONICAL

Later missions or Chapterhouse tiers should unlock upgraded variants, not mutate the existing company.

Example upgrade families:
- Crimson Wake Lances → Crimson Wake Veteran Lances
- Heartspier Skyguard → Heartspier Skyguard Royal
- Khenak Talons → Khenak Talons of the High Eyries

These variants can raise cavalry cap, regiments per development, and one premium combat stat.

---

### Integration with Doctrine Groups

**Status:** CANONICAL

- Crimson Wake Order Ideas give hidden founding/upkeep advantages.
- Dragonwake Ideas give stronger quality, not bigger pools.
- Expand the Wyvern Nests unlocks upgraded order variants.
- Sea-Nest Ascendancy unlocks expeditionary rider-company variants.
- `mercenary_manpower` modifiers can be applied to support orders.

---

## Active Design Questions

None – all systems are fully specified.

---

## Source Merge Note

This file consolidates "Monument architecture", "Wyvern orders and mercenary architecture", and the order company specifications from the source. All draft numbers and upgrade logic are preserved.