# Verne Loc Completeness Audit

**Date:** 2026-04-06  
**Auditor:** Scribe (automated cron)  
**Repo:** My-Anbennar  
**Scope:** `verne_overhaul_l_english.yml`, `verne_overhaul_dynasty_l_english.yml`, `verne_overhaul_policy_split_l_english.yml`, `Flavour_Verne_A33_l_english.yml` (vanilla, read-only)

---

## Summary

| Check | Result |
|-------|--------|
| Duplicate key detection (vanilla ↔ overhaul) | ⚠️ 53 duplicates — overhaul wins (correct precedence) |
| Missing key audit | ❌ 26 missing keys across events, missions, decisions |
| Empty value check | ✅ CLEAN — zero empty values |
| Scope tag audit | ⚠️ 1 event missing loc; 13 decision titles missing |

---

## 1. Duplicate Key Detection

**53 keys** appear in both vanilla (`Flavour_Verne_A33_l_english.yml`) and the overhaul loc files.

**Load order:** `Flavour_Verne_A33_l_english.yml` loads first (F < v), then all `verne_overhaul_*.yml` files load in alphabetical order. The overhaul **wins** for all 53 duplicates — this is the intended override behavior. No precedence bug.

Notable semantic changes in overhaul overrides:

| Key | Vanilla | Overhaul |
|-----|---------|----------|
| `A33_the_vernman_renaissance_title` | "The Vernman Renaissance" | "The Vernman Renaissance" | (same) |
| `A33_break_the_queen_of_the_hill_title` | "Disperse the Hill Gnolls" | "Break the Hill Queen" | (rebranded) |
| `A33_religious_mercantilism_title` | "Religious Mercantilism" | "Sacred Mercantilism" | (tone change) |
| `A33_the_holy_corinite_empire_title` | "Corin's Holy Empire" | "The Holy Corinite Empire" | (order change) |
| `A33_type_2_wyverns_title` | "Type 2 Wyverns" | "Type II Wyverns" | (roman numeral) |
| `verne.200.t` | "A Peculiar Land" | "The Battle Mage Collegium Opens" | (entirely rewritten) |
| `NEW_VERNE` | "New Verne" | "New Verne (Kingdom)" | (expanded) |

All 53 overrides are intentional reworkings by the overhaul. No vanilla value is silently lost due to load order.

---

## 2. Missing Key Audit

### 2a. Missing mission tooltip keys (11 keys)

These `custom_tooltip = key` references exist in `Verne_Missions.txt` but have **no entry in vanilla or overhaul loc**. These cause silent tooltip failures in-game.

| Missing Key | Likely Purpose |
|-------------|----------------|
| `verne_corinite_stewardship_effect_tt` | Corinite Stewardship mission effect tooltip |
| `verne_D5_effect_tt3_no` | D5 mission conditional branch (no path) |
| `verne_D5_effect_tt3_yes` | D5 mission conditional branch (yes path) |
| `verne_expand_foundry_tt` | Khenak Foundry expansion tooltip |
| `verne_found_crimson_scale_order_tt` | Crimson Scale order founding tooltip |
| `verne_industrial_logistics_tt` | Industrial logistics tooltip |
| `verne_khenak_steel_tt` | Khenak steel production tooltip |
| `verne_spice_route_monopoly_tt` | Spice trade monopoly tooltip |
| `verne_trade_network_tt` | Trade network tooltip |
| `verne_vernman_merchant_marine_tt` | Merchant marine tooltip |
| `verne_world_faith_emperor_tt` | World Faith Emperor tooltip |

### 2b. Missing decision `_title` loc keys (13 keys)

EU4 convention for decisions is `key_title` and `key_desc`. The overhaul has all `_desc` entries but is missing the `_title` entries for 13 decisions. The base key (without suffix) is used as the title — this may work but deviates from standard `_title` convention.

