# Verne Overhaul Scaffold Checklist

Status date: 2026-03-28

## Scaffolded (inert/no-op)
- [x] `common/policies/verne_doctrine_policies.txt` includes `verne_placeholder_doctrine_policy` (disabled by `always = no`).
- [x] `decisions/verne_overhaul_decisions.txt` includes `verne_placeholder_overhaul_decision` (disabled by `always = no`).

## Implemented (authoritative active path)
- [x] `events/verne_overhaul_dynasty_events.txt` owns `namespace = verne_overhaul_dynasty` and active safeguard event `verne_overhaul_dynasty.1`.
- [x] `common/on_actions/verne_overhaul_on_actions.txt` owns active `on_new_heir` hook dispatch.
- [x] `common/scripted_triggers/verne_overhaul_triggers.txt` owns dynasty safeguard triggers (`verne_overhaul_*heir*`).
- [x] `localisation/verne_overhaul_dynasty_l_english.yml` owns dynasty safeguard event localization keys.

## Retired (kept inert to prevent accidental reactivation)
- [x] `events/zzz_verne_overhaul_dynasty_events.txt`
- [x] `common/on_actions/zz_verne_overhaul_on_actions.txt`
- [x] `common/on_actions/zzz_verne_overhaul_dynasty_on_actions.txt`
- [x] `common/scripted_triggers/zzz_verne_overhaul_dynasty_triggers.txt`
- [x] `localisation/zzz_verne_overhaul_dynasty_l_english.yml`

## Not feature-complete yet
- [ ] V-13 first-wave policy layer implementation
- [ ] V-18 core dynastic decisions implementation

## Migration note
- See `docs/wiki/verne-dynasty-overhaul-migration.md` for old->new ownership and behavior delta.
