# Verne Modding QA Protocol

Automated quality assurance workflow for the Verne overhaul mod.
Runs after every modding session to catch bugs, logic errors, and text issues.

---

## Retroactive Standards System

When a new idea/standard is established mid-project, we don't just apply it to new work —
we scan ALL existing files retroactively. This prevents the "half-implemented improvement" problem.

### How It Works

1. New standard added to `docs/verne-standards-tracker.md` with a "since" date
2. QA subagent checks ALL files (not just recent changes) against active standards
3. Compliance matrix updated — ✅ compliant, ❌ needs update
4. Human decides: fix now or defer

### Example: "I want better tooltips"

```bash
# 1. Add standard S09 to tracker:
# "S09: Mission rewards show exact numbers, not vague descriptions"

# 2. Spawn QA subagent that scans ALL lane files (1-8) against S09:
# Result: lane1 ✅, lane2 ❌ (mission 3 says "enhanced naval power"), lane3 ✅...

# 3. Announce: "Lane 2, mission 3 needs update for S09"

# 4. Fix lane 2, mission 3 tooltip
```

### Key Insight
Every standard in the tracker is a "standing rule" — future QA checks always test against
ALL active standards, not just recently added ones. The compliance matrix tracks which files
have been verified, so we never lose track of what needs updating.

---

## QA Subagent Spawn Protocol

After ANY modding work that touches mission files, events, modifiers, or localisation,
spawn a QA subagent with the following task:

### Task Template

```
You are a QA checker for the Verne EU4 Anbennar mod. Check the files that were
recently modified for bugs, logic errors, and style issues.

Files to check: [list modified files]

Run these checks:

1. **Syntax Check** — Verify Paradox script syntax:
   - All { have matching }
   - No missing = signs
   - No stray characters
   - Comment syntax is # not // or /* */

2. **Flag Propagation** — Verify cross-mission dependencies:
   - If a mission SETS a flag (set_country_flag), the NEXT mission CHECKS it (has_country_flag)
   - If a mission requires another mission (required_missions), the chain is unbroken
   - No orphan missions (required by nothing, requiring nothing)

3. **Modifier Check** — Verify modifiers:
   - Every modifier referenced in add_country_modifier is DEFINED in common/event_modifiers/
   - Duration values are correct (-1 for permanent, positive for timed)
   - Modifier keys match the EU4 modifier list (no typos like "diplomatic_reputatione")

4. **Localisation Check** — Verify all player-facing text exists:
   - Every mission has _title, _desc, and _tt localisation keys
   - Every modifier has a _modifier_desc key
   - YAML format is correct (key:0 "value" with proper indentation)
   - No raw keys visible (MISSING_KEY style)

5. **Tooltip Clarity** — Verify tooltips explain:
   - What the player needs to DO (explicit conditions)
   - What the reward IS (specific numbers, not vague "improved trade")
   - Where to find related mechanics (cross-references to other missions/systems)
   - If tracking a hidden variable (like verne_overseas_projection), the tooltip shows the current value or progress

6. **Anbennar Lore Check** — Verify flavour text:
   - Country names match Anbennar lore (Verne, Heartspier, etc.)
   - Religious references use correct terms (Corinite, not generic "reformed")
   - Geographic references match Anbennar map (Cannor, Aelantir, Sarhal)
   - Tone matches existing Anbennar mission flavour text (dramatic but not silly)

7. **Logic Check** — Verify game mechanics:
   - Mission triggers are achievable (not requiring impossible combinations)
   - Reward values are balanced (compare to existing Anbennar mission rewards)
   - Reform references exist in common/government_reforms/
   - Province IDs exist in the province list

8. **Missing Connections** — Check for:
   - Missions that should chain but don't have required_missions
   - Events referenced in mission effects that don't exist
   - Decisions unlocked by flags that aren't set anywhere
   - Modifiers that expire but aren't refreshed

Report format:
## QA Report — [date]
### ✅ Passed
- [list of checks that passed]

### ⚠️ Warnings
- [non-critical issues, style suggestions]

### ❌ Errors
- [bugs that WILL break the game — must fix]

### 🔧 Suggested Fixes
- [exact code changes for each error]
```

