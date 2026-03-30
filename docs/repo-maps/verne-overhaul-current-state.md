# Verne Overhaul Current State (Conflict-Aware Reference)

Status date: 2026-03-29  
Owner: Verne overhaul maintainers (reference lane)

## Purpose

This reference snapshots **current canonical ownership** and **parallel-work boundaries** for Verne overhaul implementation so contributors can pick low-conflict tasks quickly.

Primary truth inputs used for this map:
- `docs/wiki/verne-canonical-vs-legacy-file-registry.md`
- `automation/conflict_hotspots.yaml`
- `docs/wiki/parallelization-lanes-playbook.md`
- `docs/wiki/merge-conflict-prevention-playbook.md`
- `scripts/pre_pr_gate.sh`

## Canonical gameplay owners (live implementation path)

| System slice | Canonical owner file(s) | Notes |
|---|---|---|
| Verne flavor baseline | `events/Flavour_Verne_A33.txt` | Existing base flavor/events still drive baseline gameplay behavior. |
| Mission spine | `missions/Verne_Missions.txt` | Primary mission progression owner for Verne. |
| Reusable trigger helper layer | `common/scripted_triggers/verne_overhaul_triggers.txt` | Shared trigger library, including dynasty safeguard triggers. |
| Reusable effect helper layer | `common/scripted_effects/verne_overhaul_effects.txt` | Shared effect library for overhaul slices. |
| Reusable modifier helper layer | `common/event_modifiers/verne_overhaul_modifiers.txt` | Canonical reusable modifier ownership. |
| Doctrine groups | `common/ideas/verne_doctrine_groups.txt` | Canonical doctrine group objects. |
| Doctrine policies | `common/policies/verne_doctrine_policies.txt` | Canonical policy ownership, but currently placeholder-only. |
| Reforms | `common/government_reforms/verne_overhaul_reforms.txt` | Canonical overhaul reforms. |
| Decisions | `decisions/verne_overhaul_decisions.txt` | Canonical decision ownership, but currently placeholder-only. |
| Overhaul on_actions | `common/on_actions/verne_overhaul_on_actions.txt` | Canonical on_actions dispatch owner. |
| Dynasty events | `events/verne_overhaul_dynasty_events.txt` | Canonical `verne_overhaul_dynasty.*` event owner. |
| Overhaul localization (general) | `localisation/verne_overhaul_l_english.yml` | Canonical non-scaffold localisation namespace. |
| Dynasty localization | `localisation/verne_overhaul_dynasty_l_english.yml` | Canonical dynasty safeguard localisation owner. |

## Live helper files (single-writer gameplay helper surfaces)

Treat these as **one-active-PR helper surfaces** during parallel gameplay planning:

- `common/scripted_triggers/verne_overhaul_triggers.txt`
- `common/scripted_effects/verne_overhaul_effects.txt`
- `localisation/verne_overhaul_l_english.yml`

If one active gameplay branch touches any file above, other gameplay branches should either avoid these files or stack onto that same branch.

## Scaffold files still pending / non-live placeholders

These files are canonical ownership targets but still scaffold/placeholder for first-wave gameplay:

- `common/policies/verne_doctrine_policies.txt` (`verne_placeholder_doctrine_policy` only)
- `decisions/verne_overhaul_decisions.txt` (`verne_placeholder_overhaul_decision` only)

Legacy scaffold/duplicate files that should stay frozen (do not extend):

- `common/on_actions/zz_verne_overhaul_on_actions.txt`
- `common/on_actions/zzz_verne_overhaul_dynasty_on_actions.txt`
- `events/zzz_verne_overhaul_dynasty_events.txt`
- `common/scripted_triggers/zzz_verne_overhaul_dynasty_triggers.txt`
- `localisation/verne_overhaul_scaffold_l_english.yml`
- `localisation/zzz_verne_overhaul_dynasty_l_english.yml`
- `common/ideas/verne_proto_adventure_ideas.txt`
- `common/policies/verne_proto_doctrine_expedition_policy.txt`

