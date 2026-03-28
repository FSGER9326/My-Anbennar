# Verne Overhaul Scaffold Checklist

Status date: 2026-03-28

## Scaffolded (inert/no-op)
- [x] `common/policies/verne_doctrine_policies.txt` includes `verne_placeholder_doctrine_policy` (disabled by `always = no`).
- [x] `decisions/verne_overhaul_decisions.txt` includes `verne_placeholder_overhaul_decision` (disabled by `always = no`).
- [x] `events/verne_overhaul_dynasty_events.txt` includes `namespace = verne_overhaul_dynasty` plus placeholder event `verne_overhaul_dynasty.1`.
- [x] `common/on_actions/zz_verne_overhaul_on_actions.txt` includes placeholder `on_new_heir` hook shell.
- [x] `localisation/verne_overhaul_scaffold_l_english.yml` contains matching placeholder localization keys.

## Not feature-complete yet
- [ ] V-13 first-wave policy layer implementation
- [x] V-17 dynasty safeguard chain implementation (canonicalized to non-`zzz_` files)
- [ ] V-18 core dynastic decisions implementation

## Safety expectation
Remaining unchecked scaffold items should stay inert/no-op until their milestone implementation starts.

The V-17 dynasty safeguard is now intentionally live in canonical files.
