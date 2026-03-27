# EU4 Baseline vs Anbennar Comparison Notes (Mechanics Scan Support)

This file tracks baseline engine/reference checks while scanning Anbennar custom systems.

## Scope and source policy

Trust order remains:

1. repo implementation truth (`common/*`, `events/*`, etc.)
2. local EU4 wiki snapshots under `docs/references/eu4-wiki/`
3. live online wiki checks when accessible

## Government mechanics baseline

Local EU4 wiki snapshot confirms government mechanics are attached via `government_abilities` and scripted in `common/government_mechanics`.

Useful local anchor:

- `docs/references/eu4-wiki/Government modding - Europa Universalis 4 Wiki.html` (contains `government_abilities` guidance and points to government mechanic modding).

Anbennar delta observed:

- high volume of custom mechanic IDs
- repeated activation across custom reform families
- heavy coupling with non-vanilla systems (magic/estates/tag-specific mechanics)

## Estate baseline

Local EU4 estate modding snapshot confirms standard privilege skeleton and estate privilege file architecture.

Useful local anchor:

- `docs/references/eu4-wiki/Estate modding - Europa Universalis 4 Wiki.html`

Anbennar delta observed:

- deep organization/law privilege ecosystems
- extensive `on_granted`/`on_invalid` cleanup and cross-estate lockouts
- mission/event synchronization of privilege state

## Mercenary baseline

Local EU4 mercenary modding snapshot provides baseline company structure and triggers.

Useful local anchor:

- `docs/references/eu4-wiki/Mercenaries modding - Europa Universalis 4 Wiki.html`

Anbennar delta observed:

- custom merc templates tied to mission flags, estates, and nation narrative chains
- multiple specialized company families (baseline pool + elite/special files)

## Great project / monument baseline

Local EU4 snapshot provides generic great project modding structure.

Useful local anchor:

- `docs/references/eu4-wiki/Great project modding - Europa Universalis 4 Wiki.html`

Anbennar delta observed:

- monument state often tied to mission and event-driven transformations
- project IDs and build triggers are frequently embedded into nation-specific progression logic

## Live online check status (2026-03-27)

Attempted direct live access to:

- `https://eu4.paradoxwikis.com/Government_modding`
- `https://eu4.paradoxwikis.com/Estate_modding`
- `https://eu4.paradoxwikis.com/Mercenaries_modding`
- `https://eu4.paradoxwikis.com/Great_project_modding`

Result in this environment: challenge page requiring JavaScript prevented content retrieval.

Implication:

- keep relying on local snapshots plus repo evidence for now
- mark any live-wiki-only validation requests as `NEEDS_REPO_CHECK` until live fetch is available

## Related docs

- [./reference-index.md](./reference-index.md)
- [../repo-maps/government-mechanic-activation-map-by-reform-reference.md](../repo-maps/government-mechanic-activation-map-by-reform-reference.md)
- [../repo-maps/custom-estate-and-privilege-ecosystems-reference.md](../repo-maps/custom-estate-and-privilege-ecosystems-reference.md)
- [../repo-maps/verne-wyvern-orders-mercs-and-monuments-reference.md](../repo-maps/verne-wyvern-orders-mercs-and-monuments-reference.md)
