# Repo Rescan Playbook (Mechanics-Difference Focus)

This playbook is for repeat full-repo scanning with one goal:

- document where Anbennar differs from base EU4 mechanics in implementation terms

## 1) Rescan scope rule

Do scans by mechanic family, not by random folder browsing.

Recommended pass order:

1. estates + privileges
2. government mechanics + reforms wiring
3. diplomacy + peace extensions
4. rebels + disasters
5. units + military subsystems
6. religion layers used by Verne design

## 2) What each scan must produce

For each family, produce or update:

- one repo-map article
- one row in `anbennar-vs-eu4-mechanics-gap-register.md`
- one row in `docs/wiki/anbennar-base-vs-verne-change-ledger.md` if the family impacts active implementation

## 3) Minimum evidence checklist

Every new article should include:

- vanilla expectation summary (short)
- Anbennar implementation deltas (short)
- exact repo anchors (files + key objects)
- adaptation advice for Verne
- upstream update risk notes

## 4) Link hygiene rule

In the same commit as a new article, update:

1. `docs/repo-maps/README.md`
2. `docs/repo-maps/anbennar-systems-master-index.md`
3. `docs/repo-maps/anbennar-systems-scan-roadmap.md`

This prevents orphan docs and conflict-prone follow-up commits.
