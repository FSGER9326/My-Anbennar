# Verne Lore Support Library

This folder is a **practical lore layer** for implementation support.

It is intentionally separate from:

- `docs/design/` (design truth)
- `docs/repo-maps/` (implementation truth)
- `docs/references/` (engine/syntax truth)

## Status policy

Each lore file should carry a status tag:

- **CANONICAL_LORE**: grounded in existing repo/design references and stable for writing.
- **WORKING_LORE**: useful implementation draft, still open to revision.
- **NEEDS_SOURCE_EXPANSION**: placeholders waiting for stronger repo/lore sourcing.

## Current lore docs

- [verne-identity-and-court-culture.md](./verne-identity-and-court-culture.md)
- [verne-religion-rivals-and-overseas-imaginary.md](./verne-religion-rivals-and-overseas-imaginary.md)

## How to use with implementation docs

1. Pick a system in `docs/implementation-crosswalk.md`.
2. Read the design doc for intended behavior.
3. Read the repo-map for implementation pattern.
4. Use this lore layer for naming/tone/flavor text and event voice.
5. Keep mechanics in implementation files, lore in lore files.
