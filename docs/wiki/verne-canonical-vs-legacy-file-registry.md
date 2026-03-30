# Verne Canonical vs Legacy File Registry

Status date: 2026-03-29  
Owner: Docs governance / Verne overhaul maintainers

## Purpose

This registry is the **file-ownership truth source** for Verne-related implementation files.

## Status key

- **Canonical**: primary file currently owned for live behavior.
- **Transitional**: active file in migration, not final ownership target.
- **Legacy (do not extend)**: retained for compatibility/history only.
- **Deprecated candidate**: slated for removal after replacement acceptance.

## Verne file ownership registry

| Domain | File | Status | Edit policy | Ownership note |
|---|---|---|---|---|
| Country flavor baseline | `events/Flavour_Verne_A33.txt` | Canonical | Patch in place for base Anbennar Verne behavior still driving gameplay. | Authoritative legacy flavor/event anchor used by roadmap and audits. |
| Mission spine | `missions/Verne_Missions.txt` | Canonical | Primary mission implementation file for Verne. | Existing mission progression remains rooted here. |
| Overhaul reusable helpers | `common/event_modifiers/verne_overhaul_modifiers.txt` | Canonical | Add reusable modifiers here. | Dedicated overhaul modifier helper layer. |
| Overhaul reusable helpers | `common/scripted_triggers/verne_overhaul_triggers.txt` | Canonical | Add cross-system Verne triggers here unless explicitly dynasty-only. | Main trigger library for overhaul and mission-route logic. |
| Overhaul reusable helpers | `common/scripted_effects/verne_overhaul_effects.txt` | Canonical | Add reusable overhaul effects here. | Canonical shared effect layer for new Verne slices. |
| Overhaul doctrine content | `common/ideas/verne_doctrine_groups.txt` | Canonical | Add/modify doctrine groups here. | Primary overhaul doctrine object file. |
| Overhaul policies | `common/policies/verne_doctrine_policies.txt` | Canonical | Add doctrine policy objects here. | Dedicated policy ownership file for doctrine expansion. **Maturity:** placeholder-only at present (`verne_placeholder_doctrine_policy`), so first-wave policies are not implemented yet. |
| Overhaul reforms | `common/government_reforms/verne_overhaul_reforms.txt` | Canonical | Add/modify overhaul reforms here. | Dedicated reform ownership layer. |
| Overhaul decisions | `decisions/verne_overhaul_decisions.txt` | Canonical | Primary overhaul decision file. | Decision anchor for dynasty/court overhaul milestones. **Maturity:** placeholder-only at present (`verne_placeholder_overhaul_decision`), so first-wave decision gameplay is not implemented yet. |
| Overhaul on_actions | `common/on_actions/verne_overhaul_on_actions.txt` | Canonical | Primary owner for live Verne dynasty safeguard hook dispatch. | Consolidated single source of truth for overhaul on_actions. |
| Overhaul on_actions scaffold shell | `common/on_actions/zz_verne_overhaul_on_actions.txt` | Legacy (do not extend) | Retired stub only. | Ownership migrated to `common/on_actions/verne_overhaul_on_actions.txt`. |
| Dynasty subsystem on_actions duplicate | `common/on_actions/zzz_verne_overhaul_dynasty_on_actions.txt` | Legacy (do not extend) | Retired stub only. | Duplicate retired after consolidation to non-`zzz` owner. |
| Overhaul dynasty events | `events/verne_overhaul_dynasty_events.txt` | Canonical (dynasty subsystem) | Primary owner for live `verne_overhaul_dynasty.*` implementation. | Live dynasty event ownership target. |
| Dynasty subsystem events duplicate | `events/zzz_verne_overhaul_dynasty_events.txt` | Legacy (do not extend) | Retired stub only. | Duplicate retired after move to `events/verne_overhaul_dynasty_events.txt`. |
| Overhaul triggers (including dynasty safeguards) | `common/scripted_triggers/verne_overhaul_triggers.txt` | Canonical | Maintain dynasty safeguard triggers in shared non-`zzz` trigger library. | Consolidated trigger ownership target. |
| Dynasty trigger split duplicate | `common/scripted_triggers/zzz_verne_overhaul_dynasty_triggers.txt` | Legacy (do not extend) | Retired stub only. | Legacy split retained only as migration trace. |
| Overhaul localization (general) | `localisation/verne_overhaul_l_english.yml` | Canonical | Add non-scaffold overhaul localization here. | Primary localization namespace for reusable systems. |
| Scaffold localization | `localisation/verne_overhaul_scaffold_l_english.yml` | Legacy (do not extend) | Freeze except retirement cleanup. | Placeholder scaffold text only. |
| Dynasty localization | `localisation/verne_overhaul_dynasty_l_english.yml` | Canonical (dynasty subsystem) | Primary owner for live dynasty safeguard localization keys. | Live dynasty localization ownership target. |
| Dynasty localization duplicate | `localisation/zzz_verne_overhaul_dynasty_l_english.yml` | Legacy (do not extend) | Retired stub only. | Duplicate retained only as migration record. |
| Prototype doctrine ideas | `common/ideas/verne_proto_adventure_ideas.txt` | Legacy (do not extend) | Do not add new production behavior. | Prototype artifact superseded by doctrine rollout files. |
| Prototype doctrine policies | `common/policies/verne_proto_doctrine_expedition_policy.txt` | Legacy (do not extend) | Freeze and replace via canonical policy layer when needed. | Early prototype policy outside canonical doctrine path. |

## Current live surface (implemented objects only, 2026-03-29)

- `common/ideas/verne_doctrine_groups.txt`: `verne_doctrine_silver_wake`.
- `common/government_reforms/verne_overhaul_reforms.txt`: `verne_court_of_silver_oaths_reform`, `verne_charter_of_great_captains_reform`, `verne_ducal_muster_of_armoc_reform`.
- `common/on_actions/verne_overhaul_on_actions.txt`: `on_new_heir` dispatches to `verne_overhaul_dynasty.1`.
- `events/verne_overhaul_dynasty_events.txt`: `country_event` `verne_overhaul_dynasty.1`.
- `common/scripted_triggers/verne_overhaul_triggers.txt`: `verne_overhaul_should_run_heir_safeguard_trigger` (and dependent safeguard triggers).

Non-live scaffold note: canonical policy/decision ownership files above are still placeholder-only and must not be interpreted as first-wave completion.
