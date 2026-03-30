# Verne Script Commentary Convention

## Objective

Define one concise, reusable comment standard for Verne gameplay script anchors (missions, events, decisions, reforms, and helper entries) so implementation intent survives refactors, merges, and future AI sessions.

This convention is intentionally **documentation-only**. It does not alter gameplay behavior.

## Scope and intent

Use this standard when touching:

- `missions/Verne_Missions.txt`
- `events/Flavour_Verne_A33.txt`
- `events/verne_overhaul_*.txt`
- Verne-specific helper files and keyed override files

Goal: preserve both **mechanical purpose** and **lore/playstyle meaning** where script logic alone is ambiguous.

## Required comment fields

For each selected anchor, place a compact comment block directly above the object (mission/event/decision/etc.) containing:

1. **Commentary (plain-language)**
   - One sentence: what this object does mechanically.
2. **Base vs new**
   - Mark as one of:
     - `base-reused`
     - `base-patched`
     - `project-new`
3. **Playstyle effect**
   - One sentence: what player behavior this encourages.
4. **Risk note**
   - Name fragile IDs/flags/keys that must remain stable.

Optional fields when relevant:

- **Province context**: include `province_id`, province name (if known), and region/continent context.
- **Lore-fit note**: classify as `official-canon`, `inferred-from-repo`, or `project-canon`.

## Canon classification rule

When lore framing is not obvious from script alone, explicitly classify the line as:

- `official-canon` when directly aligned to known Anbennar canon
- `inferred-from-repo` when derived from existing implementation patterns/text
- `project-canon` when this submod intentionally reinterprets behavior

Do not silently mix these categories.

## Formatting template

```txt
# Commentary (plain-language): ...
# Base vs new: base-reused | base-patched | project-new
# Playstyle effect: ...
# Risk note: keep <ids/flags/keys> stable.
# Province context: <id/name/region>   (optional)
# Lore-fit note: official-canon | inferred-from-repo | project-canon   (optional)
```

## Placement and length rules

- Keep each line short (target: one sentence).
- Place immediately above the anchor object.
- Avoid duplicating obvious script behavior word-for-word.
- Prefer commentary at high-value anchors over blanket comment spam.

## Suggested first-wave anchors (Verne)

For low-risk adoption, prioritize anchors that are lore-significant and frequently edited:

- Missions
  - `A33_the_vernman_renaissance`
  - `A33_the_grand_port_of_heartspier`
- Events
  - `verne.12` (Corinite conversion)
  - `verne.13` (Wyvern rider generator)

## Merge-risk discipline

To reduce conflicts:

- Keep shared docs/automation edits in separate PRs from gameplay script edits.
- In gameplay PRs, touch only selected anchors unless a wider refactor is intentional.
- Avoid opportunistic formatting churn in hotspot files.

## Definition of done for commentary adoption

A commentary pass is complete when:

- selected anchors include required fields,
- base-vs-new and risk notes are explicit,
- canon classification is present where lore interpretation is non-obvious,
- gameplay logic is unchanged,
- grep checks confirm anchor IDs and keys were not accidentally renamed.
