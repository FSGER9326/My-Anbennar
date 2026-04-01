# Mod Inspiration Bank

Curated collection of interesting modded mechanics, implementations, and creative ideas from the EU4 modding community.
Use this when looking for inspiration for Verne or other mod projects.

Last updated: 2026-03-31

---

## How to Use This File

When working on a modding task, search this file for relevant mechanics:
- "What have other mods done for naval trade?" → Check Trade section
- "How did someone implement mage advisors?" → Check Advisor/Magic section
- "Any creative succession mechanics?" → Check Succession section

When the self-improving-agent discovers new interesting implementations during web searches, log them here.

---

## Section Index
- [Trade & Economy](#trade--economy)
- [Naval & Maritime](#naval--maritime)
- [Succession & Legitimacy](#succession--legitimacy)
- [Magic & Religion](#magic--religion)
- [Mission Trees & Lanes](#mission-trees--lanes)
- [Government & Estates](#government--estates)
- [Warfare & Military](#warfare--military)
- [Colonisation & Expansion](#colonisation--expansion)
- [Diplomacy & Subjects](#diplomacy--subjects)
- [UI & Quality of Life](#ui--quality-of-life)

---

## Trade & Economy

### Reworked Trade Routes — Historical Trade Path Simulation
- **Source:** Steam Workshop (id=1472242598), originally for Beyond Typus
- **What it does:** Adds numerous new trade routes and removes some vanilla ones in favor of more complex paths, better simulating historical trade while improving gameplay balance.
- **Implementation notes:** Edits `common/tradenodes/00_tradenodes.txt` — adds additional `path` entries between nodes, can add inland routes that vanilla skips.
- **Relevance:** trade, economy, geography
- **Verne fit:** Could simulate Verne maritime trade lanes — coastal routes between court-city ports, arcane commodity flows, or oath-bound trade monopolies between vassal harbors.

### Trade Expeditions — Active Naval Trade Missions
- **Source:** Paradox Forums — Naval/Trade Overhaul proposal (forum.paradoxplaza.com/threads/1405253)
- **What it does:** Players send fleets on timed trade missions to distant nodes, loading goods from controlled provinces. Profit scales with distance and rarity of goods. Special variants include Triangle Trade, Treasure Fleets, and Northeast Passage expeditions.
- **Implementation notes:** Uses exploration-mission-style fleet mechanics gated by trade range. Investment cost scales with ship count. Cooldown of 2–4 years prevents spam. Could use events with `fleet_scope` and timed modifiers.
- **Relevance:** trade, naval, exploration, economy
- **Verne fit:** **Excellent fit.** Verne's maritime identity could use "Oath-Bound Trade Expeditions" — knightly orders or merchant houses sending fleets on flavoured missions. Tie profit to oaths held/broken, court favor, or arcane navigation.

### Change Trade Goods — Province Trade Good Events
- **Source:** Steam Workshop (id=1299899721)
- **What it does:** 50+ events allowing players to influence/change trade goods in provinces, adding agency to the economic system.
- **Implementation notes:** Province-scope events with MTTH triggers checking trade goods, neighboring goods, development. Uses `change_trade_goods` effect.
- **Relevance:** economy, trade goods
- **Verne fit:** Verne could have arcane commodity events — a court decision to cultivate magical reagents, rare woods for shipbuilding, or alchemical ingredients.

---

## Naval & Maritime

### Naval & Maritime Ideas Redone — Idea Group Overhaul
- **Source:** Steam Workshop (id=1552329306)
- **What it does:** Reworks Naval and Maritime idea groups to be competitive with other groups, adding more impactful bonuses and unique naval abilities.
- **Implementation notes:** Edits `common/ideas/` files, rebalances existing naval bonuses, adds new ones like ship durability, sailor recovery, and naval leader bonuses.
- **Relevance:** naval, military ideas
- **Verne fit:** Reference for making Verne's naval idea groups feel impactful rather than afterthoughts.

### Naval/Trade Overhaul — Protect Trade + Privateering Rework
- **Source:** Paradox Forums (forum.paradoxplaza.com/threads/1405253)
- **What it does:** Light ships provide % trade protection; having trade protection triggers periodic reward events (ducats from merchants, prosperity, relation bonuses). Privateering damages prosperity, relations, and goods produced in uncontrolled provinces. Heavy ships can also privateer at reduced efficiency.
- **Implementation notes:** Could use `on_yearly_pulse` events checking `num_of_light_ship` in trade nodes, then fire province-scope or country-scope reward/punishment events. Trade power % thresholds gate which events fire.
- **Relevance:** naval, trade, warfare
- **Verne fit:** **Strong fit.** Verne's knightly maritime orders could "protect trade" as an oath obligation — breaking the oath (raiding instead) triggers court intrigue events. Reward chain for maintaining naval supremacy in Verne trade zones.

---

## Succession & Legitimacy

_No entries yet._

---

## Magic & Religion

### Gods and Kings — Custom Religious Mechanics
- **Source:** Paradox Forums — Mod Spotlight 2024 (forum.paradoxplaza.com/threads/1625764)
- **What it does:** Adds dozens of new religions with unique mechanics per faith. Examples: Qizilbashi uses reworked Guru mechanic; Shinbutsu reworks Isolationism for syncretism; Maitreya has entirely new "Maitreyan Authority" mechanic granting discovery-based rewards; Fraticelli shares "Apostolic Poverty" mechanic across multiple heresies.
- **Implementation notes:** Custom mechanics via `government_mechanics/` or scripted modifiers + events. Maitreyan Authority likely uses a hidden variable tracked via country modifiers, with event chains that unlock rewards at thresholds. Apostolic Poverty shared across religions via common mechanic name.
- **Relevance:** religion, custom mechanics, event chains
- **Verne fit:** **Excellent fit.** Verne's arcane identity could use a similar "Arcane Authority" or "Thaumic Resonance" mechanic — a tracked meter that unlocks rewards as the player invests in magical institutions. Different "schools" of magic (court wizards, sea-mages, oath-weavers) could share a common mechanic framework with flavour-specific events.

### Anbennar Racial System — Administration & Military Per Race
- **Source:** Anbennar (wiki.anbennar.org, eu4.paradoxwikis.com/Anbennar/Races)
- **What it does:** Each race (Dwarf, Elf, Orc, Goblin, Centaur, etc.) gets distinct administration bonuses/maluses and military bonuses/maluses that fundamentally change gameplay strategy. Elves have discipline +10% but -50% manpower recovery. Dwarves get production efficiency +20% but -10% movement speed. Each race plays completely differently.
- **Implementation notes:** Uses `add_country_modifier` with racial tags, likely triggered by culture/culture group. Admin and military mechanics are separate modifier layers. Combined with unique government reforms per race, racial population events, and race-specific mission trees.
- **Relevance:** custom mechanics, government, military, flavour
- **Verne fit:** Verne could adapt this for **dynastic houses or knightly orders** — each major house gets distinct stat profiles (e.g., House X = naval focus with trade penalties; House Y = arcane power with military weakness). Implemented as government reform modifiers or triggered country modifiers based on tag/dynasty.

---

## Mission Trees & Lanes

### Europa Expanded — Custom Macrobuilder + Achievement System
- **Source:** Paradox Forums — Mod Spotlight (forum.paradoxplaza.com/threads/1678483)
- **What it does:** Adds a custom macrobuilder (Shift+B) for QoL features like upgrade-all-buildings. Also implements a faux achievement system using reworked triggered modifiers with scripted UI page buttons and Steam-style popup notifications.
- **Implementation notes:** Custom macrobuilder uses `scripted_gui` system. Achievement display uses `triggered_modifiers` reworked via `scripted_ui` with pagination. Popup notifications use `country_event` with custom event pictures.
- **Relevance:** UI, QoL, mission rewards
- **Verne fit:** A "Court Decisions" macrobuilder could consolidate Verne-specific actions (oath management, arcane research, fleet orders) into one UI. Achievement-style "Oath Milestones" could track player progress through the mod.

### Europa Expanded — Game Rules System
- **Source:** Paradox Forums — Mod Spotlight (forum.paradoxplaza.com/threads/1678483)
- **What it does:** V3/CK3-inspired game rules screen letting players configure campaign behavior: which mission trees AI picks, event probability toggles, nation spawning chances, etc.
- **Implementation notes:** Uses `game_rules` system introduced in 1.37. Custom rules defined in configuration files, with UI built via scripted_gui.
- **Relevance:** UI, customization, replayability
- **Verne fit:** Let players configure Verne-specific campaign rules: "Oath Strictness" (harsh vs forgiving oath mechanics), "Arcane Prevalence" (how much magic affects gameplay), "Maritime Focus" (naval vs land balance toggle).

---

## Government & Estates

### Government Mechanics Expanded — Per-Nation Government Abilities
- **Source:** Steam Workshop (id=2970604652)
- **What it does:** Adds unique government mechanics (abilities, interactions, UI bars) to specific nations: Ming gets "Imperial Agency," Japan gets "Unified Shogunate," France gets feudal/absolutist mechanics, Netherlands gets Dutch Republic + Staatse Leger mechanics. Three Persia mechanics. Clean implementation, minimal conflicts.
- **Implementation notes:** Uses `common/government_mechanics/` (scriptable since 1.35). Each mechanic defines powers, interactions, range modifiers, and scaled modifiers. Unlocked via unique government reforms. Custom UI with icons, backgrounds, bars.
- **Relevance:** government, estates, UI, custom mechanics
- **Verne fit:** **Directly applicable.** Verne could have a "Court Influence" government mechanic with a tracked bar (crown vs. estate power). Interactions could include: "Summon the Oath Council," "Declare Arcane Emergency," "Reform Maritime Law." Each interaction costs/places a resource and has cooldowns.

### Estates/Corruption Rework — Tied Mechanics
- **Source:** Steam Workshop (id=1652338457)
- **What it does:** Reworks corruption to interact meaningfully with estates rather than being a flat money sink. Ties estate loyalty/influence to corruption levels, making the estate system feel interconnected.
- **Implementation notes:** Edits estate definitions and adds events linking `corruption` variable to estate influence changes. Uses `on_yearly_pulse` events checking corruption thresholds.
- **Relevance:** estates, government, corruption
- **Verne fit:** Verne's estates (merchant houses, knightly orders, arcane guilds) could have corruption tied to oath-breaking — breaking oaths increases "dishonor" which feeds into estate loyalty decay and corruption events.

### Elder Scrolls Universalis — Estate Privileges Overhaul
- **Source:** Reddit r/EU4mods (reddit.com/r/EU4mods/1d6f0ef)
- **What it does:** Complete overhaul of estate privileges for TES universe factions, adding fantasy-specific privileges that reflect magical guilds, warrior orders, and political factions.
- **Implementation notes:** Extends `common/estate_privileges/` with new privilege definitions tied to TES factions. Each privilege has specific crownland costs, estate influence, and triggered effects.
- **Relevance:** estates, government, fantasy
- **Verne fit:** Template for Verne estate privileges — "Arcane Research Mandate" (mage estate gets research bonuses but costs crownland), "Oath of Maritime Defense" (knightly estate buffs navy but locks you into defensive pacts), "Merchant Charter of the Deep" (trade estate gets monopoly but triggers court rivals).

### Anbennar — Crownland Equilibrium Adjustment
- **Source:** Anbennar Wiki (wiki.anbennar.org/Mechanics)
- **What it does:** Base crown influence increased to 80 (from vanilla 60) for crownland equilibrium calculation to account for more estates. Also adjusts imperial authority, female advisor likelihood, and native ferocity mechanics.
- **Implementation notes:** Edits `common/defines/` to change `ESTATE_CROWN_INFLUENCE` base value. Other changes via define overrides.
- **Relevance:** government, estates, balance
- **Verne fit:** If Verne adds additional estates (Arcane Guild, Maritime Order, Dynastic Council), the crownland equilibrium needs recalibration. Anbennar's approach of simply bumping the base value is a clean, proven solution.

---

## Warfare & Military

_No entries yet._

---

## Colonisation & Expansion

_No entries yet._

---

## Diplomacy & Subjects

_No entries yet._

---

## UI & Quality of Life

### Europa Expanded — Scripted UI Achievements + Triggered Modifiers
- **Source:** Paradox Forums — Mod Spotlight (forum.paradoxplaza.com/threads/1678483)
- **What it does:** Recreates the triggered modifiers screen using scripted UI with page buttons. Combines achievement tracking with improved triggered modifier display. Faux Steam Achievement popups for completion.
- **Implementation notes:** `scripted_gui` replaces vanilla triggered modifiers display. Page navigation via scripted UI buttons. Popup events with custom graphics simulate achievement notifications.
- **Relevance:** UI, QoL, engagement
- **Verne fit:** "Oath Completion" popups when finishing major Verne story arcs. Scripted UI for a "Verne Codex" tracking completed oaths, discovered arcane secrets, and maritime milestones.

---

## Scouting Log

Track what has been scouted and when.

| Date | Source | Entries Found |
|------|--------|---------------|
| 2026-03-31 | Paradox Forums, Steam Workshop, Reddit, Anbennar Wiki | 12 entries |
| 2026-03-31 | EU4 modding wiki, FandomSpot | Reference only |
| 2026-03-31 | Gods and Kings, Europa Expanded, Gov Mechanics Expanded | High-value mods |


## Sources to Scout

### High Priority (EU4-specific mods)
- [Anbennar](https://github.com/Anbennar/Anbennar) — Already our base, but check interesting sub-mods
- [Paradox Forums - EU4 Mods](https://forum.paradoxplaza.com/forum/index.php?forums/eu4-mods.854/) — Mod showcases
- [Steam Workshop - EU4](https://steamcommunity.com/workshop/browsebrowsefiles.php?appid=236850) — Top-rated mods
- [r/EU4](https://reddit.com/r/eu4) — Mod posts and discussions

### Medium Priority (cross-game inspiration)
- [CK3 modding wiki](https://ck3.paradoxwikis.com/) — Similar mechanics (succession, legitimacy)
- [HOI4 modding wiki](https://hoi4.paradoxwikis.com/) — Military/production mechanics
- [Stellaris modding wiki](https://stellaris.paradoxwikis.com/) — Empire/government mechanics

### Community
- [EU4 Modding Discord](https://discord.gg/paradox-modding) — Active community, ask about implementations
- [Anbennar Discord](https://discord.gg/anbennar) — Anbennar-specific techniques

---

*This file is periodically updated by the mod-inspiration-scout cron job.*
