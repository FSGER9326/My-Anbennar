# Pressure, Disasters, and Corinite Integration

This document covers pressure systems (legitimacy/prestige/projection), anti-corruption tools, disasters, Corinite mainline support, and alternative paths.

---

## Canonical Systems

### Pressure Mechanics

**Status:** CANONICAL

To balance Verne's power, the state must be maintained. If key stats fall below thresholds, negative modifiers or disaster progress are triggered.

| Pressure Type | Threshold | Triggered Penalty (example) | Duration |
|---------------|-----------|----------------------------|----------|
| **Low Legitimacy** | < 50 (after major dynastic-state tools active) | "Fading Ducal Authority": `yearly_legitimacy = -1`, `liberty_desire_in_subjects = 5`, `estate_loyalty_equilibrium = -5` | 5 years |
| **Low Prestige** | < 0 (after Vernissage/Regatta/world-court systems active) | "Tarnished Courtly Reputation": `diplomatic_reputation = -1`, `improve_relation_modifier = -0.10` | 5 years |
| **Low Power Projection** | < 25 (after sea-state/imperial/rider doctrine) | "Empty Boasts of the Wake": `prestige = -0.50`, `army_tradition = -0.25`, `navy_tradition = -0.25` | 5 years |

These are applied via events or country modifiers, not as permanent hidden modifiers.

---

### Anti-Corruption Tools

**Status:** CANONICAL

Verne can actively reduce corruption through three decisions (each with 10-12 year cooldown).

#### 1. Purge the Admiralty Ledgers
- **Theme:** Financial anti-corruption sweep
- **Costs:** 100 ducats (or scaled) + 50 ADM
- **Effects:** `add_corruption = -1`, optional `add_mercantilism = 1` if harsh branch, temporary `trade_efficiency = -0.05` for 5 years if harsh, possible Burghers anger.

#### 2. Muster the Ducal Auditors
- **Theme:** Anti-corruption through noble and chancery discipline
- **Costs:** 50 MIL + 50 ADM
- **Effects:** `add_corruption = -1`, `reform_progress_growth = 0.10` for 5 years, `yearly_legitimacy = 1` for 5 years, possible Nobles influence increase.

#### 3. Red Court Inquest
- **Theme:** Magical malpractice purge
- **Costs:** 75 ADM + Mages interaction
- **Effects:** `add_corruption = -1`, small decrease in magical-infamy pressure, possible Mages loyalty loss or influence increase.

**Passive Anti-Corruption:** Certain doctrines and reforms provide `yearly_corruption = -0.05` to `-0.20`.

---

### Disasters

**Status:** CANONICAL

Four thematic disasters represent the collapse of a Verne pillar. Severity scales with how deep the player committed to that pillar.

#### 1. The Shattering of Silver Oaths
- **Type:** Court-dynasty disaster
- **Triggers:** legitimacy < 50, stability < 1, `verne_marriage_court_active = yes`, fewer than 2 royal marriages, weak or absent heir
- **Effects:** `diplomatic_reputation = -2`, `improve_relation_modifier = -0.20`, `prestige = -1`, pretender/faction events
- **Resolution:** legitimacy > 75, stability ≥ 1, secure heir, restore marriages, calm court estates

#### 2. Scandal of the Red Court
- **Type:** Magical corruption disaster
- **Triggers:** high magical infamy with weak legitimacy, repeated risky Red Court decisions, low Mages loyalty or high influence, corruption ≥ 5
- **Effects:** `yearly_corruption = 0.10`, `prestige = -1`, `diplomatic_reputation = -1`, anti-mage/scandal events
- **Resolution:** corruption < 2, reduce magical infamy, stabilize Mages, complete cleansing or paragon-support events

#### 3. The Chapterhouse Feud
- **Type:** Knightly order / rider estate disaster
- **Triggers:** strong order path active, Nobles influence ≥ 80, low legitimacy, two or more order companies founded without stabilizing reforms
- **Effects:** `merc_maintenance_modifier = 0.20`, local unrest in rider provinces, elite order revolts, `diplomatic_reputation = -1`
- **Resolution:** reduce order privilege, legitimacy ≥ 70, crown-control choice events, pay or discipline the orders

#### 4. Overseas Overstretch of the Vernissage
- **Type:** Overseas / exposition overreach disaster
- **Triggers:** `verne_world_network ≥ 6`, loans or severe debt, low income buffer, insufficient maritime/logistical doctrine support
- **Effects:** `trade_efficiency = -0.10`, `advisor_cost = 0.10`, `prestige = -1`, overseas unrest/network stress events
- **Resolution:** restore finances, secure ports/commanderies, reduce debt and corruption, stabilize overseas logistics

**Scaling Rule:** The more Verne commits to a pillar, the more dangerous its collapse. Use extra progress modifiers, stronger penalties, and heavier on-start events when late-state flags are active.

---

### Corinite Integration

**Status:** CANONICAL

Verne already has a Corinite conversion event that flips the capital and adds a Corinite center of reformation. The overhaul should:

- Preserve the capital-centered conversion identity
- Improve surrounding rewards and presentation
- Tie it into the Corinite-imperial route

**Additional Rewards (when embracing Corinite):**
- Unlock Corinite Stewardship Ideas or Apostolic Sea-Lanes Ideas if not yet available
- Unlock a Corinite reform triplet tier earlier
- Grant temporary imperial-faith prestige modifier
- Improve relations with Corinite neighbors

**Fallback:** If capital cannot host the center, fall back to a random valid owned province.

---

### Anti-Corinite / Non-Corinite Content

**Status:** NEEDS_DESIGN (low priority)

A small alternate sub-branch or contingency rewards for refusing Corinite should exist:
- 3-5 side missions
- Alternate rewards on existing missions
- Non-Corinite dynastic/imperial route

This is a low-priority design area.

---

## Active Design Questions

- **Anti-Corinite content:** The design is not fully specified; only the concept exists.
- **Scaling implementation:** Exact numbers for disaster progress modifiers are not defined; they will be determined during coding.

---

## Source Merge Note

This file consolidates "Balancing pressure package", "Anti-corruption package", "Verne-specific disasters", "Corinite conversion and center of reformation", and "Anti-Corinite / non-Corinite content". All triggers, thresholds, and effects are preserved.