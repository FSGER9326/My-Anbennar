# Project Docs

This folder holds the working project documentation for the Verne overhaul.

Use it as the main non-code workspace for planning, design, grounding, and local reference material.

## What Lives Here

### Planning
- [mod-spec.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/mod-spec.md)
- [implementation-roadmap.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/implementation-roadmap.md)
- [first-wave-backlog.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/first-wave-backlog.md)

These files answer:

- what the overhaul is trying to become
- what order we should build it in
- what the next concrete tasks are

### Working rules
- [codex-grounding-checklist.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/codex-grounding-checklist.md)
- [eu4-local-reference-index.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/eu4-local-reference-index.md)

These files exist to keep implementation grounded in:

- the real Anbennar repo
- the local EU4 wiki snapshots
- explicit compatibility checks before editing

### Design layer
- [design/README.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/README.md)

The `design/` folder is the structured GitHub-friendly design layer built from the theorycraft document.

It includes:

- doctrine and national-idea specs
- reforms
- mission rewrites
- dynasty and court systems
- orders, monuments, and mercs
- pressure, disasters, and Corinite material
- implementation scaffolding
- a source-coverage matrix

### Repo grounding maps
- [repo-maps/README.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/repo-maps/README.md)

The `repo-maps/` folder records how existing Anbennar systems are actually implemented in the repo so future changes can mirror real patterns instead of guessing.

It now includes:

- Verne overseas system maps
- a master index of non-vanilla Anbennar systems
- a first-pass magic systems reference
- a broader non-magic systems overview
- a roadmap for future deep-scan articles

### Local references
- [references/eu4-wiki](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/references/eu4-wiki)

This is the saved EU4 wiki snapshot bundle used as a local reference set.

## Suggested use order

1. check the real repo files
2. check the grounding checklist
3. check the relevant design doc
4. check the local EU4 wiki snapshot if syntax or engine rules are unclear

## Repo cleanup note

Documentation and reference material should live under `docs/` when possible so the repo root stays focused on actual mod content.
