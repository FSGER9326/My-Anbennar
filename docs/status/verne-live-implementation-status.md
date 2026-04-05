# Verne Live Implementation Status

Last reviewed from code: **2026-04-05**
Authoritative scope: live Verne overhaul implementation state derived from repo files, not older roadmap/backlog prose.

## Purpose

This file is the **single authoritative implementation-status source** for the Verne overhaul.

Use this file when answering:
- what is live right now,
- what is only partially integrated,
- what is still planned,
- what is referenced in docs but was not re-verified in this pass.

Do **not** treat roadmap/backlog/spec prose as implementation truth. Those files are planning tools, not status ledgers.

## Standard status labels

- **Live** — implemented in live repo files and verified in this pass.
- **Partial** — implemented in real files, but incomplete, thinly integrated, or still missing important playability follow-through.
- **Planned** — still intended work, not implemented in the canonical owner files verified here.
- **Referenced but not verified in this pass** — mentioned elsewhere or adjacent to live systems, but not re-audited in code here.

## System status table

| System | Status | Canonical owner file(s) | Playability impact |
|---|---|---|---|
| Doctrine groups | **Live** | `common/ideas/verne_doctrine_groups.txt`, `localisation/verne_overhaul_l_english.yml` | Verne has a broad doctrine roster across maritime, court, overseas, magical, industrial, dynastic, and faith-imperial lanes. This is no longer a prototype slice. |
| Doctrine policies | **Live** | `common/policies/verne_doctrine_policies.txt`, `localisation/verne_overhaul_l_english.yml` | Verne has a substantial cross-doctrine policy layer. This is no longer a placeholder scaffold. The main risk is integration/balance verification, not missing object coverage. |
| Government reforms | **Live** | `common/government_reforms/verne_overhaul_reforms.txt`, `localisation/verne_overhaul_l_english.yml` | Verne has a broad reform ladder spanning multiple state identities and late-game synthesis states. This is real live content, not just a foundation tier. |
| Dynasty safeguard and heir logic | **Live** | `common/on_actions/verne_overhaul_on_actions.txt`, `events/verne_overhaul_dynasty_events.txt`, `common/scripted_triggers/verne_overhaul_triggers.txt`, `common/scripted_effects/verne_overhaul_effects.txt`, `localisation/verne_overhaul_dynasty_l_english.yml` | A live safeguard path exists for invalid/no-heir states and dynasty protection helpers. This is a real gameplay safety net, though broader dynasty-event breadth remains limited. |
| Dynasty / court decisions | **Live** | `decisions/verne_overhaul_decisions.txt`, `common/scripted_triggers/verne_overhaul_triggers.txt`, `common/scripted_effects/verne_overhaul_effects.txt`, `localisation/verne_overhaul_l_english.yml` | Verne has a live decision surface covering dynasty protection, marriage court, advisor access, Khenak/order chartering, post-crisis consolidation, harbor-state steering, curatorial steering, and dynastic diplomacy steering. This is no longer placeholder-only. |
| Advisor package | **Partial** | `common/advisortypes/verne_overhaul_advisors.txt`, `events/verne_overhaul_advisor_events.txt`, `decisions/verne_overhaul_decisions.txt`, `localisation/verne_overhaul_l_english.yml` | A real bespoke advisor package exists and is wired into decisions and some missions. It is playable, but still relatively compact compared with the breadth of the doctrine/reform layer. |
| Mission rewrite / mission integration | **Partial** | `missions/Verne_Missions.txt`, `common/scripted_triggers/verne_overhaul_triggers.txt`, `common/scripted_effects/verne_overhaul_effects.txt`, `localisation/verne_overhaul_l_english.yml` | Slot headers (slots 5–9) corrected 2026-04-02. Liliac-lane prerequisite wiring (7 missions) corrected 2026-04-02. 9 new missions added: A33_corinite_stewardship, A33_pearlescent_concord (Lane 8), A33_establish_trade_network, A33_vernman_merchant_marine, A33_spice_route_monopoly (Lane 5), A33_found_the_crimson_scale_order (Lane 7), A33_world_faith_emperor (Lane 8), A33_expand_the_foundry_complex, A33_khenak_steel_program, A33_industrial_logistics_chain (Lane 9). 8 new modifiers added to support new missions. Full audit against doctrine/reform/dynasty/order/crisis layer still pending. |
| Order state / mercenary state | **Partial** | `common/mercenary_companies/verne_overhaul_orders.txt`, `events/Flavour_Verne_A33.txt`, `decisions/verne_overhaul_decisions.txt`, `missions/Verne_Missions.txt`, `localisation/verne_overhaul_l_english.yml` | Verne has bespoke merc/order companies and some unlock wiring through decisions, missions, and legacy flavor events. This is playable, but still thinner than the doctrine/reform layer and should be treated as an active integration surface, not a finished subsystem. |
| Pressure / disaster state | **Partial** | `common/disasters/verne_overhaul_crisis.txt`, `events/verne_overhaul_crisis_events.txt`, `decisions/verne_overhaul_decisions.txt`, `missions/Verne_Missions.txt`, `common/event_modifiers/verne_overhaul_modifiers.txt`, `localisation/verne_overhaul_l_english.yml` | A real Verne court crisis exists, with monthly events, mission interaction, and post-crisis payoff. It is no longer just a concept, but still needs fuller campaign-level testing and probably future branching/resolution audit work. |
| Helper layers (scripted triggers/effects/modifiers) | **Live** | `common/scripted_triggers/verne_overhaul_triggers.txt`, `common/scripted_effects/verne_overhaul_effects.txt`, `common/event_modifiers/verne_overhaul_modifiers.txt`, `localisation/verne_overhaul_l_english.yml` | Reusable helper-state infrastructure is clearly live and supports missions, decisions, dynasty logic, crisis logic, and state-shaping rewards. |
| Localisation coverage | **Live** | `localisation/verne_overhaul_l_english.yml`, `localisation/verne_overhaul_dynasty_l_english.yml` | 39 missing mission-name loc entries added 2026-04-03. All `name` values from `Verne_Missions.txt` now have corresponding loc entries. Coverage is comprehensive for doctrines, reforms, decisions, advisors, modifiers, crisis, and mission content. |
| Legacy flavor file interaction | **Referenced but not verified in this pass** | `events/Flavour_Verne_A33.txt` | The legacy Verne flavor file still owns important live mission/event behavior and remains part of the playable spine. It was used as evidence of live interaction, but not comprehensively re-audited here. |

