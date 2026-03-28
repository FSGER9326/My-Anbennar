# Verne Canonical vs Legacy File Registry

Status date: 2026-03-28  
Owner: Docs governance / Verne overhaul maintainers

## Purpose

This registry is the **single documentation source of truth** for which Verne-related files are currently canonical, transitional, or legacy.

Use it to prevent duplicate edits across overlapping Verne scaffolds and legacy anchors.

## Classification rules

- **Canonical**: primary file to edit for current behavior in that subsystem.
- **Transitional**: active but expected to be merged/replaced during ongoing migration.
- **Legacy (do not extend)**: retained for compatibility/history; avoid adding new behavior.
- **Deprecated candidate**: slated for deletion once replacement acceptance criteria are met.

## Verne implementation registry

| Domain | File | Status | Edit policy | Why this status / conflict note |
|---|---|---|---|---|
| Country flavor baseline | `events/Flavour_Verne_A33.txt` | Canonical | Patch carefully in-place for base Anbennar Verne behavior that still drives gameplay. | Still the authoritative legacy flavor/event anchor referenced in roadmap and audits. |
| Mission spine | `missions/Verne_Missions.txt` | Canonical | Primary mission implementation file for Verne. | Existing mission progression remains rooted here; overhaul mission rewrites should land here unless explicitly split. |
| Overhaul reusable helpers | `common/event_modifiers/verne_overhaul_modifiers.txt` | Canonical | Add reusable modifiers here. | Dedicated helper layer for overhaul states; covered by smoke checks. |
| Overhaul reusable helpers | `common/scripted_triggers/verne_overhaul_triggers.txt` | Canonical | Add cross-system Verne triggers here unless explicitly dynasty-only. | Main trigger library for overhaul and mission-route logic. |
| Overhaul reusable helpers | `common/scripted_effects/verne_overhaul_effects.txt` | Canonical | Add reusable overhaul effects here. | Canonical shared effect layer for new Verne implementation slices. |
| Overhaul doctrine content | `common/ideas/verne_doctrine_groups.txt` | Canonical | Add/modify doctrine groups here. | Primary overhaul doctrine object file, already tracked by validation sentinels. |
| Overhaul policies | `common/policies/verne_doctrine_policies.txt` | Canonical | Add doctrine policy objects here. | Dedicated policy file for overhaul doctrine expansion. |
| Overhaul reforms | `common/government_reforms/verne_overhaul_reforms.txt` | Canonical | Add/modify overhaul reforms here. | Dedicated reform layer with mandatory sentinels in smoke profile. |
| Overhaul decisions | `decisions/verne_overhaul_decisions.txt` | Canonical | Keep as primary overhaul decision file. | Intended decision anchor for dynasty/court overhaul milestones. |
| Overhaul on_actions | `common/on_actions/verne_overhaul_on_actions.txt` | Canonical | Primary owner for live Verne dynasty safeguard hook dispatch. | Implementation comments mark this file as the single source of truth for Verne overhaul on_actions. |
| Overhaul on_actions scaffold shell | `common/on_actions/zz_verne_overhaul_on_actions.txt` | Legacy (do not extend) | Retired stub only; **do not extend retired stubs**. | Migration note retires this scaffold shell in favor of `common/on_actions/verne_overhaul_on_actions.txt`. |
| Dynasty subsystem on_actions duplicate | `common/on_actions/zzz_verne_overhaul_dynasty_on_actions.txt` | Legacy (do not extend) | Retired stub only; **do not extend retired stubs**. | Migration note retires this duplicate after consolidation to non-`zzz` on_actions ownership. |
| Overhaul dynasty events | `events/verne_overhaul_dynasty_events.txt` | Canonical (dynasty subsystem) | Primary owner for live `verne_overhaul_dynasty.*` implementation. | File header explicitly states this is the single source of truth and that `events/zzz_verne_overhaul_dynasty_events.txt` is retired. |
| Dynasty subsystem events duplicate | `events/zzz_verne_overhaul_dynasty_events.txt` | Legacy (do not extend) | Retired stub only; **do not extend retired stubs**. | Migration note retires this duplicate after moving live logic to `events/verne_overhaul_dynasty_events.txt`. |
| Overhaul triggers (including dynasty safeguards) | `common/scripted_triggers/verne_overhaul_triggers.txt` | Canonical | Add/maintain dynasty safeguard triggers in the shared non-`zzz` trigger library. | Migration note consolidates dynasty safeguard triggers into this file. |
| Dynasty trigger split duplicate | `common/scripted_triggers/zzz_verne_overhaul_dynasty_triggers.txt` | Legacy (do not extend) | Retired stub only; **do not extend retired stubs**. | Legacy split retained for migration traceability; active ownership moved to `common/scripted_triggers/verne_overhaul_triggers.txt`. |
| Overhaul localization (general) | `localisation/verne_overhaul_l_english.yml` | Canonical | Add non-scaffold overhaul localization here. | Primary localization namespace for reusable modifiers/tooltips/doctrine/reforms. |
| Scaffold localization | `localisation/verne_overhaul_scaffold_l_english.yml` | Legacy (do not extend) | Freeze except when retiring scaffold keys. | Contains placeholder text; superseded by live localization files for implemented systems. |
| Dynasty localization | `localisation/verne_overhaul_dynasty_l_english.yml` | Canonical (dynasty subsystem) | Primary owner for live dynasty safeguard event localisation keys. | Migration note consolidates dynasty localisation ownership here. |
| Dynasty localization duplicate | `localisation/zzz_verne_overhaul_dynasty_l_english.yml` | Legacy (do not extend) | Retired stub only; **do not extend retired stubs**. | Legacy duplicate retained as migration record; active keys live in `localisation/verne_overhaul_dynasty_l_english.yml`. |
| Prototype doctrine ideas | `common/ideas/verne_proto_adventure_ideas.txt` | Legacy (do not extend) | Do not add new production behavior; migrate needed patterns into canonical doctrine files. | Prototype artifact; superseded by structured doctrine rollout files. |
| Prototype doctrine policies | `common/policies/verne_proto_doctrine_expedition_policy.txt` | Legacy (do not extend) | Freeze and replace through canonical policy layer when needed. | Early prototype/scratch policy file outside canonical doctrine policy path. |

## Migration guardrails

1. **No dual-live edits:** if a subsystem has both scaffold and `zzz` dynasty files, pick one canonical path per commit.
2. **No new placeholder keys:** new production text belongs in `localisation/verne_overhaul_l_english.yml` or `localisation/verne_overhaul_dynasty_l_english.yml`, not scaffold localization.
3. **Promotions must be explicit:** when moving a transitional file to canonical, update this registry and the docs hubs in the same commit.

## Update protocol

When introducing, retiring, or reclassifying Verne files:

1. update this registry first,
2. update links in docs hubs,
3. run docs/link and Verne smoke checks,
4. include the registry delta in the PR summary.
