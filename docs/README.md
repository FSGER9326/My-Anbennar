# Project Docs

This folder holds the working project documentation for the Verne overhaul.

Use it as the main non-code workspace for planning, design, grounding, and local reference material.

## What lives here

### New? Start here
- [start-here.md](./start-here.md)

### Planning
- [mod-spec.md](./mod-spec.md)
- [implementation-roadmap.md](./implementation-roadmap.md)
- [first-wave-backlog.md](./first-wave-backlog.md)

These files answer:

- what the overhaul is trying to become
- what order we should build it in
- what the next concrete tasks are

### Working rules
- [../AGENTS.md](../AGENTS.md)
- [codex-grounding-checklist.md](./codex-grounding-checklist.md)
- [automation/pre-pr-artifact-flow.md](./automation/pre-pr-artifact-flow.md)
- [references/reference-index.md](./references/reference-index.md)

These files keep implementation grounded in:

- the real Anbennar repo
- the local EU4 wiki snapshots
- explicit compatibility checks before editing

### Design layer
- [design/README.md](./design/README.md)

The `design/` folder is the structured GitHub-friendly design layer.

### Repo grounding maps
- [repo-maps/README.md](./repo-maps/README.md)

The `repo-maps/` folder records how existing Anbennar systems are actually implemented in the repo.

### Local references
- [references/README.md](./references/README.md)
- [references/eu4-wiki](./references/eu4-wiki)

### Maintenance wiki
- [wiki/README.md](./wiki/README.md)
- [wiki/high-value-non-modding-eu4-wiki-topics.md](./wiki/high-value-non-modding-eu4-wiki-topics.md)
- [wiki/noob-friendly-doc-naming-convention.md](./wiki/noob-friendly-doc-naming-convention.md)
- [wiki/checklist-automation-system.md](./wiki/checklist-automation-system.md)
- [wiki/merge-conflict-prevention-playbook.md](./wiki/merge-conflict-prevention-playbook.md)
- [wiki/parallelization-lanes-playbook.md](./wiki/parallelization-lanes-playbook.md)
- [wiki/checklist-automation-blindspots-changelog.md](./wiki/checklist-automation-blindspots-changelog.md)
- [wiki/verne-canonical-vs-legacy-file-registry.md](./wiki/verne-canonical-vs-legacy-file-registry.md)

Use this for long-term change tracking, upstream-update adaptation, and beginner-friendly conventions.

## Suggested use order

Use this sequence to avoid bouncing between overlapping docs:

1. **Start point:** [start-here.md](./start-here.md) for the minimal entry flow.
2. **Command/index layer:** [wiki/checklist-automation-system.md](./wiki/checklist-automation-system.md) for operational commands only.
3. **Ownership truth layer:** [wiki/verne-canonical-vs-legacy-file-registry.md](./wiki/verne-canonical-vs-legacy-file-registry.md) for canonical-vs-legacy file ownership.
4. **Then deep-dive by need:** design docs, planning docs, and references.

## Documentation organization recommendations

If the repo feels crowded, a practical structure is:

- **`docs/design/`**: intended mechanics and design decisions
- **`docs/repo-maps/`**: implementation anchors and code-grounded patterns
- **`docs/references/`**: static external references (EU4 snapshots)
- **`docs/planning/`** *(optional future move)*: sequencing docs like roadmap/backlog/specs

For low-risk cleanup, move files gradually and keep redirects/index links updated in the same commit.