## Playability summary

### Mechanically implemented systems

Verne now has real mechanical breadth in:
- doctrine groups,
- doctrine policies,
- government reforms,
- dynasty safeguards,
- state-shaping decisions,
- advisor recruitment,
- custom merc/order companies,
- crisis/disaster state,
- reusable helper layers.

This is **well beyond a scaffold phase**.

### Campaign-spine integration

The mission tree already integrates many of these systems through:
- helper variables,
- flags,
- scripted triggers/effects,
- mission rewards,
- crisis suppression hooks,
- advisor/event triggers,
- order unlock flow.

That said, the campaign spine is **not yet fully re-audited against the broadened doctrine/reform/dynasty/state layer**.

### Mission-driven playability

Verne currently looks **more like a playable overhaul-in-progress than a mere systems prototype**.

But the most playability-critical risk is now **mission-spine truthfulness and integration correctness**, not lack of raw mechanical objects.

In plain terms:
- the repo already contains a lot of real Verne content,
- but campaign quality now depends more on integration verification than on adding more doctrine/reform breadth.

### Honest current assessment

Current state: **playable-overhaul direction with meaningful live systems, but still carrying integration risk and documentation debt**.

Not accurate anymore:
- “placeholder-only policy layer”
- “placeholder-only decision layer”
- “early scaffold state” as a general description of the whole overhaul

Still accurate:
- some systems are broader in object count than in campaign validation,
- mission integration remains the most important technical audit surface,
- documentation had fallen behind the code before this pass.

## Playability-critical gaps called out clearly

Highest-priority gaps after this documentation pass:

1. **Mission spine audit against live overhaul state**
   - `missions/Verne_Missions.txt` should be audited against the live doctrine/reform/dynasty/order/crisis/helper layer.
   - This is the best next gameplay task because campaign playability depends on the mission spine more than on adding more object breadth.

