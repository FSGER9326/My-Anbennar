# Start Here (Noob-Friendly)

If you are new to GitHub and modding, read in this order:

1. [docs/README.md](./README.md)
2. [docs/wiki/README.md](./wiki/README.md)
3. [docs/wiki/fluff-and-art-production-playbook.md](./wiki/fluff-and-art-production-playbook.md)
4. [docs/wiki/anbennar-base-vs-verne-change-ledger.md](./wiki/anbennar-base-vs-verne-change-ledger.md)
5. [docs/implementation-crosswalk.md](./implementation-crosswalk.md)
6. one matching article from [docs/repo-maps/README.md](./repo-maps/README.md)

## Default recommended workflow (run this first)

Use the noob autopilot script as your default branch-sync + safety-check workflow before you push:

- **macOS/Linux (bash):** `bash scripts/noob_autopilot.sh`
- **Windows PowerShell:** `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1`

If merge conflicts still remain after docs auto-resolution, rerun with a one-flag fallback:

- **Prefer main side (safest if unsure):**
  - bash: `bash scripts/noob_autopilot.sh --prefer-main`
  - PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-main`
- **Prefer your branch side:**
  - bash: `bash scripts/noob_autopilot.sh --prefer-branch`
  - PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-branch`

This runs a guided linear flow with step labels, conflict handling, docs guards, and smoke checks.

Hard rule for any branch with an open PR: run this sync helper first, follow the exact `Next command` if it reports unresolved conflicts, and only push after it finishes successfully.

Personal habit mantra: **sync first, then push.**

Run pre-PR gate before opening any PR.

- **macOS/Linux (bash):** `bash scripts/pre_pr_gate.sh`
- **Windows PowerShell:** `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\pre_pr_gate.ps1`

## Daily use (quick command shortcuts)

Pick one mode so you can run the right checks without thinking:

- **Implementation mode (script/event/loc changes)**
  - **macOS/Linux (bash):** `bash scripts/verne_mode_impl.sh`
  - **Windows PowerShell:** `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_mode_impl.ps1`
- **Docs mode (checklist/docs changes)**
  - **macOS/Linux (bash):** `bash scripts/verne_mode_docs.sh`
  - **Windows PowerShell:** `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_mode_docs.ps1`

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


## What should we do right now? (Decision guide)

If you feel lost, use this decision tree in order.

### Step 1: Check readiness to implement

You are **ready to start implementation now** only if all are true:

- the target mechanic has a repo-map reference with concrete anchors,
- the change ledger has a row for the target,
- there is at least one smoke-test checklist item for the touched IDs,
- scope is a small `v0.1` slice (not a full overhaul in one go).

If any item is missing, do not implement yet—finish grounding first.

### Step 2: Choose one of four modes

1. **Scan + index mode** (use when anchors are still unclear)
   - Create/expand one repo-map article for one target.
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

### Practical rule of thumb

- If your next commit changes **more than 5-7 files** across unrelated systems, split it.
- If you cannot explain the exact entry point and state carriers in two sentences, do one more scan pass first.
- Prefer many small completed slices over one large partially-finished rewrite.

## CI quick-fix commands (matches workflow summaries)

When GitHub Actions reports a failed audit, start with the exact command shown in the job summary:

- Compile Python scripts: `python -m py_compile scripts/*.py`
- Docs conflict guard: `python scripts/docs_conflict_guard.py`
- Checklist link audit: `python scripts/checklist_link_audit.py`
- Verne checklist audit: `python scripts/verne_checklist_audit.py`
- Localization audit: `python scripts/localisation_audit.py --file localisation/Flavour_Verne_A33_l_english.yml`
- Event ID audit: `python scripts/event_id_audit.py --file events/Flavour_Verne_A33.txt`
- Country smoke runner: `python scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json`
- Bash smoke checks: `bash scripts/verne_smoke_checks.sh`
- PowerShell smoke checks: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1`

## Keeping PRs low-conflict (stacking strategy)

When you have multiple open PRs, use this order to minimize conflict churn:

1. Merge foundational/base-doc automation first (often crosswalk dedupe).
2. Rebase every downstream branch onto the new `main`.
3. Drop commits that are already merged (interactive rebase) or recreate branch with cherry-pick.
4. Keep each PR single-topic:
   - smoke/profile changes
   - crosswalk dedupe
   - wrapper scripts
5. Avoid parallel PRs touching hotspots unless necessary:
   - `docs/implementation-crosswalk.md`
   - `docs/start-here.md`
   - `scripts/*`

Use the helper script to detect overlap and propose merge order:

- `python scripts/pr_conflict_churn_plan.py --base main`
- If you do not have GitHub CLI available, provide branches directly:
  - `python scripts/pr_conflict_churn_plan.py --base main --branches branch-a branch-b branch-c`

After merging the first PR, rerun the script and repeat for remaining branches.
