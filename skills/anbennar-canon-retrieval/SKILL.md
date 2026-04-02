# anbennar-canon-retrieval

## Purpose
Separate lore wiki retrieval from gameplay wiki retrieval, and force canon citations into specs. Lore wiki is support material — never the final authority.

## Two Wiki Types

### 1. Anbennar Lore Wiki (wiki.anbennar.com)
- **Use for:** Worldbuilding context, character names, historical events, cultural details, geography, religion backstories
- **Authority:** LOW — lore wiki is support material, not game mechanics
- **Rule:** Always cross-reference with repo for any game-affecting claim

### 2. Anbennar Gameplay Wiki (anbennar.fandom.com)
- **Use for:** Race mechanics, development economics, formation decisions, DLC requirements, tag-specific mechanics
- **Authority:** MEDIUM — good for context, unevenly up to date
- **Rule:** Verify specific IDs against repo before citing

## Lore vs Gameplay Separation

When a request involves lore AND mechanics:

1. Separate the lore question from the game mechanic question
2. Use lore wiki for worldbuilding context
3. Use gameplay wiki + repo for mechanics
4. Never let lore override game mechanics

Example:
```
Request: "Add an event where Grombar's orc riders discover the Silverforge mountains"

Lore part: "Silverforge mountains geography, orc clan history"
→ Use lore wiki for context, cite in spec

Gameplay part: "New event for Grombar tag, must use correct event namespace, trigger, effects"
→ Use repo precedent, cite specific file/ID
```

## Canon Citation Requirements

Every lore-sensitive spec must include:

```yaml
canon_sources:
  lore:
    - page: "Silverforge"
      url: "wiki.anbennar.com/Silverforge"
      used_for: "geography and mountain names"
  gameplay:
    - page: "Grombar"
      url: "anbennar.fandom.com/Grombar"
      used_for: "orc race mechanics, government type"
  repo_precedent:
    - path: "events/verne_overhaul_grombar_events.txt"
      used_for: "existing Grombar event patterns, namespace"
```

## What "Canon" Means in Practice

- **Canon for mechanics:** What the repo implements — mission IDs, event chains, modifiers, decisions
- **Canon for lore:** What the lore wiki describes — history, geography, culture, religion
- **Conflict resolution:** If lore says X but repo implements Y → repo wins, note the divergence in spec

## Repo-First Rule

Before searching any wiki:
1. Check repo for the same content first
2. Search `missions/Verne_Missions.txt` for tag-specific content
3. Search `events/` for existing event patterns
4. Search `common/` for modifier/decision/CB patterns

Only use wiki when repo doesn't have the answer.

## Lore Decision Workflow

1. **Identify** — Is this a lore question or a game mechanics question?
2. **Scope** — Does it affect actual EU4 content (missions, events, modifiers)?
3. **Repo first** — Check repo for existing implementations
4. **Lore support** — Use lore wiki for context/background only
5. **Cite** — Record source in spec's `canon_sources` block
6. **Flag divergence** — Note if repo and lore conflict

## Important Lore Areas for Verne

- Grombar (orc nation, racial mechanics)
- Verne (human kingdom, court mechanics)
- The Liliac War (recent conflict, affects Verne's position)
- Dragonwake (western region, Wyvern Kingdoms)
- Silverforge (dwarven holds, mountain trade)
- The Heartspier (port city, maritime trade)
