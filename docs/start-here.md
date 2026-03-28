# Start Here (Noob-Friendly)

## Session start rule (read before any coding)

Before every coding session, open [docs/wiki/current-work-queue.md](./wiki/current-work-queue.md) and pick work **only** from the **Now** section.

Do not begin coding from backlog ideas, chat suggestions, or old notes unless they were first promoted into **Now** in the queue.

If you are new to GitHub and modding, read in this order:

1. [docs/wiki/current-work-queue.md](./wiki/current-work-queue.md)
2. [docs/README.md](./README.md)
3. [docs/wiki/README.md](./wiki/README.md)
4. [docs/wiki/fluff-and-art-production-playbook.md](./wiki/fluff-and-art-production-playbook.md)
5. [docs/wiki/anbennar-base-vs-verne-change-ledger.md](./wiki/anbennar-base-vs-verne-change-ledger.md)
6. [docs/wiki/verne-id-ledger.md](./wiki/verne-id-ledger.md)
7. [docs/implementation-crosswalk.md](./implementation-crosswalk.md)
8. one matching article from [docs/repo-maps/README.md](./repo-maps/README.md)

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

## Safe checkpoint commit rule

Hard default for noobs and automation-heavy workflows:

- One commit should usually touch **one system slice** only (for example: doctrine **OR** reform **OR** one mission node), not all at once.

This is a **safety default**, not a productivity tax. If a change is tightly coupled and must ship together, keep one larger commit but explain why in the commit body.

Why this helps:

- makes merge conflicts smaller and easier to resolve,
- makes smoke-check failures easier to diagnose,
- keeps rollback simple when one slice breaks.

### Recommended checkpoint template

When you package a normal slice commit, include these parts in order:

1. helper logic
2. gameplay object
3. localization
4. smoke profile sentinel
5. docs ledger update

### Fast-path exceptions (when bigger commits are okay)

Use one combined commit when at least one is true:

1. a single mechanic cannot work without paired files (script + loc + one sentinel),
2. you are doing a pure mechanical refactor/rename across one family,
3. the branch is a private spike and you will squash before PR.

If you use an exception, add one line in the commit body:

- `checkpoint-exception: required paired change for <system>`

### Example noob commit message format

Use:

- `verne: add <slice> + loc + smoke sentinel`

Example:

- `verne: add silver-oaths doctrine prototype + loc + smoke sentinel`

## CI quick-fix commands (matches workflow summaries)

When GitHub Actions reports a failed audit, start with the exact command shown in the job summary:

- Compile Python scripts: `python -m py_compile scripts/*.py`
- Docs conflict guard: `python scripts/docs_conflict_guard.py`
- Checklist link audit: `python scripts/checklist_link_audit.py`
- Verne checklist audit: `python scripts/verne_checklist_audit.py`
- Localization audit: `python scripts/localisation_audit.py --file localisation/Flavour_Verne_A33_l_english.yml`
- Event ID audit: `python scripts/event_id_audit.py --file events/Flavour_Verne_A33.txt --file events/verne_overhaul_dynasty_events.txt`
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

## What to do next when conflicts remain (missions/events/localisation)

If a merge still leaves conflict markers in gameplay content files, use this quick rule:

1. **Run docs-only cleanup first** when conflicts are only in docs hotspots or `.gitattributes`:
   - `python scripts/resolve_content_conflicts.py --union-docs-only`
2. **Prefer `--prefer-theirs`** when upstream `main` contains deliberate fixes you want to keep as the baseline (for example, validated IDs, corrected scopes, or audited localisation keys).
3. **Prefer `--prefer-ours`** when your feature branch has the intended new Verne implementation and upstream changes are older or generic placeholders.
4. **Stop automation and inspect conflict blocks manually** when both sides changed logic/text meaning (not just formatting/order), especially for mission triggers/effects, event options, or localisation wording tied to script keys.

### Concrete examples

- `missions/Verne_Missions.txt`: if both sides changed `potential`/`allow` logic for the same mission node, do **manual block-by-block review** so you do not silently drop required triggers.
- `events/Flavour_Verne_A33.txt`: if one side adds a new event option and the other changes `country_event` effects or event IDs, do **manual review** first; only use `--prefer-theirs`/`--prefer-ours` if you are sure one side is strictly obsolete.
- `localisation/Flavour_Verne_A33_l_english.yml`: if both sides edit the same localisation key text, use **manual review** to keep the intended player-facing wording and avoid mismatches with script keys.

Final verification command after resolving conflicts:

- `python scripts/docs_conflict_guard.py`
