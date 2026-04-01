# Inspiration Bank

Ideas and patterns from other EU4 mods relevant to the Verne overhaul.

*Created: 2026-04-01 | Sources: EU4 wiki, Paradox forums, Reddit r/Anbennar, Anbennar wiki*

---

## 1. Anbennar: Massive Mission Tree Scale & Lane Density

**Source:** Anbennar wiki mission count list, Reddit r/Anbennar

**Pattern:** Anbennar's biggest trees go far beyond vanilla EU4:
- Castanor: 171 missions
- Aelnar: 155 missions  
- Azkare: 126 missions
- Jaddari: 120 missions
- The Command: praised as "probably the best mission tree and EU4 experience"

**Key insight:** Trees with 50+ missions are normal in Anbennar. Verne's ~117 missions is well within the mod's precedent. The community *wants* deep, long-form trees — "bland" trees (like Lorent's 44 missions) get criticized not for size but for lack of distinctive mechanics.

**Verne relevance:** Our 10-lane, 117-mission structure is ambitious but precedented. The key differentiator isn't mission count but *mechanical identity* per lane (Red Court arcane system, dynastic machine, trade network, etc.).

---

## 2. Modular Mission Trees (Paradox Forums Concept)

**Source:** forum.paradoxplaza.com — "Mission trees and generic rules: best of both worlds?" thread

**Pattern:** Community proposal for cascading modular mission trees — instead of one big tag-based tree, nations unlock smaller trees based on:
- Culture, religion, capital location
- Government reforms, idea groups chosen
- Buildings/monuments constructed
- History flags (wars won, provinces conquered)

Example: A flatland capital + noble republic + cavalry tradition → unlocks "hussaria" missions (normally locked to Poland).

**Key insight:** Imperator Rome attempted this with generic trees (conquest, building, capital). The idea of *swap_non_generic_missions = yes* re-evaluating potential triggers is already in EU4's engine — mods can use it to dynamically swap mission series.

**Verne relevance:** Verne's government reform system already gates missions by reform. Could extend this: certain lane branches unlock based on idea group choices (Trade Ideas → unlock merchant marine branch; Espionage Ideas → unlock Red Court intelligence branch). The `swap_non_generic_missions` effect can reload the tree when reforms change.

---

## 3. custom_tooltip + hidden_effect Pattern for Clean Tooltips

**Source:** EU4 wiki (Effects, Variables pages), Reddit r/EU4mods

**Pattern:** Best practice for variable-heavy mods:
1. Use `hidden_effect` to wrap the actual variable changes (`change_variable`, `set_country_flag`, etc.)
2. Use `custom_tooltip` to show the player-friendly description
3. Localize the variable with `GetName` + `GetValue` for dynamic display

```eu4
hidden_effect = {
    change_variable = { which = verne_world_network value = 1 }
}
custom_tooltip = verne_overhaul_tt_world_network_gain
```

**Key insight:** Variables have a max of 2,147,484 before overflow. Variables can be localized with `[Root.myVar.GetName]` and `[Root.myVar.GetValue]`. The `export_to_variable` effect can pull game values (monthly_income, treasury, etc.) into variables for dynamic tooltip display.

**Verne relevance:** Verne already uses this pattern (confirmed S02-compliant across all 21 change_variable sites). For future expansion, `export_to_variable` could be used to show dynamic scaling — e.g., "Your trade network investment yields [Root.verne_trade_income.GetValue] ducats" based on actual game state.

---

## 4. Anbennar's Storytelling-Mechanics Integration

**Source:** Reddit r/Anbennar — "Which countries have deep lore and good mission trees?" thread

**Pattern:** Community's top-rated nations (Rogieria, Kobolds, Dwarven Serpentspine tags, The Command) succeed because mechanics *embody* the lore, not just reference it:
- **The Command:** Free mercenaries to intimidate coalitions early, snowballing military dominance — the mechanics feel like playing a military juggernaut
- **Kobolds:** Trap-based defensive gameplay that matches the "small but cunning" lore
- **Rogieria:** Storytelling through mission events, not just mission descriptions
- **Dwarven holds:** Hold-building mechanics in the Serpentspine that feel architecturally different

**Key insight:** Lorent (44 missions) is criticized as "bland" despite being a major nation. The problem isn't tree size — it's that the missions don't create a *distinctive play experience*. Generic conquest/acquisition missions feel interchangeable.

**Verne relevance:** Each of Verne's 10 lanes should have a mechanical identity, not just a thematic one:
- Lane 6 (Red Court): Should *feel* like managing arcane power — risk/reward, dangerous experiments
- Lane 9 (Industrial): Should *feel* like building an industrial complex — resource chains, logistics
- Lane 10 (Diplomacy): Should *feel* like courtly maneuvering — opinion management, alliance web

---

## 5. EU4 Mission Modding: Slot Expansion Beyond 5 Columns

**Source:** EU4 wiki — Mission modding page

**Pattern:** Default EU4 has 5 mission columns (slots). The number is controlled by `max_slots_horizontal` in `countrymissionsview.gui`. Mods can increase this by editing the interface file. The `position` attribute controls row placement within a slot.

Key rules:
- `slot = <int>` (1-5 default, expandable)
- `position = <int>` (1 = top, auto-fills if omitted)
- `required_missions = { }` defines prerequisites
- `provinces_to_highlight` uses all_province scope with `NOT = { country_or_non_sovereign_subject_holds = ROOT }` to exclude owned provinces
- `swap_non_generic_missions = yes` re-evaluates all series potential triggers
- Mission localization: `<mission_name>_title` + `<mission_name>_desc`

**Key insight:** Anbennar uses 5 slots but packs massive depth per slot. The slot system is flexible — multiple series can share a slot using `position` offsets. Verne's 10-lane approach (expanding to 10 columns via interface modding) is a significant UI innovation.

**Verne relevance:** The `countrymissionsview.gui` file needs `max_slots_horizontal = 10`. Each lane maps to a slot. The `position` attribute handles vertical stacking within lanes. `required_missions` handles both intra-lane chains and cross-lane gates.

---

## 6. Disaster-Based Narrative Progression (Anbennar Pattern)

**Source:** Anbennar Paradox Spotlight, Reddit discussions

**Pattern:** Anbennar uses "multiple challenging disasters" as narrative progression gates. Disasters aren't just penalties — they're story events that:
- Force the player into crisis decisions
- Unlock new mission branches based on how the disaster is resolved
- Create branching narrative paths (e.g., "embrace the corruption" vs "purge the corruption")

**Key insight:** Disasters as *narrative devices* rather than pure mechanical penalties. The resolution path determines which missions become available.

**Verne relevance:** The Red Court Crisis (Lane 4, design goal) and the Liliac War Legacy (Lane 10) could be implemented as disasters with branching resolution paths. For example:
- Red Court Crisis: Player chooses between "Embrace Arcane Power" (unlocks Lane 6 deep arcane path) or "Purge the Court" (unlocks Lane 8 faith purification path)
- This creates organic cross-lane connections through gameplay, not just prerequisite chains

---

## 7. Localisation Structure for Large Mods

**Source:** EU4 wiki scrape (localisation section)

**Pattern:** Best practices for large mod localisation:
- File format: `l_english:` header, `KEY:0 "text"` entries
- UTF-8 with BOM encoding required
- Filename must end with `_l_english.yml`
- Override vanilla: place in `localisation/replace/`
- Text formatting: `§R§` (red), `§G§` (green), `§!` (reset)
- Value formatting: `$VAL\|=$!` (show +/-), `$VAL\|%$!` (percent), `$VAL\|+$!` (green positive/red negative)
- Dynamic text: `[Root.GetAdjective]`, `[Root.Monarch.GetName]`, `[Root.myVar.GetValue]`
- Legacy keys: `$COUNTRY$`, `$CAPITAL$`, `$MONARCH$`

**Key insight:** For large mods, organize localisation files by feature area (missions, events, modifiers, reforms) rather than by file type. Use descriptive key prefixes: `verne_mission_lane1_`, `verne_event_redcourt_`, `verne_modifier_trade_`.

**Verne relevance:** Current localisation is in a single skeleton file. Should split into:
- `verne_missions_l_english.yml` — all mission titles/descriptions
- `verne_events_l_english.yml` — all event text
- `verne_modifiers_l_english.yml` — modifier descriptions
- `verne_reforms_l_english.yml` — government reform names/descriptions
- `verne_tooltips_l_english.yml` — custom_tooltip strings

---

## 8. EU4 Mission Tree Visual Design Tools

**Source:** Steam Workshop, GitHub, Reddit

**Pattern:** Community tools for mission tree design:
- **EU4 Mission Tree Exporter & Planner** (Steam Workshop): Visual designer that exports to functional .txt files
- **Eu4MissionEditorDesktop** (GitHub): Graph editor for mission trees, supports EU4 + HOI4
- **EMV** (GitHub): EU4 Mod Data Viewer — can inspect existing mod mission structures

**Key insight:** Visual tools help with the layout problem — ensuring positions don't overlap, prerequisites form valid DAGs, and the tree is navigable in-game.

**Verne relevance:** Consider using Eu4MissionEditorDesktop to validate the 10-lane layout. The graph view would reveal any remaining position conflicts or circular dependencies across lanes.

---

*Last updated: 2026-04-01*
