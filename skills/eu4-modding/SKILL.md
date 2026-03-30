---
name: eu4-modding
description: Help with Europa Universalis IV modding workflows, especially scripting, events, decisions, missions, modifiers, localisation, file structure, debugging common Paradox script mistakes, and safe repository editing for EU4 mods. Use when working on an EU4 mod, balancing game content, adding scripted content, or reviewing Paradox-format files and localisation.
---

# EU4 Modding

Use this skill when working on Europa Universalis IV mods.

## Core workflow

1. Identify the mod root and relevant folders before editing.
2. Preserve Paradox plaintext formatting and existing indentation style.
3. Check related files together:
   - script/content file
   - localisation file
   - descriptors or metadata if relevant
4. When adding content, keep namespacing consistent to avoid collisions.
5. Flag likely gameplay-balance or syntax risks clearly.

## Common folders

Look for these common EU4 paths:
- `common/`
- `events/`
- `decisions/`
- `missions/`
- `history/`
- `localisation/`
- `gfx/`
- `interface/`

## Editing rules

- Keep keys stable and unique.
- Do not rename IDs casually.
- Update localisation when adding player-facing text.
- Keep scripted triggers/effects readable with one condition per line when possible.
- Prefer small targeted edits over broad rewrites.

## Debugging checklist

When something seems broken, check in this order:
1. unmatched braces
2. wrong scope/root/from usage
3. misspelled script keys
4. missing localisation
5. wrong file placement
6. duplicate IDs or keys
7. unsupported syntax for EU4 version/mod setup

## Balance/design guidance

- Avoid stacking too many permanent bonuses without tradeoffs.
- Keep AI behavior in mind when adding decisions, missions, and events.
- Mention likely exploit risks when they appear.

## Repo workflow

When the mod is in git:
- inspect status before editing
- keep commits focused
- summarize gameplay and technical changes separately when helpful