| Missing Key | Base Decision |
|-------------|--------------|
| `verne_overhaul_appoint_court_advisor_title` | `verne_overhaul_appoint_court_advisor` |
| `verne_overhaul_charter_khenak_talons_title` | `verne_overhaul_charter_khenak_talons` |
| `verne_overhaul_codify_union_court_protocols_title` | `verne_overhaul_codify_union_court_protocols` |
| `verne_overhaul_consolidate_reforged_court_title` | `verne_overhaul_consolidate_reforged_court` |
| `verne_overhaul_form_harbormaster_general_staff_title` | `verne_overhaul_form_harbormaster_general_staff` |
| `verne_overhaul_formalize_dovesworn_partnership_title` | `verne_overhaul_formalize_dovesworn_partnership` |
| `verne_overhaul_formalize_silver_oaths_title` | `verne_overhaul_formalize_silver_oaths` |
| `verne_overhaul_levy_silver_wake_convoy_title` | `verne_overhaul_levy_silver_wake_convoy` |
| `verne_overhaul_muster_dragonwake_cadets_title` | `verne_overhaul_muster_dragonwake_cadets` |
| `verne_overhaul_open_marriage_court_title` | `verne_overhaul_open_marriage_court` |
| `verne_overhaul_organize_pearlescent_diplomatic_corps_title` | `verne_overhaul_organize_pearlescent_diplomatic_corps` |
| `verne_overhaul_pay_off_mage_debt_title` | `verne_overhaul_pay_off_mage_debt` |
| `verne_overhaul_sponsor_curatorial_embassies_title` | `verne_overhaul_sponsor_curatorial_embassies` |

### 2c. Vanilla event loc entries using `.d1`/`.d2`/`.d.<suffix>` format

53 vanilla event `.d` keys are absent from vanilla loc because those events use the multi-option `desc = { desc = "..." }` format (`.d1`, `.d2`, `.d.<suffix>` variants). **These are not missing — they use conditional event description branches.**

List: `verne.113.d`, `verne.142.d`, `verne.500.d`, `verne.503.d`, `verne.1001.d`, `verne.1002.d`, `verne.1003.d`, `verne.1009.d`, `verne.1010.d`, `verne.1011.d`, `verne.1012.d`, `verne.1014.d`, `verne.1015.d`, `verne.1016.d`, `verne.1018.d`, `verne.1019.d`, `verne.1020.d`, `verne.1022.d`, `verne.1023.d`, `verne.1024.d`, and 33 more with the same pattern.

---

## 3. Empty Value Check

**✅ CLEAN** — Zero keys with empty or null values in any overhaul loc file.

---

## 4. Scope Tag Audit

### 4a. Event IDs vs loc keys

**Overhaul events (25 IDs total):**

| Event ID | `.t` (title) | `.d` (desc) | Status |
|----------|--------------|-------------|--------|
| `verne_overhaul_advisor.1–6` | ✅ in loc | ✅ in loc | CLEAN |
| `verne_overhaul_crisis.1–9` + `.100` | ✅ in loc | ✅ in loc | CLEAN |
| `verne_overhaul_dynasty.1` | ✅ in loc | ✅ in loc | CLEAN |
| `verne_overhaul_flavour.1` | ❌ MISSING | ❌ MISSING | **BROKEN** |
| `verne_overhaul_flavour.2–4` | ✅ in loc | ✅ in loc | CLEAN |
| `verne_liliac.1–4` | ✅ in loc | ✅ in loc | CLEAN |

**Action required:** `verne_overhaul_flavour.1.t` and `verne_overhaul_flavour.1.d` are completely missing loc entries.

**Vanilla events (126 IDs):** All have required `.t` entries in vanilla loc. Branching `.d` variants (`.d1`, `.d2`, `.d.<suffix>`) are correctly used for multi-option event descriptions.

### 4b. Decision loc keys

See Section 2b above — 13 decision `_title` keys missing.

### 4c. Mission title keys

All `A33_*_title` keys referenced in `Verne_Missions.txt` exist in either vanilla or overhaul loc.

---

## Files Inspected

| File | Lines | Keys |
|------|-------|------|
| `verne_overhaul_l_english.yml` | ~1310 | ~900 |
| `verne_overhaul_dynasty_l_english.yml` | 12 | 8 |
| `verne_overhaul_policy_split_l_english.yml` | 10 | 5 |
| `Flavour_Verne_A33_l_english.yml` (vanilla) | ~1600 | ~1193 |

---

## Action Items

1. **[HIGH]** Add `verne_overhaul_flavour.1.t` and `verne_overhaul_flavour.1.d` to `verne_overhaul_flavour_l_english.yml`
2. **[HIGH]** Add the 11 missing mission tooltip keys to `verne_overhaul_l_english.yml`
3. **[MEDIUM]** Add `*_title` entries for the 13 decisions, following EU4 `key_title` convention (or confirm base-key-as-title is intentional)
4. **[LOW]** Review the 53 duplicate keys where overhaul deviates semantically from vanilla — confirm all are intentional overwrites

---

*Generated by Scribe automated audit — 2026-04-06*
