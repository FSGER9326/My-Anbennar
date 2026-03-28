# Verne Country Dossier

## 1) Identity snapshot
- **Tag / primary formable tags:** VER (Kingdom of Verne baseline; keep formable continuity rules if tag flow changes later).
- **Region / subcontinent:** Cannor (Dameshead + overseas projection lanes).
- **Canon class:** `INFERRED_CANON` + `PROJECT_CANON` hybrid.
  - `INFERRED_CANON`: preserves existing in-repo Verne anchors (missions, events, adventure chain, dynasty behavior).
  - `PROJECT_CANON`: introduces structured overhaul layers (doctrine/reform/disaster framework) that extend rather than erase baseline behavior.
- **Core fantasy:** silver-court naval monarchy that blends dynasty legitimacy, maritime projection, and elite wyvern order prestige.
- **Primary player fantasy verbs (3-6):** broker, project, colonize, patronize, discipline, centralize.

## 2) Gameplay intent
- **Intended campaign arcs:**
  - maritime/trade hegemon Verne;
  - imperial court-influence Verne;
  - wyvern order military-projection Verne;
  - flexible opener that does not force one linear mission route.
- **Power profile by phase (early/mid/late):**
  - early: legitimacy + alliance/court setup with selective external pressure;
  - mid: doctrine/reform specialization and sea-lane reach;
  - late: high ceiling with balancing pressure/disaster risks if internal pillars are neglected.
- **Win condition feel (what "success" should feel like):** a stable and prestigious silver court that can project power overseas without collapsing internally.
- **Anti-patterns to avoid (what this country should not become):**
  - generic map-paint blob with no court/dynasty identity;
  - one-route mission railroad;
  - power growth without pressure-system counterweights.

## 3) Lore role
- **Narrative role in region:** Verne is framed as a prestige monarchy whose legitimacy and diplomacy are part of its strategic weapon set, not flavor-only text.
- **Rival/friend identity anchors:** Corvuria and Lorent relationships remain key external identity poles; mission/event writing should keep these tensions legible.
- **Religious/cultural posture:** Corinite transition and non-Corinite branches are both meaningful identity surfaces; implementation must preserve conditional behavior.
- **How mechanics express lore role:** dynasty continuity, court advisor shaping, mission-routed state posture, and wyvern/monument symbols convert lore identity into repeatable gameplay loops.

## 4) System map and dependencies
- **Primary implementation anchors (missions/events/decisions/etc.):**
  - `missions/Verne_Missions.txt`
  - `events/Flavour_Verne_A33.txt`
  - `decisions/VerneDecisions.txt`
- **Shared-file dependencies (non-country-exclusive files):**
  - `common/mercenary_companies/0_anb_elite_mercenaries.txt`
  - shared monument/government/idea layers referenced by existing Verne docs and repo maps.
- **Cross-nation coupling risks:** mission or event edits can ripple into shared Cannor diplomacy/economy balance and shared content files.
- **Automation dependencies (profiles/scripts/checks):**
  - `automation/country_profiles/verne.json`
  - `scripts/country_smoke_runner.py`
  - `scripts/checklist_manifest_audit.py`

## 5) Prior-behavior delta
- **Baseline behavior (before overhaul):** meaningful but fragmented Verne identity spread across shared files and legacy anchors.
- **Current/target behavior (after overhaul):** unified dossier-driven design/implementation with explicit system intent, canon classification, and validation hooks.
- **Why this delta exists:** to prevent lore-mechanics drift, reduce duplicate assumptions, and make future multi-country scaling feasible.
- **Compatibility constraints (saves/upstream sync):** prefer anchored edits over broad rewrites in shared files; keep key names stable and avoid namespace churn.

## 6) Implementation guardrails
- **ID / namespace policy:** maintain strict uniqueness and keep Verne-specific keys under stable Verne prefixes where possible.
- **Key naming prefixes:** align decisions/events/modifiers/localisation with existing Verne naming families; avoid introducing parallel synonyms for the same mechanic.
- **Validation gates before merge:**
  - run country smoke profile for Verne;
  - run checklist manifest audit;
  - grep/smoke for unresolved markers and key drift.
- **Known high-risk regressions:**
  - shared-file edits accidentally impacting non-Verne nations;
  - lore role loss from over-normalizing into generic EU4 patterns;
  - broken mission/event key parity during refactors.

## 7) Current status
- **Scanned:** true
- **Mapped:** true
- **Verified:** true
- **Reference docs reviewed:**
  - `docs/mod-spec.md`
  - `docs/implementation-crosswalk.md`
  - `docs/repo-maps/verne-*.md`
  - `docs/lore/verne-*.md`
