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
- [ ] V-17 dynasty safeguard chain implementation
- [ ] V-18 core dynastic decisions implementation

## Safety expectation
All above scaffolds are intentionally inert and should remain no-op until milestone implementation work starts.
