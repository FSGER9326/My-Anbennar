# Noob-Friendly Documentation Naming Convention

Goal: make docs readable at a glance for new contributors.

## Rules

1. Use descriptive kebab-case names.
2. Put document type at the end.
3. Keep one meaning per suffix.
4. Avoid abbreviations unless universally obvious.

## Suffix meanings

- `-reference.md` → implementation map / code anchors
- `-playbook.md` → workflow/how-to
- `-ledger.md` → ongoing change tracking table
- `-roadmap.md` → sequencing and milestones
- `README.md` → folder entry point

## Examples

- `anbennar-base-vs-verne-change-ledger.md`
- `upstream-update-adaptation-playbook.md`
- `custom-government-mechanics-and-gui-patterns-reference.md`

## Transition rule

Do not mass-rename existing files in one big PR.

If a rename is needed, do it in small batches and immediately update links in:

- `docs/README.md`
- folder `README.md`
- `docs/implementation-crosswalk.md` (if referenced)
