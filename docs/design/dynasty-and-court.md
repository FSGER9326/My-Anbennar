# Dynasty and Court

This document covers dynastic continuity, heir shaping, marriage-court systems, advisor archetypes, and associated decisions/events.

---

## Canonical Systems

### Dynastic Continuity

**Status:** CANONICAL

Verne should maintain the síl Verne dynasty and use royal marriages effectively. Three progressive stages provide this:

| Stage | Unlock | Effects |
|-------|--------|---------|
| **Protected Lineage** | Old Friends, Old Rivals or Court of Silver Oaths | `heir_chance = 0.25`<br>`monthly_heir_claim_increase = 0.05`<br>Enables mild `on_new_heir` dynasty correction weighting |
| **Exalted Lineage** | The Kingdom of Verne, Hall of Silver Oaths tier 2+, stronger dynastic decisions | `yearly_legitimacy = 1`<br>Stronger dynasty-correction event<br>Increased chance for Blood of the Wyvern-Kings |
| **Marriage Court of Verne** | Old Friends, Old Rivals followup, Raise a Court of Silver Sails, Imperial Sea Court path | `diplomatic_relations = 1`<br>Stronger royal-marriage acceptance/prestige/legitimacy support via modifiers and events |

**Implementation:** Use `define_heir = { dynasty = ROOT ... }` in scripted events, and an `on_new_heir` event that corrects dynasty if needed when the appropriate flags are set.

---

### Heir Shaping Decisions

**Status:** CANONICAL

Five major dynastic decisions, each with cooldowns and weighted outcomes.

#### 1. Train the Heir in the Red Court
- **Cadence:** every 5 years
- **Costs:** gold + ADM or MIL + Mages influence/loyalty
- **Outcome families:**
  - Strong success: heir gains +1 ADM and +1 MIL (or +2 MIL), chance for mage_personality, chance for evocation advancement, `+1 verne_dynastic_magic_machine`
  - Moderate success: +1 to one stat, prestige gain, Mages loyalty gain
  - Mixed outcome: no stat gain, temporary court-mage modifier
  - Failure: prestige loss, Mages influence rise

#### 2. Induct the Heir into the Dragonwake
- **Cadence:** every 5 years (separate cooldown)
- **Costs:** gold + MIL + Nobles loyalty/influence
- **Outcome families:**
  - Strong success: heir gains +2 MIL (or +1 MIL/+1 ADM), chance for Blood of the Wyvern-Kings, Nobles loyalty, `+1 verne_dynastic_magic_machine` (if heir is mage-capable or Red Court exists)
  - Moderate success: +1 MIL, prestige, army tradition small
  - Mixed outcome: heir claim improved, no stat gain, future martial event weighting
  - Failure: heir injured, prestige loss, Nobles gain influence

#### 3. Present the Heir at the Vernissage
- **Cadence:** 8-10 years
- **Costs:** gold + DIP
- **Outcome families:**
  - Strong success: heir claim rises, prestige, chance for +1 ADM or +1 DIP, improve-relations modifier
  - Moderate success: prestige and legitimacy only, relations boost
  - Failure: prestige loss

#### 4. Drill the Battle-Mage Court
- **Cadence:** every 8 years
- **Costs:** gold + MIL + ADM + Mages interaction
- **Outcome families:**
  - Strong success: ruler gains evocation advancement, chance for mage_personality, temporary war-mage country modifier, `+1 verne_dynastic_magic_machine`
  - Moderate success: temporary army-quality modifier, Mages loyalty
  - Failure: ruler fatigue, prestige loss, Mages influence

#### 5. Elevate a Storm-Crowned Prince
- **Cadence:** rare late-game
- **Costs:** high gold + ADM + MIL + monument/reform prerequisites
- **Outcome families:**
  - Strong success: heir gains large stat improvement, chance for both Blood of the Wyvern-Kings and mage_personality, evocation advancement, large prestige/legitimacy
  - Risk case: expensive with partial gain, succession instability flavor if pushed recklessly

---

### Royal Marriage Support

**Status:** CANONICAL

Verne missions should reward maintaining royal marriages:
- Early mission reward for 2+ royal marriages
- Midgame mission reward for 4+ royal marriages
- Rewards for marriage ties to imperial princes or major sea powers

---

### Advisor Archetypes

**Status:** CANONICAL

Verne should attract specialized advisors through decisions/events, not just generic discounts.

| Archetype | Theme | Creation Method | Example Effects (inherent or via events) |
|-----------|-------|-----------------|-----------------------------------------|
| **Red Court Magister** | Mage-state administration, magical legitimacy, heir tutoring | Decision/event: `define_advisor` with type = scholar or statesman, skill 2-3, cost discount | Supports magical infamy control, heir/ruler training |
| **Grand Admiral of the Wake** | Fleet prestige, ship trade power, naval tradition | Decision/event: `define_advisor` with type = naval_reformer, skill 2-3 | Boosts light ship power, naval tradition |
| **Vernissage Curator** | Prestige, institution spread, exposition rewards | Decision/event: `define_advisor` with type = artist or natural_scientist, skill 2-3 | Increases institution spread, artifact rewards |
| **Khenak Master Founder** | Artillery economy, military industry | Decision/event: `define_advisor` with type = commandant or treasurer, skill 2-3 | Reduces artillery cost, improves production efficiency |

**Implementation:** Use scripted effects like `verne_spawn_red_court_magister_effect` in decisions or mission rewards.

---

## Active Design Questions

None – all systems are fully specified.

---

## Source Merge Note

This file consolidates the "Dynastic decision package", "Dynastic permanence and royal-marriage package", and "Advisor package" sections. All cadences, costs, and outcome families are preserved.