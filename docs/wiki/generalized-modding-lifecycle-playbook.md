# Generalized Modding Lifecycle Playbook (Reusable for Any Country/System)

This is the reusable process to follow for:

- a different country
- a race-focused overhaul
- a new custom mechanic
- post-upstream update maintenance

## Terminology quick-clarifier

- **Workflow** is the correct term for the full phased process (Phase A through E).
- A **target** is one concrete mechanic/system you are analyzing (for example: rebellions, peace terms, religion branches).
- A **version** is one intentionally small delivery scope for a target (for example: `v0.1` map-only, `v0.2` map+gap rows, `v1.0` implementation-ready).
- A **deep-diff** means a detailed comparison between **base EU4 behavior** and **Anbennar implementation behavior**, down to concrete files, IDs, triggers/effects, and state carriers.
- A **family** (in this repo context) means a grouped mechanic domain that shares patterns and often shares grep anchors/checklists (for example: *estate/privilege family*, *government mechanics family*, *war & peace family*).
- A **smoke test** is a fast, high-signal check that confirms a high-risk object/flow is still wired after changes; it is intentionally shallow (not a full regression suite).

## Can A/B/C be repeated before moving on?

Yes. That is a good way to run this workflow at scale.

Recommended cadence:

1. Pick one target inside one family.
2. Run **Phase A → B → C** for that target only.
3. Stop at a “small done” checkpoint (`v0.1` or `v0.2`).
4. Repeat A/B/C for the next target in the same family.
5. After 3-5 targets, run a shared **Phase D** batch validation pass.
6. Then run one **Phase E** maintenance snapshot for the batch.

This keeps throughput high while preventing giant, fragile commits.

## Quantity + quality strategy (recommended operating mode)

### 1) Work in family-sized batches

- Batch by mechanic family to maximize grep/checklist reuse.
- Keep each target to one short scope statement and one explicit done-condition.

### 2) Use a fixed deliverable ladder per target

- `v0.1`: map + anchors + baseline diff verdict.
- `v0.2`: add object-ID appendix + gap/register rows.
- `v0.3`: add smoke-test checklist entries for high-risk IDs.
- `v1.0`: mark implementation-ready with extension guidance.

### 3) Set WIP limits

- No more than 2 in-progress targets at once.
- Finish/merge one before starting a third.

### 4) Define “done” with checkable gates

Each target is done only when:

- repo-map article exists/updated,
- index files are updated,
- gap/ledger row is updated,
- smoke checks are documented or executed,
- link-check + grep checklist pass.

### 5) Separate research commits from structure-only commits

- Commit content additions first.
- Reordering/formatting/index cleanups in a follow-up commit.
- This reduces review noise and merge conflicts.

### 6) Track confidence explicitly

Use a lightweight confidence tag per target:

- `HIGH`: object IDs and flow are verified in code.
- `MEDIUM`: anchors verified, but some branches inferred.
- `LOW`: scouting-level map; requires deep-diff follow-up.

This helps you keep moving without overstating certainty.

## Phase A: Ground and map first

1. Define the target system in one sentence.
2. Find existing Anbennar anchors (files already implementing similar behavior).
3. Compare against base EU4 expectation.
4. Record findings in repo-map docs.

## Phase B: Plan and scope

1. Decide smallest safe first version (v0.1).
2. List touched files (shared vs country-specific).
3. Write update risk notes.

## Phase C: Implement in thin slices

1. Add helper triggers/effects first.
2. Wire mission/event/reform hooks second.
3. Add localization in same commit.
4. Update the change ledger row in same commit.

## Phase D: Validate and document

1. Run grep checklist for that mechanic family.
2. Confirm no broken doc links.
3. Update index files so docs stay discoverable.

## Phase E: Upstream maintenance loop

1. Sync branch with upstream.
2. Run grep checklists again.
3. Mark impacted rows `NEEDS_REVALIDATION`.
4. Patch + retest + set back to `IMPLEMENTED`.

## Minimum artifact set per mechanic

- one repo-map reference article
- one gap-register row (or mark done)
- one change-ledger row
- one quick test/checklist note
