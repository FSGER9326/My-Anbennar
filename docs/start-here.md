# Start Here

If you are new to GitHub and modding, read in this order:

1. [docs/README.md](./README.md)
2. [docs/wiki/README.md](./wiki/README.md)
3. [docs/wiki/fluff-and-art-production-playbook.md](./wiki/fluff-and-art-production-playbook.md)
4. [docs/wiki/anbennar-base-vs-verne-change-ledger.md](./wiki/anbennar-base-vs-verne-change-ledger.md)
5. [docs/status/verne-live-implementation-status.md](./status/verne-live-implementation-status.md)
6. [docs/implementation-crosswalk.md](./implementation-crosswalk.md)
7. one matching article from [docs/repo-maps/README.md](./repo-maps/README.md)

## Tiny glossary (modding terms, not GitHub terms)

- **Trigger**: a condition check (`can this happen?`).
- **Effect**: an action (`do this change now`).
- **On action**: automatic hook that runs when an event happens (for example a new heir).
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

> [!IMPORTANT]
> **One-command path (default):**
> `bash scripts/noob_autopilot.sh`

This page is intentionally minimal: run the default command, then escalate only if the command tells you to.

## What should we do right now? (Decision guide)

1. Run `bash scripts/noob_autopilot.sh`.
2. If it passes, proceed with your normal push/PR flow.
3. If it reports conflicts, overlap risk, or failing checks, use the escalation links below.

## Workflow glossary

- **Hotspot file:** a frequently edited file where parallel edits are likely to conflict.
- **Single-writer file:** a file designated to one lane/author at a time to prevent merge churn.
- **Smoke checks:** fast structural checks that catch broken links, keys, or references early.

## Escalation links only

If any item is missing, do not implement yet - finish grounding first.

### Step 2: Choose one of four modes

1. **Scan + index mode** (use when anchors are still unclear)
   - Create or expand one repo-map article for one target.
   - Update index files in the same commit.

2. **Implementation planning mode** (use when anchors are clear but risk is high)
   - Write touched-file list, risk notes, and first `v0.1` scope.
   - Define 3-5 smoke checks before coding.

3. **Theory-crafting mode** (use when design intent is unsettled)
   - Limit to one design question at a time.
   - Convert the outcome into concrete implementation constraints.

4. **Implementation mode** (use when steps above are done)
   - Ship one thin slice: helper logic -> hook wiring -> localization -> ledger update.

### Step 3: Recommended immediate sequence (to regain momentum)

- Pick **one** target in a documented family.
- Do a 30-60 minute grounding refresh (anchors + IDs + current behavior).
- Lock a tiny `v0.1` implementation scope.
- Implement and validate smoke checks.
- Commit and update ledger/index in the same pass.

Repeat this loop before expanding to the next target.

### Step 4: If Git or automation feels confusing

Run:

- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\repo_doctor.ps1`

That will tell you:

- what branch you are on
- whether you are ahead or behind
- whether the working tree is dirty
- whether hooks are installed
- whether a merge or rebase is already in progress

### Practical rule of thumb

- If your next commit changes **more than 5-7 files** across unrelated systems, split it.
- If you cannot explain the exact entry point and state carriers in two sentences, do one more scan pass first.
- Prefer many small completed slices over one large partially-finished rewrite.
- Command reference and operational index:
  [docs/wiki/checklist-automation-system.md](./wiki/checklist-automation-system.md)
- Conflict decisions and mitigation flow:
  [docs/wiki/merge-conflict-prevention-playbook.md](./wiki/merge-conflict-prevention-playbook.md)
- Verne canonical file ownership truth:
  [docs/wiki/verne-canonical-vs-legacy-file-registry.md](./wiki/verne-canonical-vs-legacy-file-registry.md)
- Parallel lane model for safe multi-tasking:
  [docs/wiki/parallelization-lanes-playbook.md](./wiki/parallelization-lanes-playbook.md)
- Full docs hub:
  [docs/README.md](./README.md)
