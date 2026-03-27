# Start Here (Noob-Friendly)

If you are new to GitHub and modding, read in this order:

1. [docs/README.md](./README.md)
2. [docs/wiki/README.md](./wiki/README.md)
3. [docs/wiki/anbennar-base-vs-verne-change-ledger.md](./wiki/anbennar-base-vs-verne-change-ledger.md)
4. [docs/implementation-crosswalk.md](./implementation-crosswalk.md)
5. one matching article from [docs/repo-maps/README.md](./repo-maps/README.md)

## Tiny glossary (modding terms, not GitHub terms)

- **Trigger**: a condition check (`can this happen?`).
- **Effect**: an action (`do this change now`).
- **On action**: automatic hook that runs when an event happens (e.g. new heir).
- **Modifier**: ongoing bonus/penalty applied to country/province/etc.
- **Scripted trigger/effect**: reusable helper block to avoid copy-paste logic.
- **Localization (loc)**: player-facing text strings.
- **Scope**: what object your script is currently acting on (country/province/ruler/etc.).
- **Vanilla**: base EU4 behavior without Anbennar custom systems.

## GitHub mini-glossary

- **Branch**: your workspace copy.
- **Commit**: one saved set of changes.
- **Pull Request (PR)**: request to merge branch into `main`.
- **Merge conflict**: same lines changed in two places; you must choose final text.

## Naming convention (noob-friendly rule)

Prefer clear names over short names:

- Good: `verne-wyvern-orders-mercs-and-monuments-reference.md`
- Bad: `vwmom-ref.md`

Use one suffix consistently:

- `-reference.md` for implementation maps
- `-playbook.md` for process/how-to docs
- `-ledger.md` for tracking tables
- `README.md` for folder entry pages
