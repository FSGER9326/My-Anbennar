# Verne Mod Living Roadmap

**Updated:** 2026-04-01 03:06 CET
**Branch:** `chore/verne-10-lane-blueprint`
**Background worker:** ✅ Running (auto-improves)

---

## Recent Fixes (background worker completed)
- ✅ verne_mission_start flag added to lane1
- ✅ verne_royal_arbitration_complete flag added to lane1
- ✅ Reform name typos fixed in lane1 (2 fixes)
- ✅ Lane 4 placeholder reform IDs replaced with actual IDs
- ✅ 11 position conflicts remapped (all lanes)
- ✅ Modifier definitions written: 65 modifiers (31 new + 34 existing preserved)
- ✅ Localisation skeleton written: ~96KB, 24 missions + 65 modifiers + events + reforms

## Current Status

- **Lanes designed (docs):** 8/8 (lane0-6, 8 in `docs/design/lanes/`)
- **Lanes implemented (code):** 9 slots active in `missions/Verne_Missions.txt`
  - Slot 1 (first_slot): 13 missions
  - Slot 2 (second_slot): 17 missions
  - Slot 3 (third_slot): 28 missions
  - Slot 4 (fourth_slot): 22 missions
  - Slot 5 (fifth_sloth): 14 missions
  - Slot 6 (sixth_slot): 6 missions
  - Slot 7 (seventh_slot): 5 missions (Lane 7 — Vernissage Secretariat)
  - Slot 8 (eighth_slot): 2 missions
  - Slot 9 (ninth_slot): 1 mission (Lane 9 — Industrial Foundries)
  - **Total:** ~117 missions
- **Modifiers implemented:** 34 in `common/event_modifiers/verne_overhaul_modifiers.txt`
- **GFX assets:** Unknown — no gfx audit completed yet
- **Standards compliance:** 8 standards defined (S01–S08), **QA scan completed** 2026-04-01
  - S01 (Numbers in tooltips): ⚠️ Partial — expansion missions (slots 6-9) lack numeric tooltips
  - S02 (Variable tracking): ❌ FAIL — 15+ missions change hidden variables without tooltip notification (biggest gap)
  - S03 (Prerequisite tooltips): ⚠️ Partial — Liliac War flag-gated missions lack explanation
  - S04 (Cross-references): ✅ Pass
  - S05 (Terminology): ⚠️ 13 typos found in player-facing text
  - S06 (Modifier _desc): ⚠️ 2 modifiers missing descriptions
  - S07 (Mission keys): ✅ Pass — all 117 missions have _title/_desc
  - S08 (Lore): ✅ Pass
- **Events:** 6 event files exist, ~200+ events total across `Flavour_Verne_A33.txt` and overhaul files

---

- ✅ Localisation skeleton written: `localisation/verne_overhaul_lanes_l_english.yml` — 106 keys (52 mission title/desc + 54 modifier title/desc) covering all 24 lane missions + 30 modifiers. File uses UTF-8 BOM. Note: these are design doc keys only — actual codebase uses different mission IDs (see design-implementation divergence below).

## Key Finding: Design-Implementation Divergence

**The design docs in `docs/design/lanes/` are a BLUEPRINT that has NOT been directly implemented.**

The actual `Verne_Missions.txt` uses completely different mission IDs than the design docs:

| Design Doc ID | Design Purpose | Actual Implementation |
|---|---|---|
| `A33_formalize_silver_oaths` | Lane 1, mission 1 | ❌ Does not exist — replaced by overhaul helper layer |
| `A33_establish_court_of_oaths` | Lane 1, mission 2 | ❌ Does not exist |
| `A33_royal_arbitration` | Lane 1, mission 3 | ❌ Does not exist |
| `A33_diplomatic_hegemony` | Lane 1, mission 4 | ❌ Does not exist |
| `A33_secure_port_of_heartspier` | Lane 2, mission 1 | ❌ Does not exist — replaced by `A33_the_grand_port_of_heartspier` |
| `A33_fleet_of_the_crimson_wake` | Lane 2, mission 3 | ❌ Does not exist |
| `A33_enact_dynastic_safeguard` | Lane 3, mission 1 | ❌ Does not exist |
| `A33_exalted_dynasty_machine` | Lane 3, mission 3 | ❌ Does not exist |
| *(all 24 design missions)* | Lanes 1-6, 8 | ❌ **None exist** in codebase |

