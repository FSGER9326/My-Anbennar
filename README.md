# Verne Overhaul Project

This repository contains the Verne overhaul work inside an Anbennar/EU4 mod workspace.

## Main areas

- [docs/README.md](docs/README.md): project planning, design docs, grounding rules, and local reference material
- [common](common): core scripted objects such as ideas, reforms, modifiers, mercs, triggers, and effects
- [missions](missions): mission trees
- [events](events): event content
- [decisions](decisions): decision content
- [localisation](localisation): localization files

## Current project docs

If you want the current design-and-build layer, start here:

- [current-work-queue.md](docs/wiki/current-work-queue.md)
- [mod-spec.md](docs/mod-spec.md)
- [implementation-roadmap.md](docs/implementation-roadmap.md)
- [first-wave-backlog.md](docs/first-wave-backlog.md)
- [design/README.md](docs/design/README.md)

## Working rule

Implementation should follow this order:

1. read the existing Anbennar repo files
2. check the relevant design doc
3. use the grounding checklist before editing shared systems
4. use the local EU4 wiki snapshots only as reference, not as a replacement for repo patterns
