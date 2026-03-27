# Project Docs

This folder holds the working project documentation for the Verne overhaul.

Use it as the main non-code workspace for planning, design, grounding, and local reference material.

## What lives here

### Planning
- [mod-spec.md](./mod-spec.md)
- [implementation-roadmap.md](./implementation-roadmap.md)
- [first-wave-backlog.md](./first-wave-backlog.md)

These files answer:

- what the overhaul is trying to become
- what order we should build it in
- what the next concrete tasks are

### Working rules
- [codex-grounding-checklist.md](./codex-grounding-checklist.md)
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

## Suggested use order

1. Check real repo files.
2. Check the grounding checklist.
3. Check the relevant design doc.
4. Check local EU4 wiki snapshots if syntax or engine rules are unclear.

## Documentation organization recommendations

If the repo feels crowded, a practical structure is:

- **`docs/design/`**: intended mechanics and design decisions
- **`docs/repo-maps/`**: implementation anchors and code-grounded patterns
- **`docs/references/`**: static external references (EU4 snapshots)
- **`docs/planning/`** *(optional future move)*: sequencing docs like roadmap/backlog/specs

For low-risk cleanup, move files gradually and keep redirects/index links updated in the same commit.
