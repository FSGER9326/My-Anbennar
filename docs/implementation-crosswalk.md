# Verne Implementation Crosswalk

This file is the bridge layer between:

1. Verne design docs
2. Anbennar implementation patterns (repo maps)
3. EU4 engine/scripting references
4. Verne lore support docs

Use it before coding to decide what should be adapted vs newly invented.

---

## [VERNE-MAG-001] Court Magic Access, Succession, and High-Magic Risk

Design doc: `docs/design/dynasty-and-court.md`

Repo pattern: `docs/repo-maps/magic-systems-reference.md`; `docs/repo-maps/powerful-mage-and-succession-reference.md`; `docs/repo-maps/witch-king-lichdom-war-wizard-infamy-reference.md`

EU4 reference: `docs/references/eu4-wiki/Effects - Europa Universalis 4 Wiki.html`; `docs/references/eu4-wiki/Variables - Europa Universalis 4 Wiki.html`; `docs/references/eu4-wiki/Event modding - Europa Universalis 4 Wiki.html`

Lore doc: `docs/lore/verne-identity-and-court-culture.md`

Status: IMPLEMENTATION_READY

Notes:

- Copy helper-based infamy/succession patterns; do not reinvent variable threshold logic.
- Keep Verne-specific flavor in missions/events/lore naming, not in core magic helpers.

---

## [VERNE-MAG-002] Magic Projects, Lichdom, and War Wizard Branches

Design doc: `docs/design/dynasty-and-court.md`; `docs/design/pressure-disasters-and-corinite.md`

Repo pattern: `docs/repo-maps/magic-projects-reference.md`; `docs/repo-maps/witch-king-lichdom-war-wizard-infamy-reference.md`

EU4 reference: `docs/references/eu4-wiki/Effects - Europa Universalis 4 Wiki.html`; `docs/references/eu4-wiki/Scopes - Europa Universalis 4 Wiki.html`

Lore doc: `docs/lore/verne-identity-and-court-culture.md`

Status: NEEDS_REPO_CHECK

Notes:

- Base project framework is clear and reusable.
- Verify exactly which existing project structures best fit Verne before implementation branch selection.

---

## [VERNE-ART-001] Artificery and Magic Mixed-Mode Integration

Design doc: `docs/design/doctrine-bible.md`; `docs/design/reform-bible.md`

Repo pattern: `docs/repo-maps/artificery-research-and-inventions-reference.md`; `docs/repo-maps/custom-estate-and-privilege-ecosystems-reference.md`

EU4 reference: `docs/references/eu4-wiki/Estate modding - Europa Universalis 4 Wiki.html`; `docs/references/eu4-wiki/Scripted function modding - Europa Universalis 4 Wiki.html`

Lore doc: `docs/lore/verne-identity-and-court-culture.md`

Status: IMPLEMENTATION_READY

Notes:

- Reuse Artificer estate organization and points/invention lifecycle patterns.
- Add Verne flavor through naming and mission gating, not by replacing core artifice helpers.

---

## [VERNE-RAC-001] Racial Administration/Military Compatibility Layer

Design doc: `docs/design/mission-rewrite-spec.md`; `docs/design/open-questions-and-design-lab.md`

Repo pattern: `docs/repo-maps/racial-population-and-military-reference.md`

EU4 reference: `docs/references/eu4-wiki/Triggers - Europa Universalis 4 Wiki.html` (if added to local references) and `docs/references/eu4-wiki/Effects - Europa Universalis 4 Wiki.html`

Lore doc: `docs/lore/verne-religion-rivals-and-overseas-imaginary.md`

Status: NEEDS_REPO_CHECK

Notes:

- Framework exists, but Verne-specific race policy assumptions must be validated against design intent.

---

## [VERNE-ADV-001] Adventure, Overseas Network, and Expedition Identity

Design doc: `docs/design/mission-rewrite-spec.md`; `docs/design/orders-monuments-and-mercs.md`

Repo pattern: `docs/repo-maps/port-of-adventure-system.md`; `docs/repo-maps/network-of-adventure-system.md`; `docs/repo-maps/verne-launch-adventure-system.md`; `docs/repo-maps/adventurer-systems-and-estate-patterns-reference.md`