## Hard "do not parallelize" file list

These are single-writer surfaces from `automation/conflict_hotspots.yaml` and should be treated as serial ownership while active work is in flight:

- `docs/start-here.md`
- `docs/wiki/checklist-automation-system.md`
- `automation/conflict_hotspots.yaml`
- `scripts/noob_autopilot.sh`
- `scripts/noob_autopilot.ps1`
- `scripts/pre_pr_gate.sh`
- `scripts/pre_pr_gate.ps1`
- `.github/workflows/*` (single-writer prefix)

Additionally, parallel gameplay tasks must not touch the same mission file, helper file, or localisation file at the same time.

## Recommended lane boundaries

Default lane split:

1. **Gameplay lane**: `common/`, `events/`, `missions/`, `decisions/`, `localisation/` gameplay implementation.
2. **Lore/docs lane**: lore/design/explanatory docs only (`docs/lore/`, `docs/design/`, dossiers, narrative docs).
3. **Reference lane**: repo-map/reference ownership docs (`docs/repo-maps/`, crosswalk references).
4. **Automation lane (serial)**: `automation/`, `scripts/`, `.github/workflows/`, and wiki workflow guides.

Coordination guardrails:
- Keep automation lane mostly serial.
- Keep one active task per lane by default.
- If overlap hits helper/mission/localisation or any single-writer file, stack instead of parallelizing.

## Branch naming pattern (recommended)

Use explicit lane-prefixed branch names to make overlap checks obvious in PR lists:

- `gameplay/verne-<slice>-<short-topic>`
- `lore-docs/<scope>-<short-topic>`
- `reference/<map-or-registry>-<short-topic>`
- `automation/<script-or-workflow>-<short-topic>`

Examples:
- `gameplay/verne-dynasty-heir-safeguard-tuning`
- `reference/verne-current-state-conflict-map-refresh`
- `automation/pre-pr-gate-overlap-check-hardening`

## Compact overlap matrix (safe vs blocked in parallel)

| Pair | Safe in parallel? | Why |
|---|---|---|
| Gameplay lane (`missions/Verne_Missions.txt`) + Lore/docs lane (`docs/lore/*`) | **Safe** | No shared gameplay/helper/localisation/single-writer files. |
| Gameplay lane (no helper/localisation edits) + Reference lane (`docs/repo-maps/*`) | **Usually safe** | Safe when gameplay slice avoids helper hotspots and single-writer docs. |
| Lore/docs lane + Reference lane | **Safe** | Distinct doc surfaces if they avoid same hotspot file. |
| Gameplay PR A touching `common/scripted_triggers/verne_overhaul_triggers.txt` + Gameplay PR B touching `missions/Verne_Missions.txt` | **Blocked** | Helper-touching gameplay work must not run in parallel with separate mission edits. |
| Gameplay PR A touching `localisation/verne_overhaul_l_english.yml` + Gameplay PR B touching any localisation file for same feature slice | **Blocked** | Localisation files are explicit no-parallel overlap surfaces. |
| Any lane + Automation lane edits to `scripts/pre_pr_gate.sh` | **Blocked** | `scripts/pre_pr_gate.sh` is single-writer. |
| Any lane + Workflow edits under `.github/workflows/*` | **Blocked** | Workflow prefix is single-writer. |
| Reference lane (`docs/repo-maps/*`) + edits to `docs/start-here.md` in another branch | **Blocked** | `docs/start-here.md` is single-writer. |

## Validation hooks for this reference

Before PR:

- `python3 scripts/checklist_link_audit.py`
- `python3 scripts/docs_conflict_guard.py`
- Optional full gate: `bash scripts/pre_pr_gate.sh`

This document is intended to stay in sync with the hotspot registry and canonical-vs-legacy file registry; refresh both assumptions if those sources change.