### When to Run QA

| Trigger | Scope |
|---------|-------|
| Lane file written | Check that lane only |
| Multiple lanes modified | Check all modified lanes |
| Event file created | Events + localisation |
| Before commit | Full Verne check (all A33/* files) |
| Weekly maintenance | All Verne files |

### Spawning Pattern

```bash
# After modding work, I spawn:
# 1. QA subagent (checks for bugs)
# 2. Text review subagent (checks lore/style — can run in parallel)
# Both use absolute paths and report to the main session
```

---

## Common Errors Checklist

Quick reference for the most frequent Paradox scripting mistakes:

### Syntax
- [ ] Every `{` has a matching `}`
- [ ] No semicolons (Paradox script doesn't use them)
- [ ] Tabs for indentation (not spaces)
- [ ] `#` for comments only (not // or /* */)
- [ ] String values in quotes, numbers without

### Missions
- [ ] `position` is within the slot's range (1-9)
- [ ] `required_missions` chain is unbroken
- [ ] `provinces_to_highlight` has valid province IDs
- [ ] `icon` references a real mission icon name
- [ ] `has_country_shield = yes` is set

### Events
- [ ] `namespace` matches the file naming convention
- [ ] Event IDs follow `namespace.number` format
- [ ] Localisation keys: `<namespace>.<id>.t`, `.d`, `.a`
- [ ] `fire_only_once` is intentional (or removed for repeatable)
- [ ] `ai_chance` block exists in every option

### Modifiers
- [ ] Modifier name is unique (doesn't overwrite vanilla/Anbennar)
- [ ] Duration is `-1` for permanent, explicit number for timed
- [ ] All keys are valid EU4 modifier keys
- [ ] Localisation exists: `<name>_modifier_desc`

### Localisation
- [ ] Format: `key:0 "text"` (colon-zero, space, quote)
- [ ] YAML indentation is consistent (spaces, not tabs)
- [ ] Special chars escaped: `\"` for quotes inside text
- [ ] `$BR$` for line breaks in multi-line text

### Government Reforms
- [ ] Reform exists in `common/government_reforms/`
- [ ] `potential` and `trigger` blocks are correct
- [ ] Tier is appropriate for the lane position
- [ ] Prerequisite reforms are listed in order

---

## Tooltip Best Practices

### Player-Facing Tooltip Rules

1. **Always show numbers** — "+5% trade efficiency" not "improved trade"
2. **Show hidden variable progress** — "Overseas Projection: 3/10" not just "Track your overseas expansion"
3. **Explain prerequisites** — "Requires: Reform X, 5 colonial provinces" not just "Locked"
4. **Cross-reference related systems** — "See: Distant Horizons mission chain" for complex mechanics
5. **Use consistent terminology** — Pick one term per concept and stick with it

### Custom Tooltip Pattern
```pdx
# In mission effect:
custom_tooltip = verne_overseas_proj_add_1_tt

# In localisation:
verne_overseas_proj_add_1_tt:0 "Your Overseas Projection increases by 1. (Current: $VAR|verne_overseas_projection$)"
```

### Variable Tracking Tooltip Pattern
```pdx
# Show current value of hidden variable:
custom_tooltip = verne_projection_current_tt

# In localisation:
verne_projection_current_tt:0 "Current Overseas Projection: $VERNE_OVERSEAS_PROJECTION$"
verne_projection_tooltip_tt:0 "Overseas Projection is gained through colonial missions and trade company reforms. Higher values unlock additional trade bonuses."
```

---

*This protocol is self-improving — errors found by QA subagents are logged to .learnings/ and promoted here when patterns recur.*
