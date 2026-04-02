# anbennar_mechanics_ontology

## Purpose
Ground the agent in Anbennar's specific mechanical reality — what makes it NOT vanilla EU4, what DLC gates matter, what the racial/cultural systems do, and how to avoid writing "balanced for vanilla" content.

## Target Versions (Must Stay Pinned)

- **EU4 patch:** `1.37.5`
- **Anbennar release:** `Update 19 — "The Final Empire"`
- **Verne branch:** `chore/verne-10-lane-blueprint` (local)
- **Upstream:** `new-master` branch on GitLab

**If these drift, update `design/upstream-lock.json` immediately.**

## The Core Difference: Anbennar Is Not Vanilla

Anbennar has its own economic balance, racial mechanics, mission density expectations, and DLC dependencies. Writing content as if it were vanilla EU4 will produce wrong-feeling content.

### Key Anbennar Economic Differences
- Development cost: cheaper in many regions vs vanilla
- Tall play: strong incentive via estates and monuments
- Colonisation: modified by expedition mechanics
- Trade: modified by Anbennar-specific trade nodes
- Racial mechanics: active racial bonuses/penalties

## DLC Dependencies

### Required DLC (Anbennar won't function without)
- Art of War, Rights of Man, Common Sense, The Cossacks
- Mandate of Heaven, Dharma, Emperor, Leviathan, Origins

### Recommended DLC
- Third Way, Federalism, Sphere of Influence, Colossus
- Cradle of Civilization

## Racial System (Anbennar-Modified)

Anbennar has modified race/culture groups with special mechanics:
- **Human** (Verne, the Empire, Ghyrenia)
- **Orc** (Grombar, Poxbringers, Ir均衡)
- **Dwarf** (Silverforge, Diamond Lake, Serpantsreach)
- **Elf** (Aelantian, Vineyards, Ibevar)
- **Half-orc** (Grombar vassals, Escanni states)

Racial bonuses/penalties are active — content touching race mechanics must verify against repo.

## Verne-Specific Systems

### Court & Oaths (Lane 1)
- `verne_court_of_silver_oaths_reform` — unique Verne reform
- Monarch power generation modifiers
- Legitimacy/royal authority tracking

### Maritime Empire (Lane 3)
- `verne_heartspier_port` — port/estuary mechanics
- `verne_crimson_wake_fleet` — fleet discount modifiers
- `verne_imperial_sea_court` — trade/institution mechanics

### Dynastic Machine (Lane 4)
- `verne_exalted_dynasty_machine_reform` — dynasty power system
- `verne_dynasty_protected_court` / `verne_dynasty_exalted_lineage` — dynasty modifiers

### Trade & Colonisation (Lane 5)
- `verne_chartered_overseas_companies` — colonial company mechanics
- `verne_overseas_projection` — overseas expansion tracking
- Variable: `verne_overseas_projection_add_1`

### Red Court & Arcane (Lane 6)
- `verne_red_court_advisory` — advisor mechanics
- `verne_dragonwake_profession` / `verne_dragonwake_shock` — profession modifiers

### Military Orders (Lane 7)
- `verne_vernissage_secretariat_reform` — specific reform reference
- `verne_battle_mage_collegium_reform` — mage/military mechanics

### Faith & Apostolic Empire (Lane 8)
- `verne_corinite_stewardship` — faith mechanics
- `verne_pearlescent_concord` — religious unity modifiers

### Industrial Foundries (Lane 9)
- Khenak Foundry — industrialisation mechanics
- `verne_royal_census` — development tracking

### Liliac War Legacy (Lane 10)
- Flag-gated: `liliac_war_truce`, `liliac_war_in_progress`
- `verne_orc_war_band_mobilised` — orc truce mechanics

## Tag Groups for Precedent

When generating content for a new tag, find similar tags in the same group:
- **Verne group** (human, court/dynasty focus): look at Verne's existing missions
- **Escann group** (orc/adventure, colonisation): look at Grombar, Castanor precedents
- **Dwarf group** (fortification, trade): look at Silverforge, Diamond Lake
- **Elf group** (magic, institutions): look at Ibevar, Aelantian

## Expedition / Hold / Empire Systems

Anbennar adds expedition mechanics for colonising wild lands:
- Expedition decisions in `decisions/Verne*.txt`
- Expedition → colonial nation → full integration chain

## What "Anbennar-Balanced" Means

When evaluating generated content:
- Is development cost appropriate for Anbennar's cheaper-dev environment?
- Does it respect racial group mechanics?
- Does it interact correctly with Verne's specific reforms?
- Does it work with the Liliac War flag-gated content?
- Is DLC-availability assumed correctly?

## Repo Verification First

For any Anbennar-specific claim, verify against the checked-out repo:
```
C:\Users\User\Documents\GitHub\My-Anbennar
```
Don't trust wiki alone for mechanic specifics — the repo is primary source.