**Design doc modifiers (30 total) — NONE implemented:**
- `verne_silver_oaths`, `verne_court_of_oaths`, `verne_royal_arbitration`, `verne_diplomatic_hegemony` (Lane 1) — ❌
- `verne_heartspier_port`, `verne_heartspier_companies`, `verne_crimson_wake_fleet`, `verne_imperial_sea_court` (Lane 2) — ❌
- `verne_dynastic_safeguard`, `verne_noble_charter`, `verne_exalted_dynasty_machine` (Lane 3) — ❌
- `verne_chartered_overseas_companies`, `verne_distant_horizons`, `verne_overseas_commanderies` (Lane 4) — ❌
- `verne_red_court_advisory`, `verne_dragonwake_profession`, `verne_battle_mage_collegium` (Lane 5) — ❌
- `verne_royal_census`, `verne_academic_endowments`, `verne_sovereign_legitimacy` (Lane 6) — ❌
- `verne_corinite_stewardship`, `verne_pearlescent_concord`, `verne_world_faith_emperor` (Lane 8) — ❌

**What exists instead:**
- 34 different modifiers in `common/event_modifiers/verne_overhaul_modifiers.txt` (e.g., `verne_dynasty_protected_court`, `verne_imperial_maritime_court`, `verne_vernissage_secretariat`)
- ~117 missions with unique IDs reflecting organic evolution (gnoll partnerships, wyvern nests, Liliac War, Vernissage, expedition fleets, etc.)
- Events split across 6 files: `Flavour_Verne_A33.txt` (main), `verne_overhaul_advisor_events.txt`, `verne_overhaul_dynasty_events.txt`, `verne_overhaul_crisis_events.txt`, `verne_overhaul_liliac_events.txt`

**Design doc events — missing:**
- `verne_overhaul_oaths.1`, `.2`, `.3` — ❌ Does not exist (Lane 1 Silver Oaths chain)
- `verne_overhaul_advisor.100` — ❌ Does not exist (Lane 5 mage advisor, only `.1` exists)
- `verne_overhaul_dynasty.1` — ✅ Exists
- `verne.200` — ✅ Exists (Battle Mage Collegium)

---

## What's Done (Implementation History)

Recent commits show extensive work completing all 9+ lane slots:

- `6e5a2ee941` — Lane 7 (Vernissage Secretariat) implemented
- `40a6576cc9` — Lane 9 (Industrial Foundries) implemented
- `491fe32081` — Lane 6 (Adventure Network expansion) implemented
- `a49ad4ecac` — Lane 10 (Liliac War legacy) implemented
- `f8af412c4d` — Luna River Basin integration event
- `45d1aa629e` — Rogue Duchy → Khenak system connection
- `5e1d4261e4` — Silver Wake + Dragonwake military decisions
- `bff1cc367a` — Mage debt system + mission structure simplification
- `30a0f7a0c6` — Gnoll partnership system
- `19c21e96ba` — Docs reconciled with live implementation state

**No lane design files have been checked against actual code.** The design docs remain aspirational blueprints.

---

## What Needs Doing (Priority Order)

### 1. [CRITICAL] Reconcile Design Docs with Implementation

The design docs describe missions/modifiers/events that don't exist. This blocks:
- QA subagents (they'd check nonexistent IDs)
- Standards compliance checks (they'd fail on missing content)
- Any future planning that references design doc mission IDs

**Options:**
- **A) Update design docs** to match actual implementation — rewrite lane files with real mission IDs, real modifiers, real event references
- **B) Implement design doc missions** on top of existing code — add the 24 blueprint missions + 30 modifiers as new content
- **C) Hybrid** — some lanes get implemented, others documented as-is

**Needs Human Input:** Falk must decide A, B, or C before any subagent work can reference these docs.

### 2. [CRITICAL] Standards Compliance QA Scan (S01–S08) ✅ COMPLETED

QA scan completed 2026-04-01. Results in `docs/verne-standards-tracker.md`.

**Key findings:**
- **S02 (Variable tracking)** is the biggest gap: 15+ missions change `verne_world_network` and `verne_overseas_projection` without tooltip notification
- **S05 (Terminology)** has 13 typos batch-fixable
- **S06 (Modifier _desc)** has 2 missing descriptions for `verne_trade_company_conversion_modifier` and `verne_indebted_to_the_mages_small`

**Action: Fix S02 first** — create shared tooltip templates for variable gains, add `custom_tooltip` to every effect block changing hidden variables.

### 3. [HIGH] Create Missing Oaths Event Chain

`verne_overhaul_oaths.1`, `.2`, `.3` are referenced in design doc Lane 1 but don't exist. If the Silver Oaths system was meant to be implemented:

- Design doc Lane 1 calls for 3 events in `verne_overhaul_oaths` namespace
- Current implementation has `verne_dynasty_protected_court` and `verne_marriage_court_protocol` modifiers that may serve similar purposes
- Need to determine if oaths chain was absorbed into existing code or simply never created

### 4. [HIGH] Localisation Audit

Check if all ~117 missions have proper `_title`, `_desc`, `_tt` keys in:
- `localisation/Flavour_Verne_A33_l_english.yml` (369KB — likely has most)
- `localisation/verne_overhaul_l_english.yml` (73KB — modifiers + events)

