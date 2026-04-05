# EU4 Mod Inspiration — Scouting Log

A living reference of interesting mechanics, implementation patterns, and creative mod work from the community. Focused on implementation details relevant to the Anbennar/Verne project.

---

## Navigation

- [Trade & Economy](#trade--economy)
- [Religion & Faith](#religion--faith)
- [Colonisation & Exploration](#colonisation--exploration)
- [Government & Mechanics](#government--mechanics)
- [Mission Trees & Narrative](#mission-trees--narrative)
- [Scripted Triggers & Flags](#scripted-triggers--flags)

---

## Trade & Economy

*(No entries yet — PRs welcome)*

---

## Religion & Faith

### Gods and Kings — Religious Schools
- **Source:** https://forum.paradoxplaza.com/forum/threads/europa-universalis-iv-mod-spotlight-gods-and-kings-2024.1625764/
- **What it does:** Adds a "religious schools" mechanic to nearly every religious group in the game. Each school functions as a sub-school within the parent faith, offering unique bonuses, mechanics, or flavour depending on which school a nation follows. Covers Catholic traditions, Buddhist schools, Islamic branches, and more.
- **Implementation notes:** Religious schools appear as a selectable/visible mechanic on the religion view. The mechanic layers on top of the base religion system, adding school-specific modifiers or interactions. Uses event-driven mechanics for school-specific behaviours (e.g., Maitreyan Authority mechanic for the Maitreyan Buddhist faith, Apostolic Poverty shared between Fraticelli/Wycliffite/Adamites/Waldensian). The mod also adds new trade goods (Rice, Saffron, Cheese) and a Goods Upgrade building system — e.g., Winery building converts a Rice province into a Rice Wine province, changing its trade value profile.
- **Relevance:** `religion` `school-system` `goods-upgrade` `flavour` `mod-architecture`
- **Verne fit:** Verne has no planned religion overhaul, but the **goods upgrade / trade good transformation** pattern (Winery → Rice Wine) is directly applicable to Verne's planned trade good differentiation for Vereneser, Verenmoor, etc. The religious schools system demonstrates how to layer sub-identities onto an existing faith without a full religion rewrite — useful if Verne ever wanted to distinguish Verenism sects or temple traditions.

### Gods and Kings — Qizilbashi Guru Mechanic Rework
- **Source:** https://forum.paradoxplaza.com/forum/threads/europa-universalis-iv-mod-spotlight-gods-and-kings-2024.1625764/
- **What it does:** Reworks the old Guru mechanic for the Qizilbashi faith (a Safavid-inspired Turkic Muslim sect). The rework gives the mechanic new interactions, decisions, or events that make it more engaging than vanilla's guru/pantheon system.
- **Implementation notes:** Likely uses a combination of country modifiers, scoped events, and a custom mechanic variable tracked per country. The Guru mechanic may now have branching choices or a piety-like progression.
- **Relevance:** `religion` `mechanic-rework` `guru` `events`
- **Verne fit:** Lower priority for Verne, but demonstrates how to take a vanilla mechanic (Guru) and give it more depth via targeted events and mechanic variables.

---

## Colonisation & Exploration

### Beyond the Cape — Settler Pool
- **Source:** https://forum.paradoxplaza.com/forum/threads/europa-universalis-iv-mod-spotlight-beyond-the-cape-2023.1598454/
- **What it does:** Replaces the flat per-colony settler model with a shared **Settler Pool** available to every country with a colonist. Max pool size is calculated from total development + number of state provinces. Each active colony deducts 1,000 settlers from the pool; the pool replenishes when the colony finishes. A modifier based on pool utilisation percentage (boost or penalty) affects all colonisation speed.
- **Implementation notes:** Likely uses country-scoped variables (`settler_pool`, `max_settler_pool`) calculated from development and state count. A modifier applies to colonisation speed based on the ratio of free settlers. Decision likely used to view/adjust pool. This is a targeted vanilla-change (no new UI, but introduces a new mechanic layer on top of existing colonisation).
- **Relevance:** `colonisation` `variable-based-mechanic` `tradeoff-design` `balance`
- **Verne fit:** Verne colonisation is not a core focus, but the **settler pool as a shared resource** pattern is a clean example of converting a per-colony stat into a strategic resource with opportunity cost. Could inspire a Verne-specific mechanic if colonisation ever becomes relevant.

### Beyond the Cape — Columbus Event & Tordesillas Treaty
- **Source:** https://forum.paradoxplaza.com/forum/threads/europa-universalis-iv-mod-spotlight-beyond-the-cape-2023.1598454/
- **What it does:** Portugal receives the Columbus proposal event before Castile if conditions are met (Exploration ideas + year 1488 + no Cape of Good Hope discovery). Rejecting transfers the event to Castile. If Castile gets Columbus, Portugal can contest discoveries, triggering a Tordesillas treaty enforcement event — splitting colonial rights by region (Portugal: Africa/Asia/Brazil, Castile: Americas). Treaty can be revoked via decision with consequences. Renames vanilla's Tordesillas to Inter Caetera.
- **Implementation notes:** Chain of scoped events with conditional triggers based on country tag, ideas, year, and province discovery flags. Treaty enforcement likely applies a modifier or special colonial region restriction via effects. The renaming of the vanilla decision/agreement shows how to override base-game named mechanics.
- **Relevance:** `events` `colonial-rights` `diplomatic-agreement` `flavour-portugal`
- **Verne fit:** Lower direct relevance but an excellent example of **conditional event chains** that change the entire map state (colonial partitioning) without a full system rewrite.

### Beyond the Cape — Trade Winds / Naval Mechanics Pass
- **Source:** https://forum.paradoxplaza.com/forum/threads/europa-universalis-iv-mod-spotlight-beyond-the-cape-2023.1598454/
- **What it does:** Trade winds given greater mechanical impact. Exploration ideas rebalanced so Quest for the New World is removed from Portugal's idea set. Access to open sea tiles gated behind diplomatic tech 9 for countries with Exploration ideas.
- **Implementation notes:** Likely uses modified ideas files (removing/adjusting trigger conditions) and trade wind modifier adjustments. No new UI — purely rebalancing via idea changes and modifier tweaks.
- **Relevance:** `naval` `trade` `exploration` `balance`
- **Verne fit:** Verne has no planned naval overhaul, but the **removing/opening exploration access via tech gates** pattern is useful design for Verne's planned institution spread mechanics.

### Beyond the Cape — Slavers Estate
- **Source:** https://forum.paradoxplaza.com/forum/threads/europa-universalis-iv-mod-spotlight-beyond-the-cape-2023.1598454/
- **What it does:** Adds a new **Slaters Estate** unlocked when a European country has a presence in West Africa and the New World simultaneously. Comes with unique privileges, agendas, events, and a disaster.
- **Implementation notes:** Estate definition with `estate_privileges`, `estate_agendas`, `estate_disasters` — the full estate framework. Unlocked via country trigger (owns province in West Africa AND owns province in New World colonial region).
- **Relevance:** `estates` `new-estate` `slave-trade` `disaster` `privileges`
- **Verne fit:** Estate-based design is well-understood in Anbennar. Demonstrates the **conditional unlock pattern** (dual-region presence requirement) — could be used for Verne's estuaries if a special estate is ever warranted.

---

## Government & Mechanics

### Government Mechanics Expanded — Persia Government Ability
- **Source:** https://steamcommunity.com/sharedfiles/filedetails/?id=2970604652
- **What it does:** Adds unique government reforms and associated government abilities to multiple nations. For Persia: a unique government ability unlocked through a tier 2 unique reform. For France (feudal and absolutist variants), Netherlands (Dutch Republic with Staatse leger), and Japan (Unified Shogunate mechanic after uniting Japan via decision).
- **Implementation notes:** Uses the government reform tree to attach mechanics via `government_action` or equivalent ability triggers. The Persia mechanic is specifically noted as similar in spirit to "The King of Kings" DLC. Mod explicitly conflicts with other government reform mods — shows that government reform is a high-collision area. New UI introduced for Persia's mechanic.
- **Relevance:** `government-reforms` `government-abilities` `persia` `japan` `france` `netherlands`
- **Verne fit:** **High relevance.** Verne is actively designing government mechanics. The pattern of "tier 2 unique reform that unlocks a special ability" maps directly to how Verne's Verenithm mechanics could be structured. The Japan mechanic (unified shogunate post-unification decision) is a good model for "post-unification state change" — applicable if Verne ever addresses Veren unification.

### Atlas Novum — HRE Great Power Ascension by Chance
- **Source:** https://forum.paradoxplaza.com/forum/threads/mod-spotlight-atlas-novum.1704392/
- **What it does:** In the Atlas Novum HRE rework, ascension to Great Power status is partially stochastic — "up to chance as much as planning and politicking." Adds unpredictability to the imperial politics system.
- **Implementation notes:** Likely uses a weighted random check alongside the standard power-score calculation for imperial triggering. The randomness may be gated behind reforms or conditional triggers.
- **Relevance:** `hre` `great-power` `randomness` `politics`
- **Verne fit:** Lower direct relevance for Verne (HRE is not a Verne system), but the **randomness layer on top of a deterministic mechanic** is a good reference if Verne ever wants subtle unpredictability in Verenithm civic outcomes.

### Atlas Novum — River Navigation & Canalisation
- **Source:** https://forum.paradoxplaza.com/forum/threads/mod-spotlight-atlas-novum.1704392/
- **What it:** Adds historically navigable rivers as sea tiles (Rhine, Danube, Don, Volga, Congo, Zambezi, Ganges, Yangtze, Columbia, Mississippi, Laurent, Hudson, Amazon, Paraná). Some rivers require expensive canalisation projects to fully access and navigate.
- **Implementation notes:** Mapwork — defines river provinces as navigable sea tiles and adds canalisation decision/building requirements. Likely uses `is_navigable_river` or similar province flags with building requirements for full access.
- **Relevance:** `mapwork` `naval` `river` `canal` `trade`
- **Verne fit:** River navigation is not on Verne's roadmap, but the **canalisation project as a gated-access mechanic** pattern (expensive, requires decision, unlocks new areas) could inspire similar infrastructure mechanics for Verenmoor or coastal Verenneser access.

---

## Mission Trees & Narrative

### Gods and Kings — Mali "Golden Empire" Mission Tree
- **Source:** https://forum.paradoxplaza.com/forum/threads/europa-universalis-iv-mod-spotlight-gods-and-kings-2024.1625764/
- **What it does:** Mali's mission tree supports its new colonial destiny — discovering the New World via the Columbus-equivalent event and establishing a colonial empire alongside European powers. Integrates local official and ruler integration mechanics.
- **Implementation notes:** Standard mission tree with events and rewards. Colonial integration likely uses existing subject-mechanic hooks with flavour events layered on top.
- **Relevance:** `mission-tree` `colonial` `africa` `flavour`
- **Verne fit:** Mission tree design reference only — not directly applicable but useful as a quality benchmark.

### Gods and Kings — Maitreyan Authority Mechanic
- **Source:** https://forum.paradoxplaza.com/forum/threads/europa-universalis-iv-mod-spotlight-gods-and-kings-2024.1625764/
- **What it does:** A new, hidden-reward mechanic for the Maitreyan Buddhist faith. Players discover the mechanic's rewards organically through play rather than via explicit tutorial. Uses an Authority-style track with escalating rewards tied to faith activities.
- **Implementation notes:** Likely uses a faith-scoped variable (e.g., `maitreyan_authority`) incremented by specific actions (conversions, provinces owned, religious events). Rewards granted at threshold values. The "hidden rewards" design is primarily event-driven with discoverable mechanics.
- **Relevance:** `religion` `hidden-rewards` `authority-track` `faith-mechanic`
- **Verne fit:** **Interesting reference for Verenithm design.** A similar "discover through play" mechanic could make Verenithm feel less like a checklist and more like an emergent civic identity. However, Verne currently prioritises transparent, well-documented systems.

### Atlas Novum — Narrative "Fractured Europe" Setup
- **Source:** https://forum.paradoxplaza.com/forum/threads/mod-spotlight-atlas-novum.1704392/
- **What it does:** Europe is set up as deeply fragmented: Iberia starts with subject co-kingdoms requiring integration before expansion; France divided by fiefdoms mid-hundred-years-war; Italy dominated by small states; Kalmar Union intact; Poland-Lithuania dominant in the East; Balkans under Turkish pressure without a bulwark.
- **Implementation notes:** Starting province ownership and subject state setup in common files. Each political condition represented through historical starting tag ownership, culture, and religion assignments.
- **Relevance:** `mapwork` `starting-setup` `flavour` `political-narrative`
- **Verne fit:** Demonstrates how starting conditions encode narrative. Verne's Veren region already has strong starting setup for narrative. Useful for ensuring Verenmoor/Verenneser starting fragmentation is implemented cleanly.

---

## Scripted Triggers & Flags

### Deep Research (2026-04-05) — Undefined Scripted Triggers: The Silent Mission Breaker
- **Source:** ChatGPT Deep Research — EU4 modding investigation
- **Problem documented:** 6 custom scripted triggers used in Verne mission files but never defined → EU4 treats them as always `false`, making missions permanently unavailable.
- **Root cause confirmed:** EU4 engine rule — undefined scripted triggers always return false.
- **File location for definitions:** `/common/scripted_triggers/<your_file>.txt` (e.g., `verne_overhaul_triggers.txt`)
- **Syntax pattern:**
  ```txt
  verne_overhaul_akasik_access_ready = {
      # trigger logic here
  }
  ```
  Used in missions as: `trigger = { verne_overhaul_akasik_access_ready = yes }`
- **Trigger patterns for Verne's missing triggers:**
  - `verne_overhaul_in_search_expedition_capacity` → check colonists, treasury, manpower, exhaustion modifier, or custom variables
  - `verne_overhaul_in_search_network_or_monument_route` → OR of trade node presence, great projects, or custom flags
  - `verne_overhaul_in_search_subject_projection_route` → OR of colonial nations, low-liberty-desire subjects, or regional subject capitals
  - `verne_overhaul_early_akasik_access_route` → OR of ruler stats, idea groups, or special modifiers
  - `verne_overhaul_laments_regatta_anchor_state_ready` → coastal province with development threshold and dock building
  - `verne_overhaul_akasik_access_ready` → institution + stability + idea group checks
- **Wyvern nest flag fix:** `set_country_flag = verne_wyvern_nest_initialized` must fire in an event (e.g., `verne.100`) that triggers when the wyvern nest is established. The flag should be set in `immediate = {}` block.
- **Modular trigger design best practice:** Keep triggers small and composable. Use OR-combinators to layer routes (network route OR subject projection route) rather than embedding all logic in one trigger.
- **Reference mods:** Anbennar itself (racial mechanics, artificery), Europa Expanded (clean modular scripting, strong separation of triggers/effects/missions), Missions Expanded (`*_available`, `*_completed`, `*_possible` naming conventions)
- **Debugging:** Check `error.log` for `Unknown trigger type: verne_overhaul_...` — this confirms the trigger is not being found.
- **Relevance:** **Critical for Verne.** The 6 undefined triggers are blocking core adventure/maritime mission chains. Creating the trigger definitions is the highest-priority fix identified in the 2026-04-05 deep audit.

---

## Scouting Log

| Date | Finds | Notes |
|------|-------|-------|
| 2026-04-03 | 10 | First scout pass. Covered: Gods and Kings (religious schools, goods upgrade, Maitreyan authority, Qizilbashi rework), Beyond the Cape (settler pool, Columbus/Tordesillas event chain, trade winds, Slavers estate), Government Mechanics Expanded (Persia/Japan/France government abilities), Atlas Novum (HRE randomness, river navigation). Web searches hit bot-detection after initial results; supplemented via web_fetch on known Paradox forum threads. |
| 2026-04-05 | 6+ | Deep research on undefined scripted triggers. Confirmed EU4 engine rule (undefined = false). Mapped 6 missing trigger names to canonical EU4 trigger patterns. Identified wyvern nest flag fix. Recommended modular trigger architecture and reference mods. Critical for Verne mission availability. |
