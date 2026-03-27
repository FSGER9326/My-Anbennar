# Anbennar Systems Scan Roadmap

This file turns the repo scan into a repeatable documentation plan.

The goal is to build an internal reference library for Anbennar-only systems so future work can adapt existing patterns instead of reinventing them.

## Working Rule

For each system, document:

1. what the system does
2. what files implement it
3. what the player-facing entry points are
4. what flags, variables, and modifiers carry its state
5. what helper effects or triggers centralize the real logic
6. what nation- or race-specific branches already exist
7. what makes it different from vanilla EU4 expectations
8. how it can be safely extended or adapted

## 10-Step Scan Plan

### 1. Map the magic access layer

Output:

- access triggers
- banned-magic branches
- mage-estate versus ruler-mage access

Current status:

- started in [magic-systems-reference.md](./magic-systems-reference.md)

### 2. Map powerful mage generation and succession logic

Output:

- ruler, heir, and consort mage generation
- always-mage branches
- inheritance and dynasty-safe examples

Priority:

- high

### 3. Map study, mana, and school progression

Output:

- mana helpers
- XP helpers
- study pulse events
- school-level progression rules

Priority:

- high

### 4. Map spellbook, patrons, and custom spell lists

Output:

- custom spell list templates
- patron state handling
- race- or tag-specific spellbook branches

Priority:

- high

### 5. Map magic projects, lichdom, war wizards, and witch-kings

Output:

- project framework
- project spillover into unrelated content
- war wizard and lich conversion patterns
- witch-king escalation structure

Priority:

- high

### 6. Map racial population, tolerance, administration, and military systems

Output:

- racial UI layer
- tolerance helpers
- administration switching
- military tech switching

Priority:

- high

### 7. Map artificery research, inventions, and mixed-mode magic interaction

Output:

- artifice points and capacity
- estate hooks
- invention lifecycle
- mixed magic-artificery coexistence patterns

Priority:

- high

### 8. Map adventurer systems and other major custom estates

Output:

- adventurer unity
- adventurer estate content
- mage and artificer estate tie-ins
- patterns worth copying for institution-style mechanics

Priority:

- medium

### 9. Map reusable government mechanics and custom GUI subsystems

Output:

- government power mechanics worth reusing
- province and country custom button patterns
- GUI plus helper plus event architecture map

Priority:

- medium

### 10. Build the adaptation library

Output:

- masterlist of do-not-reinvent systems
- per-system notes on what is easiest to adapt
- examples for nation-specific, race-specific, and project-specific extensions

Priority:

- high

## Current First-Wave Deliverables

Already documented:

- [port-of-adventure-system.md](./port-of-adventure-system.md)
- [verne-launch-adventure-system.md](./verne-launch-adventure-system.md)
- [network-of-adventure-system.md](./network-of-adventure-system.md)
- [magic-systems-reference.md](./magic-systems-reference.md)
- [powerful-mage-and-succession-reference.md](./powerful-mage-and-succession-reference.md)
- [magic-projects-reference.md](./magic-projects-reference.md)
- [racial-population-and-military-reference.md](./racial-population-and-military-reference.md)
- [artificery-research-and-inventions-reference.md](./artificery-research-and-inventions-reference.md)
- [adventurer-systems-and-estate-patterns-reference.md](./adventurer-systems-and-estate-patterns-reference.md)
- [anbennar-non-vanilla-systems-overview.md](./anbennar-non-vanilla-systems-overview.md)
- [anbennar-systems-master-index.md](./anbennar-systems-master-index.md)
- [witch-king-lichdom-war-wizard-infamy-reference.md](./witch-king-lichdom-war-wizard-infamy-reference.md)
- [custom-government-mechanics-and-gui-patterns-reference.md](./custom-government-mechanics-and-gui-patterns-reference.md)
- [custom-estate-and-privilege-ecosystems-reference.md](./custom-estate-and-privilege-ecosystems-reference.md)
- [government-mechanic-activation-map-by-reform-reference.md](./government-mechanic-activation-map-by-reform-reference.md)
- [verne-wyvern-orders-mercs-and-monuments-reference.md](./verne-wyvern-orders-mercs-and-monuments-reference.md)
- [verne-wyvernrider-estate-ecosystem-reference.md](./verne-wyvernrider-estate-ecosystem-reference.md)

Best next articles:

1. Race- and religion-specific framework comparison matrix
2. Artificery-magic crossover and nation-specific invention usage
3. Verne monument object-ID parity check for design names
4. Full reform-to-mechanic exhaustive matrix (all custom IDs)

Recently completed in this pass:

- [witch-king-lichdom-war-wizard-infamy-reference.md](./witch-king-lichdom-war-wizard-infamy-reference.md)
- [custom-government-mechanics-and-gui-patterns-reference.md](./custom-government-mechanics-and-gui-patterns-reference.md)
- [custom-estate-and-privilege-ecosystems-reference.md](./custom-estate-and-privilege-ecosystems-reference.md)
- [government-mechanic-activation-map-by-reform-reference.md](./government-mechanic-activation-map-by-reform-reference.md)
- [verne-wyvern-orders-mercs-and-monuments-reference.md](./verne-wyvern-orders-mercs-and-monuments-reference.md)
- [verne-wyvernrider-estate-ecosystem-reference.md](./verne-wyvernrider-estate-ecosystem-reference.md)

## Documentation Standard

Each future article should include:

- quick verdict
- core files table
- main objects table when useful
- step-by-step system flow
- at least two real code examples
- notes on how the implementation differs from a simpler vanilla-style approach
- safe extension or adaptation notes


## Coordination rule for index files

When adding a new repo-map article, update these three files in the same commit:

1. `docs/repo-maps/README.md`
2. `docs/repo-maps/anbennar-systems-master-index.md`
3. `docs/repo-maps/anbennar-systems-scan-roadmap.md`

This keeps the documentation registry consistent and avoids repeat conflict-only follow-up commits.
