# Verne Overhaul Implementation Audit (Current Repo State)

This file audits the **actual repo implementation state** against the canonical design docs in `docs/design/`.

Goal:
- identify what is already implemented,
- identify where the repo still contains prototype / placeholder content,
- define the most practical next coding slice.

---

## Executive Summary

The repo is **not starting from zero**.
A first-pass Verne overhaul implementation already exists across:
- `common/ideas/verne_doctrine_groups.txt`
- `common/government_reforms/verne_overhaul_reforms.txt`
- `common/scripted_triggers/verne_overhaul_triggers.txt`
- `common/scripted_effects/verne_overhaul_effects.txt`
- `decisions/verne_overhaul_decisions.txt`
- `events/verne_overhaul_dynasty_events.txt`
- `common/on_actions/verne_overhaul_on_actions.txt`
- `missions/Verne_Missions.txt`

However, the current implementation is **mixed quality**:
- some parts are already useful and reasonably grounded,
- some parts are clearly scaffold/prototype,
- some parts diverge significantly from the canonical design docs.

So the real task is **reconciliation**, not raw greenfield creation.

---

## Current State by System

### 1. Doctrine groups

**Repo status:** prototype / incomplete / divergent

File:
- `common/ideas/verne_doctrine_groups.txt`

Observed state:
- only a single doctrine group appears implemented in the current file snapshot:
  - `verne_doctrine_silver_wake`
- its identity and effects do **not** match the canonical doctrine set described in `docs/design/doctrine-bible.md`
- naming scheme diverges from the canonical `verne_<name>_ideas` plan

Assessment:
- current file should be treated as an **early prototype**, not canonical implementation
- doctrine implementation remains a major gap

Best next action:
- replace/expand doctrine implementation based on the canonical doctrine bible
- do this in a structured batch, not ad hoc

---

### 2. Government reforms

**Repo status:** prototype / partial

File:
- `common/government_reforms/verne_overhaul_reforms.txt`

Observed state:
- current file contains a **v0.2 tier-1 triplet prototype**
- reform names are close in spirit to canonical design, but numeric packages are simplified and do not match the reform bible
- only a minimal slice is present

Assessment:
- useful as a scaffold
- not yet aligned with canonical reform packages in `docs/design/reform-bible.md`

Best next action:
- reconcile Tier 1 first
- then expand to Tier 2/3 with canonical packages

---

### 3. Scripted triggers

**Repo status:** useful partial implementation

File:
- `common/scripted_triggers/verne_overhaul_triggers.txt`

Observed state:
- includes some good reusable mission and state triggers
- includes real dynasty safeguard triggers
- naming does not fully match the newer implementation scaffolding plan
- only a subset of the planned trigger catalog exists

Assessment:
- this is a good foundation
- should be extended rather than discarded

Best next action:
- preserve working triggers
- add missing canonical helper triggers using the design naming plan where practical
- avoid duplicate near-synonyms unless migration requires them

---

### 4. Scripted effects

**Repo status:** very partial

File:
- `common/scripted_effects/verne_overhaul_effects.txt`

Observed state:
- currently contains only a small number of helper effects
- includes a useful helper for enabling the adventure network
- includes the Regatta spire swap helper
- does not yet reflect the broader helper-effect catalog in `implementation-scaffolding.md`

Assessment:
- valuable pattern established
- still far below intended helper-layer coverage

Best next action:
- expand helper effects around first-wave mission rewards and path flags

---

### 5. Dynasty safeguard

**Repo status:** implemented and meaningful

Files:
- `decisions/verne_overhaul_decisions.txt`
- `events/verne_overhaul_dynasty_events.txt`
- `common/on_actions/verne_overhaul_on_actions.txt`

Observed state:
- this is the strongest current implementation slice
- there is a real `on_new_heir` hook
- a real safeguard event exists
- it uses `define_heir` and replaces placeholder/invalid heirs
- this aligns well with the design docs and scaffolding intent

Assessment:
- this is a legitimate implemented system, not just scaffolding
- should be preserved and iterated carefully

Best next action:
- audit localisation/tooltips around it
- optionally extend toward the fuller dynastic-state progression later

---

### 6. Mission tree

**Repo status:** heavily implemented, mixed canonical alignment

File:
- `missions/Verne_Missions.txt`

Observed state:
- mission tree is already large and deeply customized
- several missions now call shared scripted triggers/effects
- some missions have helpful commentary and grounded reuse notes
- the current mission file clearly predates or only partially matches the newer route-family / projection-score design language
- some first-wave design themes already overlap with implementation (`Across the Pond`, `In Search of Adventure`, `Lament's Regatta`, etc.)

Assessment:
- this is the most important file to **preserve and reconcile**, not casually rewrite from scratch
- current implementation contains a lot of real work and should be treated as the operational baseline

Best next action:
- audit the first-wave mission set against `docs/design/mission-rewrite-spec.md`
- identify which missions are:
  - already close to canonical,
  - partially aligned,
  - still conceptually outdated

---

## Key Mismatch

The single biggest project reality is:

> The repo already contains a partial Verne overhaul implementation, but the design docs now describe a more structured and more canonical target state.

That means future work needs to answer this question every time:

**Are we preserving and refining an existing implementation, or replacing a prototype that no longer matches the design?**

Right now, the answer differs by subsystem:
- dynasty safeguard: preserve and extend
- triggers/effects: preserve and expand
- reforms: prototype, reconcile
- doctrine groups: prototype, likely replace/expand
- missions: preserve and reconcile carefully

---

## Best Next Coding Slice

The most practical next implementation slice is:

### Mission/reform/doctrine reconciliation for the earliest Verne state

Specifically:
1. reconcile **Tier 1 reforms** to canonical values,
2. create/repair the **early precursor flag layer**,
3. audit the earliest mission cluster against canonical design:
   - `Old Friends, Old Rivals`
   - `Alvar's Reform`
   - `The Grand Port of Heartspier`
   - `Across the Pond`
   - `In Search of Adventure`
4. defer full doctrine-system replacement until the early mission/reform state is nailed down.

Why this slice first:
- it matches the implementation dependency order in the design docs,
- it affects early gameplay identity immediately,
- it avoids trying to rewrite the entire mission tree or all 21 doctrine groups in one pass.

---

## Recommended Work Order

### Near-term
1. audit + patch Tier 1 reforms
2. add precursor path flags/effects
3. patch early missions to consume precursor flags instead of brittle late-doctrine assumptions

### After that
4. build proper first-wave doctrine groups
5. add first-wave policies
6. extend helper effects so missions stop carrying huge custom reward logic inline

### Later
7. continue mission reconciliation deeper into the tree
8. refine order companies / disasters / advisor layers

---

## Working Rule

For Verne in this repo, prefer:

- **preserve and patch** when a working implementation already exists,
- **replace only the clearly prototype layers**,
- and always treat `missions/Verne_Missions.txt` as a high-risk file that needs targeted, grounded edits rather than broad rewrites.