2. **Legacy/base-file interaction verification**
   - `events/Flavour_Verne_A33.txt` still matters heavily to live playability.
   - It should be checked systematically against the newer overhaul layers instead of being treated as background truth by assumption.

3. **Order/advisor/crisis subsystem depth and validation**
   - These systems are live and meaningful, but still thinner and less broadly validated than doctrines/reforms.

4. **Localization completeness follow-through**
   - Broad coverage exists, but any future owner-file change still needs same-pass loc verification.

## Documentation rules for status claims

Status claims about Verne implementation must:
- be derived from **live repo files**,
- use the standard labels **Live / Partial / Planned / Referenced but not verified**,
- be updated in this file when implementation status changes.

Roadmap/backlog/spec docs must **not** carry their own competing implementation-status snapshot if that would duplicate or contradict this file.

## Localisation follow-through (2026-04-05)

- Added missing localisation coverage for live mission reward modifiers `verne_trade_network` and `verne_merchant_marine` in `localisation/verne_overhaul_l_english.yml`.
- This closed a presentation gap in the new trade-lane rewards: the scripted modifiers existed in `common/event_modifiers/verne_overhaul_modifiers.txt`, but not all of their visible name/description strings were present in Verne overhaul loc.
- No mission logic changed; this was a live-quality UI/tooltip completeness fix.

## Night session notes (2026-04-03)

### Real bugs fixed this session
- **7 duplicate loc keys removed** from `verne_overhaul_l_english.yml` (EU4 randomly picks one when duplicates exist). Duplicates were introduced by the "NEW MISSIONS" append block.
- **verne_overhaul_advisor.1.d collision** — event option name `verne_overhaul_advisor.1.d` conflicted with event desc key `verne_overhaul_advisor.1.d`. Renamed option to `verne_overhaul_advisor.1.d_wyvern`.
- **39 missing mission name loc entries added** — all `name` values from `Verne_Missions.txt` now have loc entries.
- **30 redundant additions reverted** — discovered that `verne_overhaul_l_english.yml` loads BEFORE `Flavour_Verne_A33_l_english.yml` (vanilla). Vanilla overwrites any duplicate keys at runtime. 30 mission reward modifier name entries were removed (they were redundant with vanilla). Kept only 12 province/location names that genuinely don't exist in vanilla, plus `verne_dynasty_protected_court(_desc)`.

### Slots 6–9 — NOT A BUG (corrected)
- Earlier analysis was wrong. `max_slots_horizontal = 5` is correct.
- Mission slot distribution: slot 1 = 7, slot 2 = 20, slot 3 = 4, slots 4–5 = 0 missions.
- Only slots 1–3 have assigned missions. Slots 6–9 are empty container definitions (not actual slots with content). `max_slots_horizontal = 5` means the UI shows up to 5 columns, which covers all missions.

### Smoke check results
- All 6/6 smoke checks pass
- Event ID audit: 122 IDs checked, 0 issues
- Localization audit: 1195 keys indexed, 0 duplicate keys
- Markdown link audit: 206 local links checked, 0 issues

### Files changed this session
- `localisation/verne_overhaul_l_english.yml` — loc additions, duplicate removals, advisor fix
- `events/verne_overhaul_advisor_events.txt` — option name collision fix
- `docs/status/verne-live-implementation-status.md` — status update

## Morning content pass (2026-04-03)

- Replaced the remaining placeholder stub mission descriptions in `localisation/verne_overhaul_l_english.yml` for existing legacy/base Verne mission IDs.
- Verified there are now **0** remaining `Verne mission:` placeholder descriptions in the Verne overhaul loc file.
- This was a live-quality improvement to mission presentation/localization coverage, not a mission-script rewrite.

## Single best next gameplay task

**Audit `missions/Verne_Missions.txt` against the live doctrine / reform / dynasty / order / crisis helper state and correct integration mismatches.**

Why this is next:
- Verne already has broad mechanical implementation.
- Campaign quality now depends more on mission-spine integration than on adding more breadth.
- This is the most direct way to improve real playability instead of just increasing object count.
