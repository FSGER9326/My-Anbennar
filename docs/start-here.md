# Start Here (Noob-Friendly)

> [!IMPORTANT]
> ## You only need this command
> `bash scripts/noob_autopilot.sh`
>
> Run this before you push. It handles sync/merge flow, conflict safety checks, and full smoke checks in one flow.

If you are new to GitHub and modding, read in this order:

1. [docs/README.md](./README.md)
2. [docs/wiki/README.md](./wiki/README.md)
3. [docs/wiki/checklist-automation-system.md](./wiki/checklist-automation-system.md)
4. [docs/wiki/merge-conflict-prevention-playbook.md](./wiki/merge-conflict-prevention-playbook.md)
5. [docs/wiki/anbennar-base-vs-verne-change-ledger.md](./wiki/anbennar-base-vs-verne-change-ledger.md)
6. [docs/wiki/verne-id-ledger.md](./wiki/verne-id-ledger.md)
7. [docs/wiki/verne-canonical-vs-legacy-file-registry.md](./wiki/verne-canonical-vs-legacy-file-registry.md)
8. [docs/implementation-crosswalk.md](./implementation-crosswalk.md)
9. one matching article from [docs/repo-maps/README.md](./repo-maps/README.md)

## Default recommended workflow

Use this as your default branch-sync + safety-check command before every push:

- `bash scripts/noob_autopilot.sh`

Hard rule for branches with open PRs: sync first, then push.

If the autopilot flow reports conflicts or overlap risk, follow the dedicated playbook instead of ad-hoc commands:

- [Merge Conflict Prevention Playbook](./wiki/merge-conflict-prevention-playbook.md)

For the compact command matrix (without deep fallback prose), use:

- [Checklist Automation System](./wiki/checklist-automation-system.md)

## Tiny glossary (modding terms)

- **Trigger**: a condition check (`can this happen?`).
- **Effect**: an action (`do this change now`).
- **On action**: automatic hook that runs when an event happens.
- **Modifier**: ongoing bonus/penalty.
- **Scripted trigger/effect**: reusable helper block.
- **Localization (loc)**: player-facing text.
- **Scope**: what object script is acting on.
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

## Safe checkpoint commit rule

Hard default for noobs and automation-heavy workflows:

- One commit should usually touch **one system slice** only (for example: doctrine **OR** reform **OR** one mission node).

Why this helps:

- keeps merge conflicts smaller,
- keeps smoke-check failures easier to diagnose,
- keeps rollback simple when one slice breaks.

### Recommended checkpoint template

1. helper logic
2. gameplay object
3. localization
4. smoke profile sentinel
5. docs ledger update

### Fast-path exceptions (larger commits allowed)

Use one combined commit when at least one is true:

1. a single mechanic cannot work without paired files,
2. you are doing one mechanical refactor/rename across a single family,
3. the branch is a private spike and you will squash before PR.

If you use an exception, add one line in the commit body:

- `checkpoint-exception: required paired change for <system>`