### 5. [HIGH] Modifier Cross-Reference

Verify all 34 modifiers in `verne_overhaul_modifiers.txt` are actually referenced in missions/events, and that all modifiers referenced in missions exist in the file.

### 6. [MEDIUM] Decision Definitions Audit

Design doc Lane 4 references two decisions:
- `verne_charter_overseas_decision` — grant +1 merchant per 10 years
- `verne_commandant_swap_decision` — swap governor for commandant

Check if these exist in `common/decisions/` or were never created.

### 7. [MEDIUM] CB Definition for Faith Lane

Design doc Lane 8 sets `verne_cb_against_heathen_pirates` flag but notes the actual CB in `common/cb_types/` is a follow-up task. Verify if it exists.

### 8. [MEDIUM] Government Reform Verification ✅ COMPLETED 2026-04-01

Verified 14 roadmap reforms against `common/government_reforms/verne_overhaul_reforms.txt` (24 total reforms).

**Results: 11/14 ✅ | 2 ❌ MISSING | 1 ⚠️ NAME MISMATCH**

- ✅ `verne_estuary_companies_of_heartspier_reform` (line 73)
- ✅ `verne_admiralty_of_the_crimson_wake_reform` (line 58)
- ✅ `verne_imperial_sea_court_reform` (line 264)
- ✅ `verne_throne_of_the_wyvern_kings_reform` (line 345)
- ✅ `verne_hall_of_distant_horizons_reform` (line 169)
- ✅ `verne_overseas_commanderies_reform` (line 279)
- ✅ `verne_red_court_arcana_reform` (line 108)
- ✅ `verne_dragonwake_ordinance_reform` (line 122)
- ✅ `verne_battle_mage_collegium_reform` (line 136)
- ✅ `verne_apostolic_court_of_corin_reform` (line 297)
- ✅ `verne_vernman_court_of_the_world_reform` (line 312)
- ⚠️ `verne_court_of_oaths_reform` → actual name is `verne_court_of_silver_oaths_reform` (line 9)
- ❌ `verne_crown_of_the_oathkeeper_reform` — NEVER IMPLEMENTED
- ❌ `verne_exalted_dynasty_machine_reform` — NEVER IMPLEMENTED

**Also found 10 codebase-only reforms** not referenced in any lane design doc, suggesting organic expansion. Full report: `docs/reform-verify-report.md`.

### 9. [LOW] GFX Audit

No audit exists for mission icons, decision icons, or event pictures. Need to:
- List all icons referenced in `Verne_Missions.txt`
- Verify they exist in `gfx/`
- Check event pictures in `Flavour_Verne_A33.txt`

---

## Parallelizable Tasks

These can run simultaneously as separate subagents:

1. **QA Scan** — Check S01–S08 compliance on all files (doesn't need design doc alignment)
2. **Modifier Cross-Reference** — Scan missions ↔ modifier file for mismatches
3. **Localisation Audit** — Check all mission keys have matching yml entries
4. **Government Reform Verification** — Check reform references in `common/government_reforms/`
5. **Decision & CB Audit** — Check if design doc decisions/CBs exist

---

## Needs Human Input

1. **[CRITICAL] Design vs Implementation direction:** Should design docs be rewritten to match code (A), code extended to match design (B), or hybrid (C)? This blocks all lane-specific subagent work.
2. **Scope of Lane 7 & 9:** These slots exist in code but have no design docs. Should design docs be created for them?
3. **Lane numbering:** Design docs use lanes 0-6, 8. Implementation has slots 1-9. Should design docs be renumbered to match?
4. **Event namespace:** Should `verne_overhaul_oaths.*` events be created, or was the oath system absorbed into existing events?
5. **Modifier philosophy:** The design defines 30 specific modifiers; the codebase has 34 different ones. Should design modifiers be added on top, or are the existing ones sufficient?

---

## Blocked On

- **QA subagents** → Need human decision on design direction (priority 1) before lane-specific checks make sense
- **S02 fix implementation** → Need to create shared tooltip templates and add custom_tooltip to 15+ missions (see `docs/verne-standards-tracker.md`)
- **S05 typo batch fix** → 13 typos flagged, ready for find-and-replace pass
- **Missing oaths events** → Need confirmation they should be created vs. absorbed

---

## Next Scheduled Work

| Task | When | Trigger |
|------|------|---------|
| QA compliance scan | After human chooses design direction | Cron (Mon/Wed/Fri 2AM) |
| Upstream Anbennar sync | Wed + Sun 10 AM | Cron |
| Mod inspiration scout | Mon + Thu 8 PM | Cron |
| Health monitor | Every 30 min | Cron |

---

*This roadmap is a living document. Update after every planning run. All subagent work should reference this for priorities.*