EU4 reference: `docs/references/eu4-wiki/Province modding - Europa Universalis 4 Wiki.html`; `docs/references/eu4-wiki/Event modding - Europa Universalis 4 Wiki.html`

Lore doc: `docs/lore/verne-religion-rivals-and-overseas-imaginary.md`

Status: IMPLEMENTATION_READY

Notes:

- Verne already has concrete mission-backed patterns; adapt existing helper flow rather than authoring a parallel expedition framework.

---

## [VERNE-GOV-001] Reform Triplets to Government Mechanic Wiring

Design doc: `docs/design/reform-bible.md`

Repo pattern: `docs/repo-maps/custom-government-mechanics-and-gui-patterns-reference.md`

EU4 reference: `docs/references/eu4-wiki/Modding - Europa Universalis 4 Wiki.html`; `docs/references/eu4-wiki/Effects - Europa Universalis 4 Wiki.html`

Lore doc: `docs/lore/verne-identity-and-court-culture.md`

Status: IMPLEMENTATION_READY

Notes:

- Use existing government power/interactions architecture for any new Verne state meters.
- Keep first iteration minimal (one bar + one interaction) before multi-action expansion.

---

## [VERNE-EST-001] Court/Order Institutions as Estate Ecosystems

Design doc: `docs/design/orders-monuments-and-mercs.md`; `docs/design/dynasty-and-court.md`

Repo pattern: `docs/repo-maps/custom-estate-and-privilege-ecosystems-reference.md`; `docs/repo-maps/adventurer-systems-and-estate-patterns-reference.md`

EU4 reference: `docs/references/eu4-wiki/Estate modding - Europa Universalis 4 Wiki.html`

Lore doc: `docs/lore/verne-identity-and-court-culture.md`

Status: NEEDS_REPO_CHECK

Notes:

- Strong reusable patterns exist (organization swaps, invalid cleanup, scaled modifiers).
- Must confirm whether Verne should extend Mages/Adventurers/Artificers vs introducing new custom estate actors.

---

## [VERNE-REL-001] Corinite Integration and Pressure/Disaster Framing

Design doc: `docs/design/pressure-disasters-and-corinite.md`

Repo pattern: `docs/repo-maps/witch-king-lichdom-war-wizard-infamy-reference.md`; `docs/repo-maps/custom-government-mechanics-and-gui-patterns-reference.md`

EU4 reference: `docs/references/eu4-wiki/Disaster modding - Europa Universalis 4 Wiki.html` (if added to local references); `docs/references/eu4-wiki/Event modding - Europa Universalis 4 Wiki.html`

Lore doc: `docs/lore/verne-religion-rivals-and-overseas-imaginary.md`

Status: NEEDS_DESIGN

Notes:

- Pressure scaffolding exists in design, but final implementation path still needs concrete system selection and thresholds.

---

## [VERNE-ORD-001] Wyvern Orders, Mercenary Companies, and Monument Coupling

Design doc: `docs/design/orders-monuments-and-mercs.md`

Repo pattern: `docs/repo-maps/verne-launch-adventure-system.md`; `docs/repo-maps/custom-estate-and-privilege-ecosystems-reference.md` (partial)

EU4 reference: `docs/references/eu4-wiki/Mercenaries modding - Europa Universalis 4 Wiki.html`; `docs/references/eu4-wiki/Modifier modding - Europa Universalis 4 Wiki.html`

Lore doc: `docs/lore/verne-religion-rivals-and-overseas-imaginary.md`

Status: NEEDS_REPO_CHECK

Notes:

- Existing Verne mission content references custom mercenary templates and wyvern-focused military progression.
- A dedicated repo-map deep dive for reusable merc/order frameworks is still pending.

---

## Crosswalk maintenance notes

- If a row is blocked by uncertain implementation details, keep `NEEDS_REPO_CHECK` until a concrete repo-map article resolves it.
- If a row is blocked by unresolved design conflicts, keep `NEEDS_DESIGN` and link the design open-questions entry.
- Always preserve separation of concerns: design intent vs implementation facts vs lore voice.
