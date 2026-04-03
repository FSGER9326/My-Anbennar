# Verne Standards Tracker

> Tracks compliance against Verne standards and documents deviations.

## Purpose

This document records which Verne implementation standards are being followed,
which are not, and why. It is a living record of implementation decisions
and the rationale behind deviations from the original design.

---

## Compliance Checklist Summary

| Item | Status | Last Verified |
|------|--------|--------------|
| `verne_overhaul_l_english.yml` — no duplicate loc keys | ✅ PASS | 2026-04-03 |
| `verne_overhaul_dynasty_l_english.yml` — no duplicate loc keys | ✅ PASS | 2026-04-03 |
| `verne_overhaul_lanes_l_english.yml` — no duplicate loc keys | ✅ PASS | 2026-04-03 |
| Flavour loc (vanilla Anbennar) — no duplicate keys | ✅ PASS | 2026-04-03 |
| Policy split loc — no duplicate keys | ✅ PASS | 2026-04-03 |
| Event ID audit — all 122 event IDs properly namespaced | ✅ PASS | 2026-04-03 |
| Markdown link audit — no broken links in docs | ✅ PASS | 2026-04-03 |
| `docs/automation` conflict guard — no conflicts | ✅ PASS | 2026-04-03 |
| Event ID audit (Flavour_Verne_A33) | ✅ PASS | 2026-04-03 |
| Event ID audit (verne_overhaul_dynasty_events) | ✅ PASS | 2026-04-03 |
| Event ID audit (verne_overhaul_advisor_events) | ✅ PASS | 2026-04-03 |
| Event ID audit (verne_overhaul_liliac_events) | ✅ PASS | 2026-04-03 |
| Event ID audit (verne_overhaul_crisis_events) | ✅ PASS | 2026-04-03 |
| Checklist audit — all wiki items current | ✅ PASS | 2026-04-03 |

**Score: 14/14 PASS** (as of 2026-04-03 smoke run)

---

## Key Implementation Findings

### Vanilla Loc Override Precedence (Critical)

**Finding (2026-04-03):** Verne mod loads loc files in alphabetical order.
`Flavour_Verne_A33_l_english.yml` (vanilla Anbennar) loads AFTER
`verne_overhaul_l_english.yml`. Any duplicate keys in the vanilla file
silently overwrite overhaul values at runtime.

**Implications:**
- Adding new loc entries to `verne_overhaul_l_english.yml` that already exist
  in vanilla will not override the vanilla values — they will be ignored.
- Only add loc entries to the overhaul file if they do NOT exist in vanilla.
- The vanilla file is authoritative for all shared keys.

**Action:** Before adding any new loc to `verne_overhaul_l_english.yml`,
always verify the key does not exist in `Flavour_Verne_A33_l_english.yml`.

---

## Non-Standard Deviations

### Slots 6–9 — NOT A BUG (Corrected 2026-04-03)

**Finding:** Slots 6–9 are empty container definitions with no missions assigned.
Actual mission slot distribution: slot 1 = 7 missions, slot 2 = 20 missions,
slot 3 = 4 missions, slots 4–5 = 0 missions.

`max_slots_horizontal = 5` is correct. Empty slot definitions don't affect gameplay.
No design issue exists here.

---

## Deprecated / Retired Files

| File | Status | Notes |
|------|--------|-------|
| `events/zzz_verne_overhaul_dynasty_events.txt` | ✅ Retired | Minimal header, superseded by `verne_overhaul_dynasty_events.txt` |
| `localisation/zzz_verne_overhaul_dynasty_l_english.yml` | ✅ Retired | Minimal header, superseded by `verne_overhaul_dynasty_l_english.yml` |
| `common/on_actions/zzz_verne_overhaul_dynasty_on_actions.txt` | ✅ Retired | Minimal header, superseded by `verne_overhaul_on_actions.txt` |
| `common/on_actions/zz_verne_overhaul_on_actions.txt` | ✅ Retired | Minimal header, superseded by `verne_overhaul_on_actions.txt` |
| `common/government_reforms/zzz_verne_overhaul_dynasty_reforms.txt` | ✅ Retired | Superseded by `verne_overhaul_reforms.txt` |

All retired files retain their `zzz` / `zz` prefixes to preserve any
historical content while ensuring they load last and are ignored by EU4
when their authoritative replacements are present.

---

## Encoding Standards

All Verne loc files use **UTF8-BOM** encoding. Verified 2026-04-03:

| File | Encoding | Status |
|------|----------|--------|
| `localisation/verne_overhaul_l_english.yml` | UTF8-BOM | ✅ |
| `localisation/verne_overhaul_dynasty_l_english.yml` | UTF8-BOM | ✅ |
| `localisation/verne_overhaul_lanes_l_english.yml` | UTF8-BOM | ✅ |
| `localisation/verne_overhaul_policy_split_l_english.yml` | UTF8-BOM | ✅ |
| `localisation/Flavour_Verne_A33_l_english.yml` | UTF8-BOM | ✅ |
| `localisation/speaking_memory_l_english.yml` | UTF8-BOM | ✅ |

---

## Loc File Responsibilities

| File | Purpose | Loads |
|------|---------|-------|
| `verne_overhaul_l_english.yml` | Main overhaul loc (modifiers, events, missions, decisions) | 3rd |
| `verne_overhaul_dynasty_l_english.yml` | Dynasty event loc | 3rd |
| `verne_overhaul_lanes_l_english.yml` | Lane/mission-group names | 3rd |
| `verne_overhaul_policy_split_l_english.yml` | Policy split loc | 3rd |
| `Flavour_Verne_A33_l_english.yml` | Vanilla Verne loc (from Anbennar mod) | 4th (overrides all above) |
| `speaking_memory_l_english.yml` | Speaking memory flavor loc | 3rd |

**Key rule:** Only add loc to `verne_overhaul_l_english.yml` for keys that do NOT
exist in `Flavour_Verne_A33_l_english.yml`.

---

*Last updated: 2026-04-03*
*Updated by: Scribe (AI agent) during night session*
