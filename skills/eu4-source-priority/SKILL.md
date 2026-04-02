# eu4-source-priority

## Purpose
Teach the agent which EU4/Anbennar sources outrank others, and when to trust repo over wiki.

## Source Hierarchy (descending priority)

1. **Checked-out repo at HEAD**
   - File at `C:\Users\User\Documents\GitHub\My-Anbennar`
   - The authoritative source for: mission IDs, modifier names, event namespaces, decision keys, loc keys, government reform IDs, trigger/effect usage patterns
   - Always scan here first for precedent

2. **Upstream dev history / merge requests**
   - Upstream: `https://gitlab.com/Sando13/anbennar-eu4-dev.git` branch `new-master`
   - Check when looking for: recent bug fixes, mechanic patterns, similar implementations
   - Use `git log upstream/new-master --oneline -20` to see recent changes

3. **EU4 modding wiki** (eu4.paradoxwikis.com)
   - Primary reference for: trigger/effect syntax, scope rules, scripted effects/triggers, CB types, idea group structure
   - NOT authoritative for Anbennar-specific content

4. **Anbennar gameplay wiki**
   - Useful for: race mechanics, racial system development economics, formation decisions, DLC requirements
   - Unevenly up to date — verify against repo for specific IDs
   - Some pages verified for Update 19 / The Final Empire; others outdated

5. **Anbennar lore wiki**
   - Worldbuilding context only — color, history, character names
   - Never authoritative for game mechanics

## Decision Rules

- **Repo vs wiki conflict** → repo wins always
- **Wiki for mechanics** → cross-reference with repo code
- **Lore** → wiki OK as support, not authority
- **Anbennar-specific balance/flavor** → must verify against repo
- **EU4 engine rules** → wiki is primary, repo confirms

## How to Cite Sources in Specs

```yaml
sources:
  repo_precedents:
    - path: "missions/Verne_Missions.txt"
      reason: "existing lane 1-9 mission patterns"
  wiki_precedents:
    - page: "Effect"
      reason: "trigger/effect scope syntax"
  lore_sources:
    - page: "Grombar"
      reason: "orc race mechanics context"
```

## Source Check Workflow

Before any non-trivial task:
1. Read `design/upstream-lock.json` — record current upstream SHA
2. Search repo for existing examples of similar content
3. Use wiki only for EU4 engine mechanics, not Anbennar-specific content
4. Cite sources explicitly in the mod-spec
