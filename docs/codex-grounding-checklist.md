# Codex Grounding Checklist

## Why this file exists
Use this before any real coding task.

It exists to stop blind guessing.

For Verne and Anbennar work, the right order is:

1. read the repo
2. find the existing pattern
3. identify shared files
4. check EU4 engine rules if needed
5. only then edit

If this checklist is not filled in yet, the session is still in grounding mode.

## How to use this
At the start of a task, Codex should report the answers to the sections below before making edits.

The answers can be given in chat, but they should follow this structure.

If a section cannot be answered from the repo yet, that is a signal to keep reading instead of coding.

## Task kickoff template

### 1. Task being attempted
- one-sentence description of the change
- what "done" means for this session

### 2. Exact files read first
List the exact files inspected before any edit.

Include the real paths, not vague descriptions.

Minimum expectation for Verne work:
- the direct target file
- the nearest existing Verne implementation file
- any shared multi-country file that already owns the same system

### 3. Existing repo pattern to mirror
For each major mechanic, name the exact existing pattern that will be copied.

Examples:
- `define_heir` pattern from [`events/Flavour_Verne_A33.txt`](../events/Flavour_Verne_A33.txt)
- `define_advisor` pattern from [`events/Flavour_Verne_A33.txt`](../events/Flavour_Verne_A33.txt)
- `on_new_heir` hook style from [`common/on_actions/00_on_actions.txt`](../common/on_actions/00_on_actions.txt)
- mission reward helper pattern from existing Anbennar mission files
- merc-company unlock and upgrade pattern from existing elite merc files

If there is no good repo pattern, say that explicitly instead of pretending there is one.

## Shared-file audit

### 4. Shared multi-country files affected
List every shared file that may be touched or whose behavior must be preserved.

Typical Verne examples:
- [`common/ideas/anb_country_ideas.txt`](../common/ideas/anb_country_ideas.txt)
- [`localisation/anb_powers_and_ideas_l_english.yml`](../localisation/anb_powers_and_ideas_l_english.yml)
- [`common/ideas/00_basic_ideas.txt`](../common/ideas/00_basic_ideas.txt)
- [`common/great_projects/anb_monuments_missions.txt`](../common/great_projects/anb_monuments_missions.txt)
- [`common/mercenary_companies/0_anb_elite_mercenaries.txt`](../common/mercenary_companies/0_anb_elite_mercenaries.txt)
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)
- [`events/Flavour_Verne_A33.txt`](../events/Flavour_Verne_A33.txt)
- [`common/on_actions/00_on_actions.txt`](../common/on_actions/00_on_actions.txt)

### 5. Safe Verne-only files for this task
List the files that are safe places to add helper-layer or submod content.

Examples:
- new `verne_overhaul_*.txt` helper files
- dedicated Verne-only event files
- dedicated Verne-only localization file

### 6. Replacement decision
For each touched system, answer:

- patch existing shared anchor
- use keyed override
- add new Verne-only object

Also explain why that choice is safer than the alternatives.

## Compatibility audit

### 7. Generic EU4 and Anbennar dependencies
Check whether shared systems still expect vanilla or basic behavior.

This matters most for:
- `has_idea_group`
- reform gates
- estate agendas
- policy unlock logic
- scripted triggers and effects that assume vanilla groups or vanilla object names

For doctrine or idea work, explicitly name the first compatibility risks found.

Examples:
- shared policy files that still expect `exploration_ideas`
- reform files that still expect `maritime_ideas`
- agenda files that still expect `exploration_ideas`

### 8. What will be preserved for v0.1
State which generic behaviors will still work after the change, and which ones are intentionally deferred.

This is the point where Codex must say:
- "safe now"
- "safe with alternate checks"
- or "deferred risk"

## Syntax and rules audit

### 9. Engine-rule check
If syntax or engine behavior is uncertain, verify it before coding.

Use this trust order:

1. existing Anbennar implementation in this repo
2. local EU4 wiki snapshot pages listed in [`docs/eu4-local-reference-index.md`](./eu4-local-reference-index.md)
3. live EU4 wiki or other primary modding reference
4. memory only if the above are not enough

Record:
- which rule was checked
- where it was verified
- whether the repo, local snapshot, or live wiki was the stronger authority for this task

## Assumptions and go or no-go

### 10. Open assumptions
List anything still uncertain.

Examples:
- whether a same-name override is safe here
- whether a mission check is consumed elsewhere
- whether a monument already has hidden scripted hooks

### 11. Go or no-go
End every grounding pass with one line:

- `GO`: enough grounding exists to edit safely
- `NO-GO`: more repo reading is required first

## Short prompt for future sessions
Use this when you want Codex to ground itself before coding:

```text
Before editing anything, do the grounding checklist in docs/codex-grounding-checklist.md.
Show me:
1. the exact files you read,
2. the repo pattern you will mirror,
3. the shared multi-country files involved,
4. any vanilla/basic compatibility risks,
5. whether this is GO or NO-GO.
Do not start coding until you have done that.
```
