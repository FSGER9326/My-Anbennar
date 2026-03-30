# Verne Wiki (Maintenance Docs)

This folder is the long-term maintenance wiki for your mod.

Use it to track:

- what is base Anbennar behavior
- what Verne changes on top
- exactly where each change is implemented
- what to re-check when Anbennar updates

## Files

- [anbennar-base-vs-verne-change-ledger.md](./anbennar-base-vs-verne-change-ledger.md)
- [upstream-update-adaptation-playbook.md](./upstream-update-adaptation-playbook.md)
- [high-value-non-modding-eu4-wiki-topics.md](./high-value-non-modding-eu4-wiki-topics.md)
- [noob-friendly-doc-naming-convention.md](./noob-friendly-doc-naming-convention.md)
- [generalized-modding-lifecycle-playbook.md](./generalized-modding-lifecycle-playbook.md)
- [fluff-and-art-production-playbook.md](./fluff-and-art-production-playbook.md)
- [checklist-automation-system.md](./checklist-automation-system.md)
- [merge-conflict-prevention-playbook.md](./merge-conflict-prevention-playbook.md)
- [checklist-automation-blindspots-changelog.md](./checklist-automation-blindspots-changelog.md)
- [verne-id-ledger.md](./verne-id-ledger.md)
- [verne-canonical-vs-legacy-file-registry.md](./verne-canonical-vs-legacy-file-registry.md)


## Current priority order (when unsure)

1. **Grounding first**: confirm repo-map anchor coverage for the exact target.
2. **Plan second**: define `v0.1` scope + touched-file list + smoke checks.
3. **Implement third**: one thin slice at a time.
4. **Theory-craft only when blocked**: design discussion should unblock concrete implementation decisions.
5. **Naming/structure cleanup last**: doc organization cleanups should not block active mechanic work.

This ordering is intentional: correctness and momentum first, large-scale doc polish second.


## Session-output standard (for every work session)

End each session with:

1. **What changed** (files and features)
2. **Why it matters** (gameplay/maintenance impact)
3. **Risk notes** (what could break)
4. **Checks run** (exact commands)

Minimum automation check for Verne work:
- `./scripts/verne_smoke_checks.sh`
- `./scripts/verne_checklist_audit.py`
- `./scripts/checklist_link_audit.py`

Generic scaling command for a new country workflow:
- `./scripts/new_country_scaffold.sh <country-slug> <TAG>`

This keeps collaboration understandable for contributors who did not write the change.

## Rule for future sessions

When adding or changing mechanics, update the ledger in the same commit.
